from marvinbot.utils import get_message, trim_accents
from marvinbot.handlers import CommonFilters, CommandHandler, MessageHandler
from urllib import parse
import logging
import json
import requests

log = logging.getLogger(__name__)
adapter = None


def fetch_definitions(terms):
    base_url = 'http://api.urbandictionary.com/v0/define?term={terms}'
    terms = parse.quote_plus(terms)
    response = requests.get(base_url.format(terms=terms))
    data = response.json()
    return data


def strip_markdown(str):
    special = ['*', '`', '_', '[', ']', '{', '}']
    for c in special:
        if c in str:
            str = str.replace(c, '')
    return str


def on_ud_command(update, *args, **kwargs):
    log.info('Urban Dictionary command caught')
    message = get_message(update)
    terms = " ".join(kwargs.get('terms'))

    if len(terms) == 0:
        adapter.bot.sendMessage(chat_id=message.chat_id, text="❌ Term or phrase is too short.")
        return

    verbose = kwargs.get('verbose')
    no_examples = kwargs.get('no_examples')
    n = int(kwargs.get('n'))
    n = n if n > 0 and n <= 5 else 1

    data = fetch_definitions(terms)
    # adapter.bot.sendMessage(chat_id=message.chat_id,
    #                         text=json.dumps(data, indent=4, sort_keys=True))

    def_list = data.get("list")
    tags_list = data.get("tags")
    if len(def_list) == 0:
        adapter.bot.sendMessage(
            chat_id=message.chat_id,
            text="❌ No definitions found.")
        return

    responses = []
    for item in def_list[0:n]:
        item["definition"] = strip_markdown(item.get("definition"))
        d = dict(item)
        response = "📖 *{word}*: {definition}"
        if no_examples is False and item.get("example"):
            response += "\n\n_e.g. {example}_"
        if verbose is True:
            response += "\n\n👤 {author}\n👍{thumbs_up} / 👎 {thumbs_down}"
            if len(tags_list) > 0:
                tags = map(lambda tag: "#{}".format(tag), set(tags_list))
                response += "\n{}".format(" ".join(tags))
        responses.append(response.format(**d))

    adapter.bot.sendMessage(
        chat_id=message.chat_id,
        text="\n\n".join(responses),
        parse_mode="Markdown")


def setup(new_adapter):
    global adapter
    adapter = new_adapter

    adapter.add_handler(CommandHandler('ud', on_ud_command, command_description='Allows the user to find terms or phrases on Urban Dictionary.')
                        .add_argument('--n', help='Number of results', default='1')
                        .add_argument('--no-examples', help='No examples', action='store_true')
                        .add_argument('--verbose', help='Increase verbosity', action='store_true')
                        .add_argument('terms', nargs='*', help='Terms or phrase'))
