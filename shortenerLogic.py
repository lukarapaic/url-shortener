import sqlite3
from urllib.parse import urlparse

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
ALPHABET_HASH = {char: i for i, char in enumerate(ALPHABET)}
BASE_NUM = len(ALPHABET)

# Creates the database and the table if they don't already exist
# In theory we don't need to store short_url in the table, we can calculate it from the id every time
# however, storing it makes retrieval faster, especially as the codes get longer.
def createDb(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Error connecting to database: {e}")
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS url_mapping (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                long_url TEXT NOT NULL,
                short_url TEXT
            )
        ''')
        cursor.execute('''
            CREATE UNIQUE INDEX IF NOT EXISTS idx_long_url ON url_mapping (long_url)
        ''')
        conn.commit()
        return conn
    except sqlite3.Error as e:
        conn.close()
        raise sqlite3.Error(f"Error creating the table in the database: {e}")

# Encodes a number into a base62 string
def toBase62(num):
    if num == 0:
        code = str(ALPHABET[0])
    else:
        code_list = []
        while num > 0:
            num, rem = divmod(num, BASE_NUM)
            code_list.append(ALPHABET[rem])
        code = ''.join(reversed(code_list))

    return code

# Decodes a base62 string into a number
def fromBase62(s):
    num = 0

    for char in s:
        num = num * BASE_NUM + ALPHABET_HASH[char]
    return num

# The logic for retrieving the short URL from database based on the long URL
def getShortUrl(conn, long_url):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT short_url FROM url_mapping WHERE long_url = ?", (long_url,))

        row = cursor.fetchone()

        if row:
            return row[0]
        else:
            return None
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Error retrieving short URL: {e}")

# The logic for inserting a new URL mapping into the database
def insertUrlMapping(conn, long_url):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO url_mapping (long_url) VALUES (?)", (long_url,))

        row_id = cursor.lastrowid

        short_url = toBase62(row_id)

        cursor.execute("UPDATE url_mapping SET short_url = ? WHERE id = ?", (short_url, row_id))

        conn.commit()
        return short_url
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Error inserting URL mapping: {e}")

# The logic for retrieving the long URL from database based on the short URL
def getLongUrl(conn, short_url):
    try:
        cursor = conn.cursor()
        try:
            ind = fromBase62(short_url)
        except Exception as e:
            raise ValueError ("Short URL format is not base62")

        cursor.execute("SELECT long_url FROM url_mapping WHERE id = ?", (ind,))

        row = cursor.fetchone()

        if row:
            return row[0]
        else:
            return None
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Error retrieving long URL: {e}")
    
# If the short URL exists, returns its long URL. Otherwise, returns None.    
def lengthen(conn, short_url):
    long_url = getLongUrl(conn, short_url)
    if long_url:
        return long_url
    else:
        return None

# If the long URL already exists, returns the existing short URL. Otherwise, creates a new db entry and returns the new short URL.
def shorten(conn, long_url):
    short_url = getShortUrl(conn, long_url)
    if short_url:
        return short_url
    else:
        return insertUrlMapping(conn, long_url)

# Checks if the URL is short or long, and raises an error if it's invalid
def checkURL(url, base_url):    
    if url.startswith(base_url) or url.startswith("http://" + base_url) or url.startswith("https://" + base_url):

        url = url.removeprefix("https://").removeprefix("http://").removeprefix(base_url)
        if url == "":
            raise ValueError("The short URL provided does not have a short code.")
        # Not checking for base62 format here, it will be checked in getLongUrl() through fromBase62() later to avoid decoding twice
        return url, "short"
    
    else:
        
        if not (url.startswith("http://") or url.startswith("https://")):
            url = "https://" + url

        parsed_url = urlparse(url)

        if "." not in parsed_url.netloc:
            raise ValueError("The URL provided does not have a valid format.")
        return url,"long"
    