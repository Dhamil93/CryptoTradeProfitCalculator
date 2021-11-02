
# Name: Atilola Damilare.
# Student Number: 3026982

import datetime as dt
import sys

from PyQt5 import QtGui
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QLabel, QComboBox, QCalendarWidget, QDialog, QApplication, QGridLayout, QDoubleSpinBox


class StockTradeProfitCalculator(QDialog):

    def __init__(self):

        super().__init__()

        # setting up dictionary of stocks
        self.data = self.make_data()
        # sorting the dictionary of stocks by the keys. The keys at the high level are dates, so we are sorting by date
        self.stocks = sorted(self.data.keys())

        # print all the dates and close prices for BTC
        print("all the dates and close prices for BTC", self.data['BTC'])
        # print the close price for BTC on 04/29/2013
        print("the close price for BTC on 04/29/2013", self.data['BTC'][QDate(2013, 4, 29)])

        #  first date in dataset - 29th Apr 2013
        self.first_date = dt.datetime(2013, 4, 29)
        #        #  last date in dataset - 6th Jul 2021
        # When the calendars load we want to ensure that the default dates selected are within the date range above
        #  we can do this by setting variables to store suitable default values for sellCalendar and buyCalendar.
        self.sellCalendarDefaultDate = sorted(self.data['BTC'].keys())[-1]
        print("self.sellCalendarStartDate", self.sellCalendarDefaultDate)
        self.buyCalendarDefaultDate = sorted(self.data['BTC'].keys())[-1]
        print("self.buyCalendarStartDate", self.buyCalendarDefaultDate)

        # create QLabel for stock purchased
        self.stock_label = QLabel()
        self.stock_label.setText("Stock Purchase: ")
        # create QComboBox and populate it with a list of stocks
        self.fromComboBox_stock = QComboBox()
        self.fromComboBox_stock.addItems(self.stocks)
        # create CalendarWidgets for selection of purchase and sell dates

        self.calendar_buy_label = QLabel("Purchase Date: ")
        self.calendarWidgetBuy = QCalendarWidget()
        self.calendarWidgetBuy.setGeometry(140, 100, 261, 151)

        self.calendar_sell_label = QLabel("Sell Date: ")
        self.calendarWidgetSell = QCalendarWidget()
        self.calendarWidgetSell.setGeometry(140, 270, 261, 151)

        # create QSpinBox to select stock quantity purchased
        self.spinBox_label = QLabel("Quantity Purchased: ")
        self.fromSpinBox_quantity = QDoubleSpinBox()
        self.fromSpinBox_quantity.setRange(0.001, 10000000.00)
        self.fromSpinBox_quantity.setValue(1.0)
        # create QLabels to show the stock purchase total
        self.label_stock_purchase_total = QLabel()
        self.label_stock_purchase_total.setText("Purchase Total: ")
        self.label_stock_purchase_total_value = QLabel()
        # create QLabels to show the stock sell total
        self.label_stock_sell_total = QLabel()
        self.label_stock_sell_total.setText("Sell Total: ")
        self.label_stock_sell_total_value = QLabel()

        # create QLabels to show the stock profit total
        self.label_stock_profit_total = QLabel()
        self.label_stock_profit_total.setText("Profit total: ")
        self.label_stock_profit_total.setStyleSheet("font-weight: bold")
        self.label_stock_profit_total_value = QLabel()

        # initialize the layout - 6 rows to start
        grid = QGridLayout()
        # create space between the grid
        grid.setSpacing(20)
        # row 0 - stock selection
        grid.addWidget(self.stock_label, 0, 0)
        grid.addWidget(self.fromComboBox_stock, 0, 1)
        # row 1 - quantity selection
        grid.addWidget(self.spinBox_label, 1, 0)
        grid.addWidget(self.fromSpinBox_quantity, 1, 1)
        # row 2 - purchase date selection
        grid.addWidget(self.calendar_buy_label, 2, 0)
        grid.addWidget(self.calendarWidgetBuy, 2, 1)
        # row 3 - display purchase total
        grid.addWidget(self.label_stock_purchase_total, 3, 0)
        grid.addWidget(self.label_stock_purchase_total_value, 3, 1)
        # row 4 - sell date selection
        grid.addWidget(self.calendar_sell_label, 4, 0)
        grid.addWidget(self.calendarWidgetSell, 4, 1)
        # row 5 - display sell total
        grid.addWidget(self.label_stock_sell_total, 5, 0)
        grid.addWidget(self.label_stock_sell_total_value, 5, 1)
        # row 6 - display profit total
        grid.addWidget(self.label_stock_profit_total, 6, 0)
        grid.addWidget(self.label_stock_profit_total_value, 6, 1)

        # set the calendar values
        self.calendarWidgetBuy.setMaximumDate(self.sellCalendarDefaultDate)
        self.calendarWidgetBuy.setMinimumDate(self.first_date)
        self.calendarWidgetSell.setMaximumDate(self.sellCalendarDefaultDate)
        self.calendarWidgetSell.setMinimumDate(self.first_date)
        # purchase: two weeks before most recent
        self.calendarWidgetBuy.setSelectedDate(self.sellCalendarDefaultDate.addDays(-14))
        # sell: most recent
        self.calendarWidgetSell.setSelectedDate(self.sellCalendarDefaultDate)
        # connecting signals to slots to that a change in one control updates the UI
        self.fromComboBox_stock.currentIndexChanged.connect(self.updateUi)
        self.fromSpinBox_quantity.valueChanged.connect(self.updateUi)
        self.calendarWidgetBuy.clicked.connect(self.updateUi)
        self.calendarWidgetSell.clicked.connect(self.updateUi)
        # set the window title
        self.setWindowTitle("Crypto Trade Profit Calculator")

        # Inserting an Icon in the Window
        self.iconName = ("cripto_icon.png")
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        # update the UI
        self.setLayout(grid)


    def updateUi(self):
        '''
        This requires substantial development
        Updates the Ui when control values are changed, should also be called when the app initializes
        :return:
        '''
        try:
            print("")
            stock_purchased = self.fromComboBox_stock.currentText()
            quantity = self.fromSpinBox_quantity.value()
            # get selected dates from calendars
            data_buy = self.calendarWidgetBuy.selectedDate()
            data_sell = self.calendarWidgetSell.selectedDate()

            # perform necessary calculations to calculate totals

            # Calculating Purchase Value Total of stock using the price in the chosen date
            stock_price = self.data[stock_purchased][data_buy]
            purchase_total_value = stock_price * quantity
            purchase_total_value = round(purchase_total_value, 2)

            # Calculating Sales Value Total of stock using the price in the chosen date
            stock_price = self.data[stock_purchased][data_sell]
            sell_total_value = stock_price * quantity
            sell_total_value = round(sell_total_value, 2)

            # Calculating Profit
            profit = sell_total_value - purchase_total_value
            profit = round(profit, 2)

            # update the label displaying totals
            self.label_stock_purchase_total_value.setText(str(purchase_total_value))
            self.label_stock_purchase_total_value.setStyleSheet("font-weight: bold")
            self.label_stock_sell_total_value.setText(str(sell_total_value))
            self.label_stock_sell_total_value.setStyleSheet("font-weight: bold")
            # Case there is profit will display Green, if is a loss it will be red
            if (profit < 0):
                self.label_stock_profit_total_value.setStyleSheet('color:red; font-weight: bold')
            else:
                self.label_stock_profit_total_value.setStyleSheet('color:green; font-weight: bold')
            self.label_stock_profit_total_value.setText(str(profit))
        except Exception as e:
            print(e)


    def make_data(self):
        '''
        This code is complete
        Data source is derived from https://www.kaggle.com/camnugent/sandp500/download but use the provided file to avoid confusion

        Converts a CSV file to a dictionary fo dictionaries like

            Stock   -> Date      -> Close
            AAL     -> 08/02/2013 -> 14.75
                    -> 11/02/2013 -> 14.46
                    ...
            AAPL    -> 08/02/2013 -> 67.85
                    -> 11/02/2013 -> 65.56

        Helpful tutorials to understand this
        - https://stackoverflow.com/questions/482410/how-do-i-convert-a-string-to-a-double-in-python
        - nested dictionaries https://stackoverflow.com/questions/16333296/how-do-you-create-nested-dict-in-python
        - https://www.tutorialspoint.com/python3/python_strings.htm
        :return: a dictionary of dictionaries
        '''
        file = open("./CryptoCoins_Prices/combined.csv", "r")  # open a CSV file for reading https://docs.python.org/3/library/functions.html#open
        data = {}  # empty data dictionary
        file_rows = []  # empty list of file rows
        # add rows to the file_rows list
        for row in file:
            file_rows.append(row.strip())  # https://www.geeksforgeeks.org/python-string-strip-2/
        print("len(file_rows):" + str(len(file_rows)))

        # get the column headings of the CSV file
        row0 = file_rows[0]
        line = row0.split(",")
        column_headings = line
        print(column_headings)

        # get the unique list of stocks from the CSV file
        non_unique_stocks = []
        file_rows_from_row1_to_end = file_rows[1:len(file_rows) - 1]
        for row in file_rows_from_row1_to_end:
            line = row.split(",")
            non_unique_stocks.append(line[6])
        stocks = self.unique(non_unique_stocks)
        print("len(stocks):" + str(len(stocks)))
        print("stocks:" + str(stocks))

        # build the base dictionary of stocks
        for stock in stocks:
            data[stock] = {}

        # build the dictionary of dictionaries
        for row in file_rows_from_row1_to_end:
            line = row.split(",")
            date = self.string_date_into_QDate(line[0])
            stock = line[6]
            close_price = line[4]
            # include error handling code if close price is incorrect
            data[stock][date] = float(close_price)
        print("len(data):", len(data))
        return data

    def string_date_into_QDate(self, date_String):
        '''
        This method is complete
        Converts a data in a string format like that in a CSV file to QDate Objects for use with QCalendarWidget
        :param date_String: data in a string format
        :return:
        '''
        date_list = date_String.split("-")
        date_QDate = QDate(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        return date_QDate

    def unique(self, non_unique_list):
        '''
        This method is complete
        Converts a list of non-unique values into a list of unique values
        Developed from https://www.geeksforgeeks.org/python-get-unique-values-list/
        :param non_unique_list: a list of non-unique values
        :return: a list of unique values
        '''

        # initializing a null list
        unique_list = []

        # traverse for all elements
        for x in non_unique_list:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)
                # print list
        return unique_list


# This is complete
if __name__ == '__main__':
    app = QApplication(sys.argv)
    currency_converter = StockTradeProfitCalculator()
    currency_converter.show()
    sys.exit(app.exec_())
