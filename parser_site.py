import requests
from bs4 import BeautifulSoup as BS
import urllib.request

url = "https://www.mirea.ru/schedule/"
res = requests.get(url)
soup = BS(res.text, 'lxml')
institutes = soup.find_all('a', class_='uk-link-toggle')
links = []
for i in institutes:
    links.append(i.get("href"))


def download_files():
    print('Beginning file download with urllib2...')
    # the schedule is downloaded from this link
    i = 1
    for link in links:
        file_name = link.split('/')[-1]
        urllib.request.urlretrieve(url=link, filename=f'shedules/{file_name}')
        print(str(i) + 'done')
        i += 1
    print('DOWNLOADED')
    return 0


for i in range(0, len(links)):
    links[i] = links[i].split('/')[-1]

files = {'BAK': {'IPTIP': links[0:8], 'ITU': links[9:16], 'IIT': links[17:20], 'III': links[21:25],
                 'IKB': links[26:30], 'IRI': links[31:35], 'ITKHT': links[36:39]},
         'MAG': {'IPTIP': links[40:43], 'ITU': links[44:49], 'IIT': links[50:51], 'III': links[52:53],
                 'IKB': links[54:55], 'IRI': links[56:57], 'ITKHT': links[58:59]},
         'ASP': {'IPTIP': links[60:66], 'ITU': links[67:69], 'Raspisanie': links[70], 'IIT': links[71:74],
                 'III': links[75:78], 'IKB': links[79:84], 'IRI': links[85:88], 'ITKHT': links[89:94]},
         'KPK': {'RASPISANIE': links[95]},
         'DOP': {'podg_1': links[96], 'podg_2': links[97], 'podg_3': links[98], 'podg_4': links[99], 'dop': links[100]}
         }
