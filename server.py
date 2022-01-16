import main
import threading
from database import DataBase
import console
import channel_scraper as cs


DataBase().create_tables()
amount_of_posts = {'new_posts': None, 'all_posts': DataBase.count_posts_after_time()}

def server(bot):
    while True:
        try:
            messages = bot.get_updates()
            length = len(messages)

            if length > 0:
                first_update_id = messages[0]["update_id"]
                offset = first_update_id + length
                new_message = bot.get_updates(offset=offset, timeout=1000)
            else:
                new_message = bot.get_updates(timeout=1000)

            if len(new_message):
                threading.Thread(target=validation, args=(bot, new_message)).start()

        except Exception as e:
            print("From server.server", e)


def validation(bot, new_message):
    try:
        global amount_of_posts
        new_message = new_message[0]
        entities = new_message["message"]["entities"] # raises an error if the massage is from the channel

        if len(entities) and entities[0]["type"] == 'bot_command':
            console_handler(bot, new_message)
            
        else:
            chat_id = new_message["message"]["chat"]["id"]
            bot.send_message(chat_id, "እንደገና ይሞክሩ")
    except Exception as e:
        print("From server.validation", e)



def console_handler(bot, new_message):
    try:
        global amount_of_posts
        first_name = new_message["message"]["chat"]["first_name"]
        sent_text = new_message["message"]["text"]
        chat_id = new_message["message"]["chat"]["id"]
        time = new_message["message"]["date"]
        new_posts = amount_of_posts['new_posts']
        all_posts = amount_of_posts['all_posts']

        if sent_text == "/start":
            if not new_posts:
                new_posts = DataBase.count_posts_after_time(time)
                amount_of_posts['new_posts'] = new_posts

            bot.send_message(
                chat_id, console.start(
                    new_posts=new_posts,
                    all_posts=all_posts,
                    user_name=first_name
                )
            )
            

        elif sent_text == "/stop":
            bot.send_message(chat_id, console.stop(contact="@City_Board"))

        elif sent_text == "/reload_posts":
            cs.reload(time)
            amount_of_posts['all_posts'] = DataBase.count_posts_after_time()
            amount_of_posts['new_posts'] = DataBase.count_posts_after_time(time)
            bot.send_message(chat_id, "Data reloaded!")

        elif sent_text in ["/categories", "/menu"]:
            bot.send_message(chat_id, console.cmds[sent_text]())

        elif sent_text in list(console.descriptions.keys())[3:]:
            main.send_imgs(bot, time, chat_id, sent_text)

        else:
            bot.send_message(chat_id, "እንደገና ይሞክሩ")

    except Exception as e:
        print("From main.console_handler:", e)

