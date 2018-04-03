import argparse
import requests
import csv
from time import sleep
from bs4 import BeautifulSoup

def get_url_data(url):
    """
    Extracts data from a single URL.
    Gets number of tags from source code.

    Returns list: [url,rescode,img,figure,video,h1,h2,h3,strong]

    Arguments:
    - url: url to parse
    """
    data = [url]

    try: 
        r = requests.get(url)
        data.append(str(r.status_code))
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'lxml')
            data.append(str(len(soup.find_all('img'))))
            data.append(str(len(soup.find_all('figure'))))
            data.append(str(len(soup.find_all('video'))))
            data.append(str(len(soup.find_all('h1'))))
            data.append(str(len(soup.find_all('h2'))))
            data.append(str(len(soup.find_all('h3'))))
            data.append(str(len(soup.find_all('strong'))))

    except ConnectionResetError:
        data.append('error')

    return data

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--url',
            type=str, help='Single URL')
    group.add_argument('-f', '--file', 
            type=str, help='URLs file')
    parser.add_argument('-o', '--output', required=False, default='output.csv',
            type=str, help='Output file for file mode')
    parser.add_argument('-d', '--delay', required=False, default=1, 
            type=float, help='Seconds to wait between requests')

    args = parser.parse_args()

    if args.file:
        with open(args.file) as inputfile:
            with open(args.output, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile,delimiter=";")
                writer.writerow(['url','rescode','img','figure','video','h1','h2','h3','strong'])
                i = 1
                for url in inputfile.read().splitlines():
                    print("({}) {}".format(i,url))
                    writer.writerow(get_url_data(url))
                    i += 1
                    sleep(args.delay) 
                csvfile.close()
            inputfile.close()

    if args.url:
        print(";".join(['url','rescode','img','figure','video','h1','h2','h3','strong']))
        print(";".join(get_url_data(args.url)))

