import json
import requests
import re

from bs4 import BeautifulSoup

with open('settings.json', 'r') as f:
    settings = json.load(f)
    BOT_TOKEN = settings['bot_token']
    DEBUG_CHAT = settings.get('debug_chat')


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
        try:
            print("Fetching entry {}".format(entry['name']))
            response = requests.get(entry['url'])
            soup = BeautifulSoup(response.content, 'html.parser')
            new_links = []
            new_parsed = []
            if entry['url'] not in parsed:
                parsed[entry['url']] = []
            already_parsed_urls = [p['url'] for p in parsed[entry['url']]]
            counter = 0

            for link in soup.select("div.main div.list_mode_thumb a"):
                if not link.select_one('.desc_flex'):
                    continue
                title = " ".join([
                    _part for _part in link.select_one('.ad-details-left').getText().split()
                ])
                link_parsed = link['href'].split('?')[0]
                new_parsed.append({'title': title, 'url': link_parsed})
                # Only allow "new" status for links within the 5 first on the page
                # (A new link can appear from page 2 if one is deleted from page 1)
                if link_parsed not in already_parsed_urls and counter < 5:
                    if entry.get('title_must_contain', None):
                        if not re.search(entry['title_must_contain'], title, re.IGNORECASE):
                            continue

                    if entry.get('page_must_not_contain', None):
                        page_text = requests.get(link_parsed).text
                        if re.search(entry['page_must_not_contain'], page_text, re.IGNORECASE):
                            continue

                    new_links.append({'title': title, 'url': link_parsed})
                counter += 1

            # Add new ones to parsed
            for value in new_parsed.items():
                if value['url'] not in already_parsed_urls:
                    parsed[entry['url']].insert(0, value)
            # Keep this reasonable
            parsed[entry['url']] = parsed[entry['url']][:100]

            for new_link in new_links:
                print("Found new links: {}".format(new_link))
                send_telegram("{}, {}".format(new_link['title'], new_link['url']), entry['chatId'])
        except Exception as e:
            print("Error: {}".format(e))
            send_telegram("Error: {}".format(e), DEBUG_CHAT)

    with open('parsed.json', 'w') as f:
        json.dump(parsed, f, indent=4)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        send_telegram("Error in main: {}".format(e), DEBUG_CHAT)
