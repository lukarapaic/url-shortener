def expand(short_url):
    # TODO Implement the logic for the retrieval of the long URL
    return "Long URL for {}".format(short_url)

def shorten(long_url):
    # TODO Implement the URL shortening logic
    return "myshort.url/test123"

def checkURL(url):

    # TODO Check validity of URL, throw exception if invalid
    valid_flag = True # Placeholder for actual validation logic
    if not valid_flag:
        raise ValueError("The URL provided does not have a valid format.")
    if url.startswith("myshort.url/"):
        return "short"
    else:
        return "long"
    