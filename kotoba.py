from typing import List
from bs4 import BeautifulSoup
import requests
from main import Kanji
import xlwt

url = 'http://jls.vnjpclub.com/tu-vung-minna-no-nihongo-bai-{}.html'


def getListKanji(bai: int) -> List[Kanji]:
    r = requests.get(url.format(bai))
    soup = BeautifulSoup(r.text, 'lxml')
    tbody = soup.select("#khungchinhgiua > table > tbody")[0]
    # all row in table
    listKanji = []
    for tr in tbody('tr'):
        hiragana = tr.td.string
        kanji = tr('td')[4].string
        am_han = tr('td')[5].string
        mean = tr('td')[6].string
        bai = str(bai)
        listKanji.append(Kanji([kanji, hiragana, am_han, mean, bai]))
    return listKanji

def toExcelFile(f: str, k: List[Kanji]):
    workbook = xlwt.Workbook()  
    sheet = workbook.add_sheet("Kotoba") 
    # Writing on specified sheet 
    sheet.write(0, 0, 'KANJI')
    sheet.write(0,1, 'HIRAGANA')
    sheet.write(0,2, 'ÂM HÁN')
    sheet.write(0,3, 'NGHĨA')
    sheet.write(0,4, 'BÀI')
    for i in range(len(k)):
        sheet.write(i+1,0, k[i].getKanji())
        sheet.write(i+1,1, k[i].getHiragana())
        sheet.write(i+1,2, k[i].getBoThu())
        sheet.write(i+1,3, k[i].getMean())
        sheet.write(i+1,4, k[i].getBai())
    workbook.save(f)

if __name__ == "__main__":
    listKanji = []
    for i in range(1,51):
        listKanji += getListKanji(i)
    toExcelFile('excel_kanji.xls',listKanji)