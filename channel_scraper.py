from requests_html import HTML, HTMLSession
from posts import PostItem
from datetime import datetime
from database import DataBase

def push_items(html, data_before, db):
    while data_before:
        try:
            divs = html.find("div.tgme_widget_message_wrap.js-widget_message_wrap")
            
            for div in divs:
                try:
                    post_id = div.find("a.tgme_widget_message_photo_wrap", first=True)
                    post_id = post_id.attrs["href"].split("/")[4].split("?")[0]

                    posted_date = div.find("time.time", first=True).attrs["datetime"]
                    posted_date = datetime.strptime(posted_date,"%Y-%m-%dT%H:%M:%S+00:00")
                    
                    description = div.find("div.tgme_widget_message_text.js-message_text", first=True)
                    category, exp_date, description = format_description(description.text)
                    category = "/"+category
                    if post_id and posted_date and exp_date and category:
                        db.add_item(category, PostItem(post_id=post_id, 
                                                posted_date=posted_date, 
                                                exp_date=exp_date,
                                                description=description
                                                )
                                )

                except Exception as e:
                    print("From channel_scraper.collect_items unable to parse post_id: ", e)

            r = session.get(f"{url}?before={data_before}")
            html = r.html
        except Exception as e:
            print("From channel_scraper.collect_items:", e)
            
        try:   
            data_before = html.find("a.tme_messages_more.js-messages_more", first=True).attrs["data-before"]
        except:
            if data_before==1:
                data_before = 0
            else:
                data_before = 1



def format_description(description):
    try:
        data = description.split(",")
        category = data[0]
        exp_date = data[1].split("/")
        exp_date = datetime(int(exp_date[2]), int(exp_date[1]), int(exp_date[0]))
        try:
            description = data[2]
        except:
            description = None
        return category, exp_date, description
    except Exception as e:
        print("From Channel_scraper.format_description: ", e)
        return None, None, None


session = HTMLSession()
url = "https://t.me/s/asdfmilomIIOdfmBItpwomvsmcslei"


def scrap(db):
    while True:
        try:
            r = session.get(url)
            html = r.html
            try:
                data_before = html.find("a.tme_messages_more.js-messages_more", first=True).attrs["data-before"]
            except:
                data_before = 1
            push_items(html, data_before, db)
            break
        except Exception as e:
            print("From channel_scraper", e)


def reload(time):
    db = DataBase()
    scrap(db)
    for category in DataBase.categories:
        matches = db.filter_by_date(category, time, exp_date=True)
        for match in matches:
            db.del_item(category, match)
    db.close()
    
    
