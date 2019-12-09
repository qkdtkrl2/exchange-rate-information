import urllib.request
from bs4 import BeautifulSoup

def StartCroring(x):
    exchange_str = f'https://www.kita.net/cmmrcInfo/ehgtGnrlzInfo/rltmEhgt.do?sDate={x}'
    fp = urllib.request.urlopen(exchange_str)
    source = fp.read()
    fp.close()
    class_list = ["pcVer"]
    soup = BeautifulSoup(source, 'html.parser')
    soup = soup.find_all("td", class_=class_list)
    return soup














