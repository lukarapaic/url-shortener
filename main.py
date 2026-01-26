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
                if sl.checkURL(url) == "short":
                    result = sl.lengthen(conn,url)
                    print ("Expanded URL:", result)
                else:
                    result = sl.shorten(conn, url, BASE_URL)
                    print ("Shortened URL:", result)
            except ValueError as ve:
                print("Invalid URL:", ve)
            except Exception as e:
                print(e)
    finally:
        conn.close()

if __name__ == "__main__":
    main()