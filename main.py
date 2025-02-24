import sys
import io
import sqlite3

from PyQt6.QtWidgets import QWidget, QApplication, QTableWidgetItem
from PyQt6.QtCore import Qt
from addCoffee import addCoffeeValue
from ui.main_ui import Ui_Form


class Coffee(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.set_values)
        self.addButton.clicked.connect(self.add_values)
        self.tableWidget.itemChanged.connect(self.change_value)
        self.con = sqlite3.connect("data//coffee.sqlite")
        self.cur = self.con.cursor()
        self.modified = dict()

    def set_values(self):
        result = self.cur.execute("SELECT * FROM coffee_options").fetchall()
        self.titles = [descr[0] for descr in self.cur.description]
        self.tableWidget.clear()
        if result:
            self.tableWidget.setRowCount(len(result))
            for row, value in enumerate(result):
                for column, value1 in enumerate(value):
                    value1 = QTableWidgetItem(str(value1))
                    if column == 0:
                        value1.setFlags(value1.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.tableWidget.setItem(row, column, value1)

    def add_values(self):
        self.addCoffee = addCoffeeValue(self.con)
        self.addCoffee.show()

    def change_value(self, item):
        if self.tableWidget.currentRow() != -1:
            self.modified[self.titles[item.column()]] = item.text()
            print(self.modified)
            que = "UPDATE coffee_options SET\n"
            que += "\n".join([f"{key}='{self.modified.get(key)}'" for key in self.modified.keys()])
            que += "WHERE id = ?"
            self.cur.execute(que, (self.tableWidget.item(item.row(), 0).text(), ))
            self.con.commit()
            self.set_values()

    def closeEvent(self, event):
        if self.addCoffee:
            self.addCoffee.close()
        self.con.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    coffee = Coffee()
    coffee.show()
    sys.exit(app.exec())
