import requests


def hello(client, channel, args):
    """printa Hello World na tela"""
    return client.api_call('chat.postMessage', channel=channel,
                           text='Hello World', as_user=True)


def tempo(client, channel, args):
    """mostra o tempo atual dado uma cidade"""
    if not args:
        return client.api_call('chat.postMessage',
                               text='Preciso da cidade para saber o tempo..',
                               as_user=True, channel=channel)

    args = '+'.join(args)
    url = f'http://wttr.in/{args}?0T&lang=pt'
    response = requests.get(url)
    if not response.ok:
        return client.api_call('chat.postMessage',
                               text='Não foi possível obter o tempo '
                               'agora. Tente novamente mais tarde',
                               as_user=True, channel=channel)

    msg = f'```{response.text}```'
    return client.api_call('chat.postMessage', channel=channel, text=msg,
                           as_user=True)


def dolar(client, channel, args):
    """mostra a atual cotacao do dolar"""
    url = f'https://api.hgbrasil.com/finance/quotations'
    params = {
        'format': 'json',
        'key': '83da4431'
    }

    # https://api.hgbrasil.com/finance/quotations
    response = requests.get(url, params=params)
    if not response.ok:
        return client.api_call('chat.postMessage',
                               text='Não foi possível obter o valor do dólar '
                               'agora. Tente novamente mais tarde',
                               as_user=True, channel=channel)

    data = response.json()
    quotation = data['results']['currencies']['USD']['buy']
    msg = f'O valor do dólar atual é *{quotation}*'
    return client.api_call('chat.postMessage', channel=channel, text=msg,
                           as_user=True)
