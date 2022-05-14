# reacjilator-chalice
Translate Slack message with flag emoji(e.g. :jp: :us: :uk:) reaction. :smile:

## Description
This is implemented [slack/reacjilator](https://github.com/slackapi/reacjilator) with [aws/chalice](https://github.com/aws/chalice).

You can easily translate Slack messages with flag emojiflag emoji(e.g. :jp: :us: :uk:) reaction.

The translated messages is sent back to the thread, so it does not interfere with other conversations.

## Features
- It works easily as Slack bot.
- Even when using other translation API you can easily respond.
- Since it is a serverless configuration, it is easy to operate.


## Requirement
- Python 2.7.x
- Packages in use
	- aws/chalice: Python Serverless Microframework for AWS 
 		- https://github.com/aws/chalice
 	- requests/requests: Python HTTP Requests for Humans™ ✨🍰✨
 		- https://github.com/requests/requests
 	- slackapi/python-slackclient: Slack Developer Kit for Python
 		- https://github.com/slackapi/python-slackclient
 	- boto/boto3: AWS SDK for Python 
 		- https://github.com/boto/boto3
- Services in use
	- Amazon API Gateway 
		- https://aws.amazon.com/api-gateway/
	- AWS Lambda – Serverless Compute - Amazon Web Services
		- https://aws.amazon.com/lambda/
	- Amazon Simple Notification Service (SNS) | Event Notifications for Distributed Applications and Microservices | AWS 
		- https://aws.amazon.com/sns/
	- Slack API | Slack 
		- https://api.slack.com/
	- Translate API — Yandex Technologies 
		- https://tech.yandex.com/translate/

## Usage
Install this bot on "Slack".
If you react to the message with the emoji of the flag, this bot translate the original message and post it under the message thread.

### Demo
![2017-12-17 18_11_16](https://user-images.githubusercontent.com/6448792/34078201-01eec178-e359-11e7-8494-17d044371c5f.gif)


## Installation

1. Refer to the following document and install this bot in "Slack".

	- slackapi/reacjilator: A translation bot that translates a message when a user reacted with an emoji 🇨🇳 🇮🇹 🇹🇭 🇫🇷 🇯🇵 🇮🇳 🇺🇸 🇧🇬 🇹🇼 🇦🇪 🇰🇷
		- https://github.com/slackapi/reacjilator
	- [Japanese] Developing a bot for your workspace 翻訳ボットを作る!
		- https://www.slideshare.net/tomomi/japanese-developing-a-bot-for-your-workspace-82133038

1. Deploy bot using `aws/chalice`.

```sh
$ pip install chalice
$ chalice new-project reacjilator-chalice
$ cd reacjilator-chalice
$ git clone https://github.com/uchimanajet7/reacjilator-chalice
$ chalice deploy
```
Environment variables and so on need to be set individually.
And prepare the resources of AWS necessary for execution.

### Setting Example

1. Environment variables settings are done with `./chalice/config.json` file.

```sh
{
    "stages": {
        "dev": {
            "autogen_policy": true,
            "api_gateway_stage": "api"
        }
    },
    "environment_variables": {
        "SLACK_VERIFICATION_TOKEN": "YOUR_SLACK_VERIFICATION_TOKEN",
        "SLACK_TOKEN": "YOUR_SLACK_TOKEN",
        "YANDEX_API_KEY": "YOUR_YANDEX_API_KEY",
        "SNS_TOPIC_ARN": "YOUR_SNS_TOPIC_ARN",
        "SNS_SUBJECT": "slack event data"
    },
    "lambda_timeout": 180,
    "lambda_memory_size": 128,
    "version": "2.0",
    "app_name": "reacjilator"
}
```

- About setting items
	- `SLACK_VERIFICATION_TOKEN`: String
		- Specify the token to use "Slack API".
	- `SLACK_TOKEN`: String
		- Specify the token to use "Slack API".	- `YANDEX_API_KEY`: String
		- Specify the API key to use "Yandex API".
	- `SNS_TOPIC_ARN`: String
		- Specify ARN of "Amazon SNS".
	- `SNS_SUBJECT`: String
		- Specify the subject of SNS to be sent.


### When you want to use channel filter
If you want to limit the channels that respond to flag emoji reactions, you need to create a list of allowed channels.

1. Allowed channels settings are done with `./chalicelib/filter.json` file.

```sh
{
    "C1234567R": "random",
    "C823A567R": "dev"
}
```

Specify the format `channel ID`: `channel Name`.
Refer to the following for how to check the `channel ID`. 

- Slack | APIに使う「チャンネルID」を取得する方法 - Qiita 
	- https://qiita.com/Yinaura/items/bd28c7b9ef614696fb7e


## Author
[uchimanajet7](https://github.com/uchimanajet7)

- aws chaliceを使ってslackの翻訳botを作ってみた #aws #chalice #slack #bot #serverless - uchimanajet7のメモ 
	- http://uchimanajet7.hatenablog.com/entry/2017/12/18/102237

## Licence
[MIT License](https://github.com/uchimanajet7/reacjilator-chalice/blob/master/LICENSE)

