from urllib import request
from re import findall


def scrape_page(url: str, search: str):
    request_page = request.Request(url)
    response = request.urlopen(request_page)
    response_data = str(response.read())

    found = findall(search, response_data)

    return found


def main():
    url = "https://docs.splunk.com/Documentation/Splunk/8.2.6/DistSearch/SHCarchitecture"
    search = r'<p>(.*?)</p>'

    collection_found = scrape_page(url, search)

    #for found in collection_found:
    #    print(found)


if __name__ == "__main__":
    # main()
    for i in range(20):
        main()
