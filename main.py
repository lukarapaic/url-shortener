import shortenerLogic as sl

print("--- URL Shortener ---")

while True:
    url = input("Enter a long URL to shorten or a short URL to expand. Type 'q' to quit: ")
    if url.lower() == 'q':
        break

    try:
        if sl.checkURL(url) == "short":
            result = sl.expand(url)
            print ("Expanded URL:", result)
        else:
            result = sl.shorten(url)
            print ("Shortened URL:", result)
    except ValueError as ve:
        print("Invalid URL:", ve)
    except Exception as e:
        print("Filler error ", e)