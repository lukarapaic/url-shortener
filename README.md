#### url-shortener ####
A small Python tool designed to convert long URLs into manageable short URLs, or the inverse. The project focuses on creating a reliable system using SQLite for data persistance and a custom Base62 algorithm to handle the encoding and decoding of the URLs.

#### Features ####
- Base62 Encoding/Decoding: A custom implementation that maps database auto-increment IDs to a 62-character alphabet, ensuring short codes with no collision and a quick lookup. Uses an indexed column for long URL storage for a faster lookup of existing entries.

- Domain-Agnostic Storage: The database and the low-level functions are "unaware" of the short url domain name (eg.. 'myshort.url/'). This is completely handled at the high level, ensuring longevity and maintainability.

- Helpful input Normalisation: Uses urllib.parse and custom prefix handling to detect and fix the missing protocols in input URLs, or detect faulty URLs.

- A single entry point for both functionalities: Depending on the input content, the tool routes the request towards either shortening or expanding the URL

#### Tech Stack ####
- Language: Python 3.10.11
- Database: SQLite3
- Libraries: sqlite3, urllib.parse

#### Architecture and Design Choices ####
Split into 2 modules:
1. High level - main.py: Manages the user input and output, terminal loop, and deals with the BASE_URL constant, keeping it away from the low level.
2. Low level - shortenerLogic.py: Handles the SQLite transactions, the Base62 encoding and decoding, and the URL parsing.

This split ensured that the low level logic can be reused without any adjustments even if the high level completely changed.

- Base62: The ALPHABET_HASH dictionary is initialised at the module level, ensuring that the character lookups during the decoding are O(1). This makes the encoding effectively O(log62(n)), n being the length of the string.
- Database: Along the auto-increment ID, stores short URLs and their respective long URLs. I chose to store the shortURLs instead of calculating them every time mostly for the sake of visual clarity, as well as making sure the processing speed doesn't suffer at extremely high database entries if scaled enough. The long_url column has a unique index to ensure a binary tree lookup O(log(n)) rather than a linear O(n) one.

#### Installation & Setup ####
1. Clone the repository:
git clone https://github.com/lukarapaic/url-shortener.git
cd url-shortener

2. Run the application:
python main.py
# Note: The database file url_shortener.db will be created automatically in the root directory on the first run

#### Usage ####
1.a. To shorten an URL - input the url (eg. https://hithub.com)
1.b. To expand a shortened URL - input the short url starting with "myshort.url" (eg. myshort.url/1)
2. Receive a resulting URL in the terminal
3. Repeat the process or type 'q' to quit
