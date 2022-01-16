import console
from datetime import datetime
from database import DataBase
from configparser import ConfigParser

if __name__ == "__main__":
    import telegram
    import server



def send_imgs(bot, date, chat_id, category):
    try:
        config = ConfigParser()
        config.read("files/config.ini")
        channel_addr = config["Telegram"]["entity"]

        if category == "/all_ads":
            photo_found = all_or_new_imgs(bot, chat_id, channel_addr)
        elif category == "/new_ads":
            photo_found = all_or_new_imgs(bot, chat_id, channel_addr, date)
        else:
            photo_found = category_img(bot, chat_id, category, channel_addr)

        if not photo_found:
            bot.send_message(chat_id, "ለጊዜው በዚህ ዘርፍ ማስታዎቂያ አልተለጠፈም")

        bot.send_message(chat_id, console.prompt_after_img(True))
    except Exception as e:
        print("From main.send_image:", e)


def all_or_new_imgs(bot, chat_id, channel_addr, date=datetime.fromtimestamp(2667600)):
    try:
        db = DataBase()
        photo_found = False
        for category in console.categories_list:
            items_after_date = db.filter_by_date(category, date, posted_date=True, before=False)
            for item in items_after_date:
                caption = item.description if item.description else console.descriptions[category]

                bot.send_photo(chat_id, channel_addr+str(item.post_id), 
                    caption=caption)

                photo_found = True
        
        db.close()
        return photo_found
    except Exception as e:
        db.close()
        print("From all_or_new_imgs:", e)


def category_img(bot, chat_id, category, channel_addr):
    try:
        db = DataBase()
        photo_found = False
        items_categoy = db.filter_by_date(category, datetime.fromtimestamp(2667600), posted_date=True, before=False)
        db.close()
        for item in items_categoy:
                caption = item.description if item.description else console.descriptions[category]

                bot.send_photo(chat_id, channel_addr+str(item.post_id), 
                    caption=caption)

                photo_found = True

        return photo_found
    except Exception as e:
        print("From category_img:", e)


def main():
    config = ConfigParser()
    config.read("files/config.ini")

    token = config["Telegram"]["token"]
    base_url = config["Telegram"]["base_url"]

    bot = telegram.Bot(token, base_url)
    server.server(bot)


if __name__ == "__main__":
    main()
