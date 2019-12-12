import requests
from bs4 import BeautifulSoup
import os


def func():

    os .mkdir('./Random')
    r = requests.get("http://explosm.net/rcg")
    site = BeautifulSoup(r.content, 'html5lib')

    # print()
    a = site.find(attrs={'class': 'rcg-panels'})

    for i in range(1, 4):
        img = requests.get(a.contents[2*i - 1]['src'])
        f = open("./Random/frame{}.png".format(i), 'wb')
        f.write(img.content)
        f.close()
        print("printing random image%d" % i)
