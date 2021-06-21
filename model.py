import sqlite3, os

BASE_DIR = os.getcwd()

class Image:
    def __init__(self, account_name: str = None, image: bytes = None):
        self.account_name = account_name
        self.image = image

    def __repr__(self):
        return f'Image for {self.account_name} account'

    def commit(self):
        if (self.account_name and self.image):
            db_path = BASE_DIR + '/images.db'
            if (os.path.isfile(db_path)):
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute("SELECT id FROM accounts WHERE account_name == (?)", [self.account_name])
                idx = c.fetchone()
                if (not idx):
                    c.execute("INSERT INTO accounts (account_name) VALUES (?)", [self.account_name])
                    idx = c.lastrowid
                else:
                    idx = idx[0]
                c.execute("INSERT INTO images (image_account, image) VALUES (?, ?)", [idx, self.image])
                conn.commit()
                conn.close()
            else:
                raise FileNotFoundError("Please created database first: create_database()")
        else:
            raise ValueError("Please set account_name and image parameters")
    
    @staticmethod
    def output(account_name: str, dir_path: str):
        db_path = BASE_DIR + '/images.db'
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""
            SELECT image FROM accounts, images
            WHERE account_name == ? AND accounts.id == images.image_account
        """, [account_name])
        images = c.fetchall()
        if (images):
            images = [e[0] for e in images]
            for idx, image in enumerate(images):
                with open(f'{dir_path}/{idx}.jpeg', 'wb') as f:
                    f.write(image)
        else:
            print("No images were found in the database, try adding this account")
        conn.close()

    @staticmethod
    def create_database():
        conn = sqlite3.connect(BASE_DIR + '/images.db')
        conn.execute("PRAGMA foreign_keys = 1")
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY,
                created TEXT DEFAULT CURRENT_TIMESTAMP,
                account_name TEXT NOT NULL
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY,
                created TEXT DEFAULT CURRENT_TIMESTAMP,
                image_account INTEGER NOT NULL,
                image BLOB NOT NULL,
                FOREIGN KEY(image_account) REFERENCES accounts(id)
            )
        """)
        conn.commit()
        conn.close()