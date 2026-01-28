import shortenerLogic as sl

BASE_URL = "myshort.url/"

print("--- URL Shortener ---")
def main():
    try:
        conn = sl.createDb("url_shortener.db")
    except Exception as e:
        print(e)
        return

    try:
        while True:
            url = input("Enter a long URL to shorten or a short URL to expand. Type 'q' to quit: ")
            if url.lower() == 'q':
                break

            try:
                url, type_of_url = sl.checkURL(url, BASE_URL)

                if type_of_url == "short":
                    result = sl.lengthen(conn, url)
                    if result is None:
                        print("URL not found in the database.")
                    else:
                        print("Expanded URL:", result)
                        
                else:
                    result = sl.shorten(conn, url)
                    print("Shortened URL:", BASE_URL + result)

            except ValueError as ve:
                print("Invalid URL:", ve)
            except Exception as e:
                print(e)
    finally:
        conn.close()

if __name__ == "__main__":
    main()