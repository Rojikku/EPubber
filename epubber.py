#!/usr/bin/python

#Imports
import urllib3
from ebooklib import epub
from pyquery import PyQuery as pq
from array import array
import sys
import argparse
import os.path
import json

#Vars
bk= epub.EpubBook()
X = 0
Listed = 0
Indexing = 0
WorkingList = 0
Contin = 1
SPINE = ['nav']
MagicalIndex = []
CacheName = "cache"
cache = []
if os.path.isfile(CacheName):
    WorkingList = 1
    with open(CacheName, 'r') as f:
        cache = json.load(f)
listSize = len(cache)
listCount = listSize - 1
#Functions

def Chapter(your_url, CH):
    d = pq(GetHTML(your_url))
    page = d(Query).html()
    c1 = epub.EpubHtml(title="Chapter "+N, file_name=CH+'.xhtml', lang='en')
    c1.content = page
    SPINE.append(c1)
    print(c1)
    bk.add_item(c1)
    return
def WPubCache():
    with open(CacheName, 'w') as f:
        json.dump(cache, f)

    return
def GetHTML(This):
    user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) ..'}
    http = urllib3.PoolManager(10, headers=user_agent)
    r1 = http.urlopen('GET', This)
    return r1.data

def Index():
    Links = ["end", ]
    d = pq(GetHTML(Context))
    if Indexing == 1:
        print("Printing selected code")
        print(d(ContextRule))
        print("Printing valid links")
    for link in d(ContextRule):
        if Indexing == 1:
            print(link.attrib["href"])
        if Context == "http://japtem.com/projects/magis-grandson-toc/":
            MagicalIndex.append("http://japtem.com/" + link.attrib["href"])
        else:
            MagicalIndex.append(link.attrib["href"])
def PageDump(your_url):
    d = pq(GetHTML(your_url))
    page = d(Query).html()
    print(page)
    return

#Arguement Parsing
parser = argparse.ArgumentParser(description='Epubber uses jQuery to select and generate Epub files from webpages with a standardized format.')
parser.add_argument('--mode', nargs='?', const="b", default=False)
args = parser.parse_args()

    
#Core
Context = input("Put in the index/ToC/context link: ")


if args.mode:
    if args.mode.lower() == "index":
        ContextRule = input("Set the Context (Table of Contents) jQuery String Selector: ")
        Indexing = 1
        Index()
        print(MagicalIndex)
    elif args.mode.lower() == "page":
        print("Using Context link as page link")
        Query = input("Set the Query (Chapter) jQuery String Selector: ")
        PageDump(Context)
    else:
        print("Mode Invalid. Valid modes are: index, page")
    sys.exit()

#Checks Database for context link
if WorkingList == 1:
    print("Cache Found, searching " + str(listSize) + " entries...")
    for i in range(0, listSize):
        print("Checking Entry: " + str(i))
        if cache[i][0] == Context:
            print("Found!")
            Listed = i+1      
            break
        
if Listed != 0:
    print("Listing confirmed.")
    Listed = Listed-1
    a = cache[Listed]
    Context = a[0]
    Title = a[1]
    ContextRule = a[2]
    Query = a[3]
    
else:
    Title = input("Set Book Name: ")
    ContextRule = input("Set the Context (Table of Contents) jQuery String Selector: ")
    Query = input("Set the Query (Chapter) jQuery String Selector: ")
    cache.append([])
    a = cache[listSize]
    a.append(Context)
    a.append(Title)
    a.append(ContextRule)
    a.append(Query)

for row in cache:
    print(row)

WPubCache()
Index()


for my_url in MagicalIndex:
    X += 1
    N = str(X)
    Ch = "c"+N
    Chapter(my_url, Ch)
    #SPINE+=", "+Ch
##    my_url = input("Download maybe successful! I dunno! I didn't make error checking! Give me another link, or say 0 for done! ")
##    if my_url == "0":
##        print(X)
##        for i in range(1, X+1):
##            List += "c" + str(i) + ", "
##            Links += "c" + str(i) + ".xhtml, "
##            
##        print(List)
##        bk.toc = (epub.Link(Links),
##                  (epub.Section('Languages'),
##                   (List)),
##                   )

#Metadata
bk.set_identifier(Title)
Title = Title+" CH 1-"+N
bk.set_title(Title)
bk.set_language('en')

bk.add_author("Kami Produced")

style = '''
body, table {
    margin-left: 100px;
    margin-right: 100px;
    color: #FF9898 !important;
    background: black !important;
    background-color: black !important;
    font-size: 28px !important;
    font: 28px Times New Roman !important;
    font-weight: 400 !important;
}
'''
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
bk.add_item(nav_css)

bk.spine=SPINE

epub.write_epub(Title+'.epub', bk, {})
