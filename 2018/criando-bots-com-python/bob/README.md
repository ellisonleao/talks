# Bob

A simple Slack chatbot

## Installing

### Prerequisites

- Python 3.6+
- You are an Admin of a Slack Organization
- You generated a [Slack API Token for your bot](https://my.slack.com/services/new/bot)

### Steps

1. Clone the repo

```
git clone https://github.com/ellisonleao/bob.git
```

2. Install the dependencies

```
cd bob
pip install -r requirements.txt
```

3. Run the code

```
SLACK_TOKEN=XXXXXX python run.py
```

### Implementing your own commands

1. Open `commands.py` file
2. create any func passing `(client, channel, args)` as arguments
3. Implement it.
4. Save and restart the bot.
5. Profit!
