import json
import logging
import os

import boto3
import chalicelib
import requests
from chalice import Chalice, Response
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET')
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
DEEPL_AUTH_KEY = os.environ.get('DEEPL_AUTH_KEY')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')
SNS_SUBJECT = os.environ.get('SNS_SUBJECT')

app = Chalice(app_name='deepl-for-slack-lambda')
sc = WebClient(token=SLACK_BOT_TOKEN)
sns_client = boto3.client('sns')
lang = chalicelib.Lang()
ch_filter = chalicelib.Filter()

# Enable DEBUG logs.
# app.log.setLevel(logging.DEBUG)


@app.lambda_function(name='translate')
def translate_lambda_function(event, context):
    # debug
    app.log.debug('input data:{}'.format(event))

    # get data
    sns_msg = None
    sns_subject = None
    for record in event.get('Records'):
        sns_msg = record.get('Sns').get('Message')
        sns_subject = record.get('Sns').get('Subject')
        break

    if sns_subject is None or sns_subject != SNS_SUBJECT:
        app.log.error('Subject of SNS message did not match.')
        return

    if sns_msg is None:
        app.log.error('Not found SNS message value.')
        return

    sns_dict = json.loads(sns_msg)

    slack_channel = sns_dict.get('item').get('channel')
    if slack_channel is None:
        app.log.error('Not found slack channel value.')
        return

    # Is channel filter?
    if not ch_filter.is_allowed(slack_channel):
        app.log.error('It is not a permitted channel.')
        return

    slack_reaction = sns_dict.get('reaction')
    if slack_reaction is None:
        app.log.error('Not found slack reaction value.')
        return

    # Target language undetermined.
    lang_name = lang.get_lang(slack_reaction)
    # debug
    app.log.debug('language:{}'.format(lang_name))
    if lang_name is None:
        app.log.error('Not found language value.')
        return

    lang_deepl = lang.get_deepl(lang_name)
    if lang_deepl is None:
        app.log.error('Not found language deepl value.')
        return

    slack_ts = sns_dict.get('item').get('ts')
    if slack_ts is None:
        app.log.error('Not found slack ts value.')
        return

    # get slack message object
    slack_msg = get_slack_message(slack_channel, slack_ts)
    if slack_msg is None:
        app.log.error('Not found slack message value.')
        return

    slack_msg_text = slack_msg.get("text")
    if slack_msg is None:
        app.log.error('Not found slack message text value.')
        return

    # message translate by deepl
    tr_lang, tr_msg = translate_by_deepl(slack_msg_text, lang_deepl)

    # send message
    send_message_to_slack(slack_channel, slack_reaction,
                          slack_msg, tr_msg, tr_lang)

    return


@app.route('/')
def index():
    return create_response(200, "Responding with AWS chalice")


@app.route('/slack-events', methods=['POST'])
def receive_slack_events():
    request = app.current_request
    slack_data = request.json_body

    # debug
    app.log.debug('input data:{}'.format(slack_data))

    slack_token = slack_data.get('token')
    # It is not a request from slack.
    if slack_token is None or slack_token != SLACK_SIGNING_SECRET:
        return create_response(400, 'Request from not slack and can not accepted.')

    slack_type = slack_data.get('type')
    if slack_type is None:
        return create_response(400, 'Not found slack type value.')

    # respond to url_verification event
    # see also: https://api.slack.com/events/url_verification
    if slack_type == 'url_verification':
        return slack_data.get('challenge')

    slack_event = slack_data.get('event')
    if slack_event is None:
        return create_response(400, 'Not found slack event value.')

    slack_event_type = slack_event.get('type')
    if slack_event_type is None:
        return create_response(400, 'Not found slack event type value.')

    # Responds only to reaction_added
    if slack_event_type == 'reaction_added':
        slack_reaction = slack_event.get('reaction')
        if slack_reaction is None:
            return create_response(400, 'Not found slack reaction value.')

        # Only the emblem of the flag is permitted
        if slack_reaction.startswith('flag-'):
            # publish message
            response = sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject=SNS_SUBJECT,
                Message=json.dumps(slack_event)
            )
            # debug
            app.log.debug('sns response:{}'.format(response))
            return create_response(response.get('ResponseMetadata').get('HTTPStatusCode'), 'Successfully accepted request.')

    return create_response(204, 'Successfully accepted request.')


def create_response(code, msg):
    if code is None:
        code = 500

    body = {'code': code, 'message': msg}

    if not code in {200, 202, 204}:
        # error
        app.log.error(body)

    return Response(body=body, status_code=code)


def get_slack_message(channel, ts):
    # call conversations.replies API
    resp = sc.chat.postMessage(
        "conversations.replies",
        channel=channel,
        ts=ts,
        limit=1,
        inclusive=True
    )

    # debug
    app.log.debug('slack replies:{}'.format(resp))

    for msg in resp.get("messages"):
        return msg

    return None


def translate_by_deepl(msg, lang):
    url = "https://api.deepl.com/v2/translate"
    params = {"key": DEEPL_AUTH_KEY, "text": msg, "target_lang": lang}

    response = requests.get(url, params=params)

    # debug
    app.log.debug('deepl response:{}'.format(response))

    if response.json().get('code') != 200:
        raise create_response(400, 'Could not translate it.')

    tr_lang = response.json().get('detected_source_lang')
    tr_msg = '\n'.join(response.json().get('text'))

    return (tr_lang, tr_msg)


def send_message_to_slack(channel, reaction, slack_msg, tr_msg, tr_lang):
    attachments = None

    pretext = '_The message is translated in_ :{}: _({})_'.format(
        reaction, tr_lang)

    or_msg = slack_msg.get('text')
    attachments = [
        {
            "pretext": pretext,
            "text": tr_msg,
            "footer": or_msg,
            "mrkdwn_in": ["text", "pretext"]
        }
    ]

    ts = slack_msg.get('thread_ts')
    if ts is None:
        ts = slack_msg.get('ts')

    resp = sc.chat.postMessage(
        'chat.postMessage',
        channel=channel,
        attachments=attachments,
        as_user=False,
        username='DeepL translate Bot',
        thread_ts=ts
    )
    # debug
    app.log.debug('slack post response:{}'.format(resp))
