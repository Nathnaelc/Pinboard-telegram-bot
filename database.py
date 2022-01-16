from console import categories_list
import sqlite3
from datetime import datetime
from posts import PostItem

class DataBase:
    categories = categories_list

    def __init__(self, path="files/posts.db"):
        
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        with self.conn:
            for category in self.categories:
                self.cursor.execute(f""" CREATE TABLE IF NOT EXISTS {category[1:]} (
                    post_id INTEGER NOT NULL PRIMARY KEY,
                    posted_date INTEGER NOT NULL,
                    exp_date INTEGER NOT NULL,
                    description TEXT DEFAULT NULL
                ); """)

    def add_item(self, category, item):
        with self.conn:
            self.cursor.execute(f"SELECT * FROM {category[1:]} WHERE post_id = :post_id;", \
                {"post_id":item.post_id})

            if (self.cursor.fetchone()):
                print("Item exists!")
            else:
                self.cursor.execute(f"INSERT INTO {category[1:]} VALUES \
                    (:post_id, :posted_date, :exp_date, :description);",
                        {
                            'post_id': item.post_id,
                            'posted_date': item.posted_date.timestamp(),
                            'exp_date': item.exp_date.timestamp(),
                            'description': item.description
                        }
                )
                

    def del_item(self, category, item):
        with self.conn:
            self.cursor.execute(f"DELETE FROM {category[1:]} WHERE post_id = :post_id;", \
                {"post_id": item.post_id})


    def filter_by_date(self, category, time, exp_date=False, posted_date=False, before=True):
        matches = []
        date = datetime(time.year, time.month, time.day, 0, 0)
        date = date.timestamp()
        if posted_date:
            if before:
                self.cursor.execute(f"SELECT * FROM {category[1:]} WHERE posted_date < :date", {'date': date})
            else:
                self.cursor.execute(f"SELECT * FROM {category[1:]} WHERE posted_date >= :date", {'date': date})
        elif exp_date:
            if before:
                self.cursor.execute(f"SELECT * FROM {category[1:]} WHERE exp_date < :date", {'date': date})
            else:
                self.cursor.execute(f"SELECT * FROM {category[1:]} WHERE exp_date >= :date", {'date': date})
        if exp_date or posted_date:
            data = self.cursor.fetchall()
            for item in data:
                matches.append(PostItem(item[0], item[1], item[2], item[3]))
        return matches

    @classmethod
    def count_posts_after_time(cls, time=datetime.fromtimestamp(2667600)):
        amount = 0
        database = cls()
        for category in cls.categories:
            amount += len(database.filter_by_date(category, time, posted_date=True, before=False))
        return amount

    def close(self):
        self.conn.close()


