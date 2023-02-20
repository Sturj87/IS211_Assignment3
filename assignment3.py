import argparse
import datetime
import csv
import io
import re
import urllib.request


# Saar T. IS211 CUNYSPS SPRING 2023
# --url http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv


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

    # Determine the  browser with the highest hits

    csv_browsers = {}
    Firefox = Chrome = MSIE = Safari = 0
    url_data = download_data(url)
    csv_data = csv.reader(io.StringIO(url_data))
    for row in csv_data:
        if re.search('Firefox', row[2]):
            Firefox += 1
        elif re.search('Chrome', row[2]):
            Chrome += 1
        elif re.search('MSIE', row[2]):
            MSIE += 1
        elif re.search('Safari', row[2]):
            Safari += 1
    csv_browsers["Firefox"] = Firefox
    csv_browsers["Chrome"] = Chrome
    csv_browsers["MSIE"] = MSIE
    csv_browsers["Safari"] = Safari
    highest_hits = max(csv_browsers, key=csv_browsers.get)
    print("The browser with the highest hits is", highest_hits,
          "with", csv_browsers[highest_hits], "hits")

    # Output a list of hours of the day sorted by the total number of hits that occurred in that hour
    # EXTRA CREDIT
    hour_list = []
    url_data = download_data(url)
    csv_data = csv.reader(io.StringIO(url_data))
    for row in csv_data:
        time_format = '%Y-%m-%d %H:%M:%S'
        hour_time = datetime.datetime.strptime(row[1], time_format)
        hour = hour_time.hour
        hour_list.append(hour)
    print("First hour with", hour_list.count(0), "hits")
    print("Second hour with", hour_list.count(1), "hits")
    print("Third hour with", hour_list.count(2), "hits")
    print("Fourth hour with", hour_list.count(3), "hits")
    print("Fifth hour with", hour_list.count(4), "hits")
    print("Sixth hour with", hour_list.count(5), "hits")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)


