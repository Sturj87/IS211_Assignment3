import argparse
import datetime
import csv
import io
import re
import urllib.request


def download_data(url):
    """
    Reads data from a URL and returns the data as a string

    :param url:
    :return: the content of the URL
    """
    # read the URL
    with urllib.request.urlopen(url) as response:
        response = response.read().decode('utf-8')

    # return the data
    return response


def main(url):

    # Determine the number of Images within the file

    regex_images = "([^\\s]+(\\.(?i)(jpe?g|png|gif|))$)"
    p = re.compile(regex_images)

    url_data = download_data(url)
    csv_data = csv.reader(io.StringIO(url_data))
    count_images = 0
    count_files = 0
    for row in csv_data:
        count_files += 1
        if re.search(p, row[0]):
            count_images += 1
    pt = count_images / count_files
    percentage = "{:.0%}".format(pt)
    print("Image requests account for", percentage, "of all requests")

    # Determine the most searched browser in the file

    Firefox = 0
    Chrome = 0
    Internet_Explorer = 0
    Safari = 0
    csv_browsers = {}
    url_data = download_data(url)
    csv_data = csv.reader(io.StringIO(url_data))
    for row in csv_data:
        if re.search('Firefox', row[2]):
            Firefox += 1
        elif re.search('Chrome', row[2]):
            Chrome += 1
        elif re.search('Internet Explorer', row[2]):
            Internet_Explorer += 1
        elif re.search('Safari', row[2]):
            Safari += 1
    csv_browsers["Firefox"] = Firefox
    csv_browsers["Chrome"] = Chrome
    csv_browsers["Internet Explorer"] = Internet_Explorer
    csv_browsers["Safari"] = Safari
    popular = max(csv_browsers, key=csv_browsers.get)
    print(f"The most popular browser is {popular}"
          f" with {csv_browsers[popular]} hits.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)

