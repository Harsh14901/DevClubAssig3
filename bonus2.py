import requests
from bs4 import BeautifulSoup
import os
import datetime


def func():

    fi = open("input.txt", "r")
    n = int(fi.read().split()[1])
    fi.close()
    if(n > 0):
        os.mkdir('latest')
    else:
        print('no file to scrape')
        exit(0)
    month = datetime.date.today().month
    year = datetime.date.today().year
    while(n > 0):
        url = "http://explosm.net/comics/archive/%s/%s" % (year, month)

        r = requests.get(url)
        site = BeautifulSoup(r.content, 'html5lib')
        for tag in site.find_all(id='comic-author'):
            info = tag.get_text().split()
            img_url = "http://explosm.net" + tag.parent.a['href']
            i = requests.get(img_url)
            f = open("./latest/{}-{}.png".format(info[0], info[2]), 'wb')
            f.write(i.content)
            f.close()
            n -= 1
            if(n <= 0):
                break
            print("Downloading to " +
                  "./latest/{}-{}.png".format(info[0], info[2]))

        if(month == 1):
            month = 12
            year -= 1
        else:
            month -= 1
