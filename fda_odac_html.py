from datetime import date
from urllib.request import urlopen
from bs4 import BeautifulSoup

filename = "/home/llh76224/r/research/odac_info/fda_odac_html_"+str(date.today())+".csv"
f = open(filename, "w", encoding="utf-8")
headers = "Year, Date, Agenda, Material, Link\n"
f.write(headers)

today = date.today()
for i in range(0,1):
    yrs=str(today.year-i)
    url = "https://www.fda.gov/advisory-committees/oncologic-drugs-advisory-committee/"+ yrs + "-meeting-materials-oncologic-drugs-advisory-committee"

    html = urlopen(url).read()
    pagesoup = BeautifulSoup(html, features="html.parser")
    # pagesoup = BeautifulSoup(html, features="lxml")
    itemlocator = pagesoup.findAll('a', {'data-entity-type': 'node'})

    for items in itemlocator:   
        names = items['title']

        refs = 'https://www.fda.gov' + items['href']
        # print(refs)

        html_dtls=urlopen(refs).read()
        dtlsoup = BeautifulSoup(html_dtls, features='lxml')

        evtinfo = dtlsoup.find('div', id='event-information')
        dt = evtinfo.find('dl', class_='lcds-description-list--event')
        dd = dt.find('dd', class_='cell-2_1').text

        material= dtlsoup.find('h2', text='Event Materials')
        if material!=None:
            material= 'Yes'
        else:
            material='No'

        heading3 = dtlsoup.find('h3', text='Agenda')
        agenda = ''
        for sibling in heading3.find_next_siblings():
            if sibling.name =='h3':
                # print('Not a tag of p')
                break
            # else
            if sibling.name =='p':
                agenda=agenda + sibling.text
        agenda.replace("\n", ".")

        f.write(yrs.replace(","," ") + ',' +
                dd.replace(","," ") + ',' +
                agenda.replace(","," ") + ',' +
                material.replace(",", " ") + ',' +
                refs.replace(","," ") + "\n" )

f.close()
