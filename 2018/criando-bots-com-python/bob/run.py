import os
import sys
import time
import inspect

from slackclient import SlackClient

# importando todos os comandos implementados
import commands


BOT_NAME = 'bob'
SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
# RTM delay time
DELAY = 1


def _default_message(client, channel):
    """"mensagem padrao de erro de comando"""
    funcs = inspect.getmembers(commands, inspect.isfunction)
    if not funcs:
        msg = 'No momento não tenho nenhuma função implementada'
    else:
        msg = """
    No momento não consigo entender esse comando. Estou apenas com esses:
    """
        # listando dinamicamente as funcoes do modulo commands
        for func in funcs:
            msg += f'- *{func[0]}*: {func[1].__doc__}\n'

    return client.api_call('chat.postMessage', text=msg, channel=channel,
                           as_user=True)


def _get_bot_id(client):
    """obtendo o ID do bot"""
    call = client.api_call('users.list')
    if not call.get('ok'):
        sys.exit('Could not get Bot ID')

    users = call.get('members')
    for user in users:
        if 'name' in user and user.get('name') == BOT_NAME:
            return user['id']
    sys.exit('Could not get Bot ID')


def _parse_and_handle_command(client, bot_id):
    """funcao que trata o stream e chama o comando especifico"""
    # le o proximo batch de streams
    stream = client.rtm_read()
    if not stream:
        return

    at_bot = f'<@{bot_id}>'

    for msg in stream:
        print(msg)
        # msgs podem vir vazias
        if not msg:
            continue

        if 'text' in msg and at_bot in msg['text']:
            # separamos a msg do mention para o bot
            input_ = msg['text'].split(at_bot)[1]

            # se nao temos msg, podemos pular
            if not input_:
                continue

            # separamos o comando dos parametros
            splitted = input_.split()
            command = splitted[0]
            args = []
            if len(splitted) > 0:
                args = splitted[1:]

            # checamos se existe o comando nas funcoes de comando
            func = getattr(commands, command.lower(), False)
            if func and callable(func):
                return func(client, msg['channel'], args)
            else:
                _default_message(client, msg['channel'])


def main():
    if not SLACK_TOKEN:
        sys.exit('SLACK_TOKEN missing. Quitting..')

    client = SlackClient(SLACK_TOKEN)
    bot_id = _get_bot_id(client)

    if not client.rtm_connect():
        sys.exit('Failed to connect on Slack RTM API')

    print('Connected to Slack RTM. Reading Events..')
    while True:
        # pegar proximo stream
        _parse_and_handle_command(client, bot_id)
        time.sleep(DELAY)


if __name__ == "__main__":
    main()
