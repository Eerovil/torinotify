import json
import requests

from bs4 import BeautifulSoup

with open('settings.json', 'r') as f:
    settings = json.load(f)
    BOT_TOKEN = settings['bot_token']


def send_telegram(bot_message, chat_id):
    send_text = (
        'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + chat_id +
        '&text=' + bot_message
    )

    response = requests.get(send_text)

    print(response.content)
    print(bot_message)


def main():
    with open('entries.json', 'r') as f:
        entries = json.load(f)['entries']
    try:
        with open('parsed.json', 'r') as f:
            parsed = json.load(f)
    except FileNotFoundError:
        parsed = {}

    for entry in entries:
        print("Fetching entry {}".format(entry['name']))
        response = requests.get(entry['url'])
        soup = BeautifulSoup(response.content, 'html.parser')
        new_links = []
        if entry['url'] not in parsed:
            parsed[entry['url']] = []

        for link in soup.select("div.main div.list_mode_thumb a"):
            if not link.select_one('.desc_flex'):
                continue
            title = " ".join([
                _part for _part in link.select_one('.ad-details-left').getText().split()
            ])
            link_parsed = link['href'].split('?')[0]
            if parsed[entry['url']] and link_parsed == parsed[entry['url']][0]['url']:
                break
            else:
                new_links.append({'title': title, 'url': link_parsed})

        if entry['url'] not in parsed:
            parsed[entry['url']] = []
        parsed[entry['url']] = new_links + parsed[entry['url']]
        parsed[entry['url']] = parsed[entry['url']][:10]

        for new_link in new_links:
            print("Found new links: {}".format(new_link))
            send_telegram("{}, {}".format(new_link['title'], new_link['url']), entry['chatId'])

    with open('parsed.json', 'w') as f:
        json.dump(parsed, f, indent=4)


if __name__ == '__main__':
    main()
