import requests
from bs4 import BeautifulSoup
import os
import datetime


months = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
          'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12}

fi = open("input.txt", "r")
input_list = fi.read().split()
fi.close()
if(input_list[0].lower() == 'random'):
    os .mkdir('./Random')

    r = requests.get("http://explosm.net/rcg")
    site = BeautifulSoup(r.content, 'html5lib')
    a = site.find(attrs={'class': 'rcg-panels'})

    for i in range(1, 4):
        img = requests.get(a.contents[2*i - 1]['src'])
        f = open("./Random/frame{}.png".format(i), 'wb')
        f.write(img.content)
        f.close()
        print("Downloading random image%d" % i)

elif(input_list[0].lower() == 'latest'):
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
else:
    start_month = int(months[input_list[0].lower()])
    start_year = int(input_list[1])
    end_month = int(months[input_list[2].lower()])
    end_year = int(input_list[3])
    authors = input_list[4:]
    urls = []

    while(start_year <= end_year):

        urls.append("http://explosm.net/comics/archive/%s/%s" %
                    (start_year, start_month))

        if(start_year == end_year and start_month == end_month):
            break

        if(start_month == 12):
            start_month = 1
            start_year += 1
        else:
            start_month += 1

    for url in urls:
        done = False
        r = requests.get(url)
        site = BeautifulSoup(r.content, 'html5lib')
        for tag in site.find_all(id='comic-author'):
            info = tag.get_text().split()

            if(info[2] in authors):
                img_url = "http://explosm.net" + tag.parent.a['href']
                i = requests.get(img_url)
                folder_path = "./scrapped/{}/{}/".format(
                    info[0][:4], info[0][5:7])
                if(done == False):
                    os.makedirs(folder_path)
                    done = True
                image_name = "{}-{}.png".format(info[0], info[2])
                f = open(folder_path + image_name, 'wb')
                f.write(i.content)
                f.close()
                print("Downloading to %s" % (folder_path + image_name))
