import os
import sys
import SqlLite

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import urllib.request
import WebCorring
from datetime import *
import Calc_Exchange

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

a = []
b = []
c = []
d = []
e = []
f = []
g = []

a2 = []
b2 = []
c2 = []
f2 = []

naraname = ['KRW 대한민국', 'USD 미국', 'JPY 일본', 'EUR 유럽', 'CNY 중국', 'HKD 홍콩', 'GBP 영국', 'CHF 스위스',
                    'CAD 캐나다', 'AUD 호주', 'NZD 뉴질랜드', 'SEK 스웨덴', 'DKK 덴마크', 'NOK 노르웨이',
                    'SAR 사우디아라비아', 'KWD 쿠웨이트', 'BHD 바레인', 'AED 아랍에미리트 연합', 'THB 태국',
                    'SGD 싱가포르', 'IDR 인도네시아', 'INR 인도', 'MYR 말레이지아', 'PKR 파키스탄', 'BDT 방글라데시',
                    'PHP 필리핀', 'EGP 이집트', 'MXN 멕시코', 'BND 브루나이']

naraname2 = ['USD 미국', 'JPY 일본', 'EUR 유럽', 'CNY 중국', 'HKD 홍콩', 'GBP 영국', 'CHF 스위스',
                    'CAD 캐나다', 'AUD 호주', 'NZD 뉴질랜드', 'SEK 스웨덴', 'DKK 덴마크', 'NOK 노르웨이',
                    'SAR 사우디아라비아', 'KWD 쿠웨이트', 'BHD 바레인', 'AED 아랍에미리트 연합', 'THB 태국',
                    'SGD 싱가포르', 'IDR 인도네시아', 'INR 인도', 'MYR 말레이지아', 'PKR 파키스탄', 'BDT 방글라데시',
                    'PHP 필리핀', 'EGP 이집트', 'MXN 멕시코', 'BND 브루나이']

kospi_top5 = {
    '1': naraname2,
    '2': a,
    '3': f,
    '4': g,
    '5': b,
    '6': c,
    '7': d,
    '8': e
}

date_list = []
name_list = []
type_list = []
money1_list = []
money2_list = []
profit_list = []

column_idx_lookup = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7}

info_list = {
    '1': date_list,
    '2': name_list,
    '3': type_list,
    '4': money1_list,
    '5': money2_list,
    '6': profit_list
}
column_idx_lookup2 = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5}

now = datetime.now()

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 50
        self.top = 50
        self.title = 'Exchange Rate'
        self.width = 1265
        self.height = 900
        self.initUI()

    def initUI(self):
        #SqlLite.Create_tabe()

        self.init_exchangedata(now)

        self.InitMenu()

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(20, 40, 635, 540)

        self.tableWidget.setRowCount(len(naraname2))
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.setTableWidgetData()

        self.tableWidget2 = QTableWidget(self)
        self.tableWidget2.setGeometry(675, 160, 570, 540)

        self.InitInfoData()
        self.InfoTable()

        self.tableWidget2.itemDoubleClicked.connect(self.RemoveTableData)

        groupBox = QGroupBox("", self)
        groupBox.setGeometry(20, 600, 240, 30)

        self.radio1 = QRadioButton("1개월", self)
        self.radio1.move(30, 600)
        self.radio1.setChecked(True)
        self.radio1.clicked.connect(self.radioButtonClicked)

        self.radio2 = QRadioButton("3개월", self)
        self.radio2.move(90, 600)
        self.radio2.clicked.connect(self.radioButtonClicked)

        self.radio3 = QRadioButton("1년", self)
        self.radio3.move(150, 600)
        self.radio3.clicked.connect(self.radioButtonClicked)

        self.radio4 = QRadioButton("3년", self)
        self.radio4.move(210, 600)
        self.radio4.clicked.connect(self.radioButtonClicked)

        self.CalcFun()

        self.combo1 = QComboBox(self)
        self.combo1.setGeometry(270, 605, 150, 20)

        self.InitComboBox()

        self.lbl = QLabel(self)
        self.lbl.setGeometry(20, 610, 635, 300)
        self.DrewGraph('month')

        self.show()

    def RemoveTableData(self):
        row = self.tableWidget2.currentItem().row()

        date = self.tableWidget2.item(row, 0).text()
        name = self.tableWidget2.item(row, 1).text()
        type = self.tableWidget2.item(row, 2).text()
        money1 = self.tableWidget2.item(row, 3).text()
        money2 = self.tableWidget2.item(row, 4).text()

        SqlLite.Remove_Data(date, name, type, money1, money2)

        self.InitInfoData()
        self.InfoTable()

    def InfoTable(self):
        self.tableWidget2.clear()

        self.tableWidget2.setRowCount(len(date_list))
        self.tableWidget2.setColumnCount(6)
        self.tableWidget2.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.setTableWidgetData2()

    def CalcFun(self):
        groupBox2 = QGroupBox("", self)
        groupBox2.setGeometry(675, 40, 500, 30)

        self.radio5 = QRadioButton("매매기준율", self)
        self.radio5.move(685, 40)
        self.radio5.setChecked(True)
        self.radio5.clicked.connect(self.radioButtonClicked2)

        self.radio6 = QRadioButton("현금 살때", self)
        self.radio6.move(785, 40)
        self.radio6.clicked.connect(self.radioButtonClicked2)

        self.radio7 = QRadioButton("현금 팔때", self)
        self.radio7.move(885, 40)
        self.radio7.clicked.connect(self.radioButtonClicked2)

        self.radio8 = QRadioButton("송금 보낼때", self)
        self.radio8.move(985, 40)
        self.radio8.clicked.connect(self.radioButtonClicked2)

        self.radio9 = QRadioButton("송금 받을때", self)
        self.radio9.move(1085, 40)
        self.radio9.clicked.connect(self.radioButtonClicked2)

        self.combo2 = QComboBox(self)
        self.combo2.setGeometry(675, 80, 200, 30)

        self.textBox1 = QLineEdit(self)
        self.textBox1.setGeometry(675, 110, 200, 30)

        self.textBox2 = QLineEdit(self)
        self.textBox2.setGeometry(975, 110, 200, 30)

        self.label = QLabel(self)
        self.label.setText('=')
        self.label.setGeometry(925, 110, 50, 30)

        self.calcBtn = QPushButton('Calc', self)
        self.calcBtn.setGeometry(1195, 80, 50, 30)
        self.calcBtn.clicked.connect(self.button_click)

        self.insertBtn = QPushButton('Insert', self)
        self.insertBtn.setGeometry(1195, 110, 50, 30)
        self.insertBtn.clicked.connect(self.button_click2)

    def InitMenu(self):
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

    def PixMapDrew(self):
        self.lbl.clear()
        pixmap = QPixmap("image\Graph.png")
        self.lbl.setPixmap(QPixmap(pixmap))

    def init_FGsetting(self, y):
        date_before = y - timedelta(1)
        searchdate = f'{date_before.year}.{date_before.month}.{date_before.day}'
        money_data = []

        if len(WebCorring.StartCroring(searchdate)) == 0:
            while True:
                date_before2 = date_before - timedelta(1)
                searchdate = f'{date_before2.year}.{date_before2.month}.{date_before2.day}'
                if len(WebCorring.StartCroring(searchdate)) != 0:
                    break
                else:
                    date_before = date_before2

        for data in WebCorring.StartCroring(searchdate):
            money_value = data.get_text().replace('\n', '').replace('\t', '')
            money_data.append(money_value)

        count = 0
        idx = 0
        for i in money_data:
            if count == 0:
                b2.append(money_data.__getitem__(idx).replace(',', ''))
                count = count + 1
                idx = idx + 1
            elif count == 1:
                c2.append(money_data.__getitem__(idx).replace(',', ''))
                count = count + 1
                idx = idx + 1
            elif count == 2:
                count = count + 1
                idx = idx + 1
            elif count == 3:
                count = 0
                idx = idx + 1

        idx2 = 0
        for i in b:
            rate = round(((float(b2.__getitem__(idx2)) + float(c2.__getitem__(idx2))) / 2), 2)
            a2.append(str(rate))
            idx2 = idx2 + 1

        idx3 = 0
        for i in a:
            updown = round(float(a.__getitem__(idx3)) - float(a2.__getitem__(idx3)), 2)
            if updown < 0:
                temp = str(updown).replace('-', '')
                str_updown = f'▽ {temp}'
                f.append(str_updown)
            elif updown > 0:
                str_updown = f'▲ {str(updown)}'
                f.append(str_updown)
            else:
                f.append(str(updown))
            f2.append(str(updown))
            idx3 = idx3 + 1

        idx4 = 0
        for i in a:
            updown_rate = round(((float(f2.__getitem__(idx4)) * 100) / float(a.__getitem__(idx4))), 2)
            g.append(str(updown_rate))
            idx4 = idx4 + 1

    def InitInfoData(self):
        date_list.clear()
        name_list.clear()
        type_list.clear()
        money1_list.clear()
        money2_list.clear()
        profit_list.clear()

        for i in SqlLite.Date_SeletData():
            date_list.append(i)

        for i in SqlLite.Name_SeletData():
            name_list.append(i)

        for i in SqlLite.Type_SeletData():
            type_list.append(i)

        for i in SqlLite.Money1_SeletData():
            x = i.split('/')
            y = float(x[0])
            z = round(y, 2)
            zx = f'{z}/{x[1]}'
            money1_list.append(i)

        for i in SqlLite.Money2_SeletData():
            x = i.split('/')
            y = float(x[0])
            z = round(y, 2)
            zx = f'{z}/{x[1]}'
            money2_list.append(i)

        self.profit()


    def profit(self):

        index_list = []
        type_col_list = []
        exchange_rate = []
        money1_list_calc = []
        money2_list_calc = []
        exchange_rate_calc = []
        for i in name_list:
            index_list.append(naraname2.index(i))

        for i in type_list:
            if i == "매매기준율":
                type_col_list.append(1)
            elif i == "현금 살때":
                type_col_list.append(4)
            elif i == "현금 팔때":
                type_col_list.append(5)
            elif i == "송금 보낼때":
                type_col_list.append(6)
            elif i == "송금 받을때":
                type_col_list.append(7)

        index = 0
        for i in index_list:
            x = self.tableWidget.item(i, type_col_list[index]).text()
            exchange_rate.append(x)
            index = index + 1

        for i in money1_list:
            x = str(i).split('/')
            y = float(x[0])
            money1_list_calc.append(y)

        if len(money2_list) > 0:
            for i in money2_list:
                x = str(i).split('/')
                y = float(x[0])
                money2_list_calc.append(y)

        index2 = 0
        for i in exchange_rate:
            if index_list[index2] == 1:
                xc = float(i)/100.00
                x = xc * money1_list_calc[index2]
                y = money2_list_calc[index2] - x
                z = round(y, 1)
                zx = f'{z}/KRW'
                profit_list.append(str(zx))
            elif index_list[index2] == 19:
                xc = float(i)/100.00
                x = xc * money1_list_calc[index2]
                y = money2_list_calc[index2] - x
                z = round(y, 1)
                zx = f'{z}/KRW'
                profit_list.append(str(zx))
            else:
                x = float(i) * money1_list_calc[index2]
                y = money2_list_calc[index2] - x
                z = round(y, 1)
                zx = f'{z}/KRW'
                profit_list.append(str(zx))
            index2 = index2 + 1

    def init_exchangedata(self, x):
        money_data = []
        date_now = x
        date_before = date_now
        searchdate = f'{date_now.year}.{date_now.month}.{date_now.day}'

        if len(WebCorring.StartCroring(searchdate)) == 0:
            while True:
                date_now2 = date_now - timedelta(1)
                searchdate = f'{date_now2.year}.{date_now2.month}.{date_now2.day}'
                date_before = date_now2
                if len(WebCorring.StartCroring(searchdate)) != 0:
                    break
                date_now = date_now2


        for data in WebCorring.StartCroring(searchdate):
            money_value = data.get_text().replace('\n', '').replace('\t', '')
            money_data.append(money_value)

        count = 0
        idx = 0
        for i in money_data:
            if count == 0:
                b.append(money_data.__getitem__(idx).replace(',', ''))
                count = count + 1
                idx = idx + 1

            elif count == 1:
                c.append(money_data.__getitem__(idx).replace(',', ''))
                count = count + 1
                idx = idx + 1

            elif count == 2:
                d.append(money_data.__getitem__(idx).replace(',', ''))
                count = count + 1
                idx = idx + 1

            elif count == 3:
                e.append(money_data.__getitem__(idx).replace(',', ''))
                count = 0
                idx = idx + 1

        idx2 = 0
        for i in b:
            rate = round(((float(b.__getitem__(idx2)) + float(c.__getitem__(idx2))) / 2), 2)
            a.append(str(rate))
            idx2 = idx2 + 1

        self.init_FGsetting(date_before)

    def button_click2(self):
        searchdate = f'{now.year}.{now.month}.{now.day}'
        name = self.combo2.currentText()
        type = self.radio2msg()

        str = name.split(' ')
        money1 = f'{self.textBox1.text()}/{str[0]}'
        num = float(self.textBox2.text())
        money2 = f'{num}/KRW'
        SqlLite.Insert_Info(searchdate, name, type, money1, money2)

        self.InitInfoData()
        self.InfoTable()

    def button_click(self):
        name = self.combo2.currentText()
        idx = naraname2.index(name)
        exchange = {}
        if self.radio2msg() == "매매기준율":
            exchange = float(a.__getitem__(idx))
        elif self.radio2msg() == "현금 살때":
            exchange = float(b.__getitem__(idx))
        elif self.radio2msg() == "현금 팔때":
            exchange = float(c.__getitem__(idx))
        elif self.radio2msg() == "송금 보낼때":
            exchange = float(d.__getitem__(idx))
        elif self.radio2msg() == "송금 받을때":
            exchange = float(e.__getitem__(idx))

        money = float(self.textBox1.text())
        x = Calc_Exchange.Usd_Exchage(name, exchange, money)
        self.textBox2.setText(x)

        #self.init_exchangedata(now)
        #self.tableWidget.clear()
        #self.setTableWidgetData()

    def setTableWidgetData2(self):

        column_headers = ['날짜', '통화명', '타입', '외화', '한화', '차익']
        self.tableWidget2.setHorizontalHeaderLabels(column_headers)

        for k, v in info_list.items():
            col = column_idx_lookup2[k]
            for row, val in enumerate(v):
                item = QTableWidgetItem(val)
                if col == 2:
                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)

                self.tableWidget2.setItem(row, col, item)

        self.tableWidget2.resizeColumnsToContents()
        self.tableWidget2.resizeRowsToContents()

    def setTableWidgetData(self):
        column_headers = ['통화명', '매매기준율', '전일대비', '등락율', '현찰 살 때', '현찰 팔 때', '송금 보낼 때', '송금 받을 때']
        self.tableWidget.setHorizontalHeaderLabels(column_headers)

        for k, v in kospi_top5.items():
            col = column_idx_lookup[k]
            for row, val in enumerate(v):
                item = QTableWidgetItem(val)
                if col == 2:
                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)

                self.tableWidget.setItem(row, col, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    def radio2msg(self):
        msg = ""
        if self.radio5.isChecked():
            msg = "매매기준율"
        elif self.radio6.isChecked():
            msg = "현금 살때"
        elif self.radio7.isChecked():
            msg = "현금 팔때"
        elif self.radio9.isChecked():
            msg = "송금 보낼때"
        else:
            msg = "송금 받을때"
        return msg

    def radioButtonClicked2(self):
        msg = self.radio2msg()

    def radioButtonClicked(self):
        msg = ""
        if self.radio1.isChecked():
            msg = "month"
        elif self.radio2.isChecked():
            msg = "month3"
        elif self.radio3.isChecked():
            msg = "year"
        elif self.radio4.isChecked():
            msg = "year3"

        self.DrewGraph(msg)

    def DrewGraph(self, type):
        file = "image\Graph.png"
        if os.path.isfile(file):
            os.remove(file)

        token = self.combo1.currentText()
        temp = token.split(" ")

        urllib.request.urlretrieve(f"https://ssl.pstatic.net/imgfinance/chart/marketindex/area/{type}/FX_{temp[0]}KRW.png", "E:\OpenSource_Project_Exchange\image\Graph.png")
        self.PixMapDrew()

    def InitComboBox(self):
        for i in naraname2:
            self.combo1.addItem(i)
        self.combo1.setCurrentIndex(0)

        for i in naraname:
            self.combo2.addItem(i)
        self.combo2.setCurrentIndex(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


