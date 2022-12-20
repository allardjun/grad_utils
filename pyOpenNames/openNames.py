import os
import sys
from bs4 import BeautifulSoup


#os.system("open -a Google\ Chrome \"http://cbc.ca/news\" ")

if len(sys.argv)>1:
        suffix = sys.argv[1]
else:
    suffix = '_DomPhD'

the_html = open('Slate Reader' + suffix + '.html','r').read()
soup = BeautifulSoup(the_html, 'lxml')

rows = soup.find_all('tr')

studentSlateIDs = []
studentNames = []

for row in rows:
    if row.attrs:
        for attr in row.attrs:
            if attr == 'data-id':
                print(row.attrs['data-id'])
                studentSlateIDs.append(row.attrs['data-id'])
    divs = row.find_all('div')
    for div in divs:
        if div.attrs:
            if div.attrs['class'][0]=='name':
                print(div.text)
                studentNames.append(div.text)

print(studentSlateIDs)
print(studentNames)

if len(studentSlateIDs)==len(studentNames):
    for iStudent in range(len(studentSlateIDs)):
        print(studentNames[iStudent] + "\t " + studentSlateIDs[iStudent])

if 1:
    for studentSlateID in studentSlateIDs:
        url = "https://apply.grad.uci.edu/manage/reader/?r=https%3a%2f%2fapply.grad.uci.edu%2fmanage%2f&b=be7c6ee0-c81c-48c1-abc2-15225ae5d075&id=" + studentSlateID
        commandForChrome = "open -a Google\ Chrome \""+ url + "\""
        os.system(commandForChrome)

if 0:
    htmlFile = open("names" + suffix + ".html","w")
    for iStudent in range(len(studentSlateIDs)):
        url = "https://apply.grad.uci.edu/manage/reader/?r=https%3a%2f%2fapply.grad.uci.edu%2fmanage%2f&b=be7c6ee0-c81c-48c1-abc2-15225ae5d075&id=" + studentSlateIDs[iStudent]
        lineForHTML = "<a href=\""+ url + "\">" + studentNames[iStudent]+ "</a><br>\n"
        htmlFile.write(lineForHTML)
    htmlFile.close()
