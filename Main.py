import sys, sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Hазвание сорта", "Cтепень обжарки", "Mолотый/в зернах", "Oписание вкуса", "цена".capitalize(), "Oбъем упаковки(мл)"])
        self.titles = ["id", "name_sort", "step_obj", "type", "tasty", "price", "volume"]
        self.update()
        self.pushButton.clicked.connect(self.upload)
        self.tableWidget.itemChanged.connect(self.item_changed)

    def update(self):
        res = self.con.cursor().execute("""SELECT * FROM coffee""").fetchall()
        self.tableWidget.setRowCount(len(res))
        for i, elem in enumerate(res):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def item_changed(self, item):
        if item.column() != 0:
            a = item.text()
            col = self.titles[item.column()]
            ind = self.tableWidget.item(item.row(), 0).text()
            que = "UPDATE coffee SET " + col + " = "
            que += f"'{a}'" if item.column() < 5 else a
            que += " WHERE id = " + ind
            self.con.cursor().execute(que)
            self.con.commit()

    def upload(self):
        self.uploadWidget = UploadCoffee(self)
        self.uploadWidget.show()


class UploadCoffee(QMainWindow):
    def __init__(self, form):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.form = form
        self.pushButton.clicked.connect(self.upload)

    def upload(self):
        res = [self.name.text(), self.step_obj.text(), self.type.text(), self.tasty.text(), self.price.text(), self.volume.text()]
        if "" in res or None in res:
            QMessageBox.critical(self, "Ошибка", "Не все поля заполнены")
        else:
            self.up(res)

    def up(self, res):
        que = "INSERT INTO coffee(name_sort, step_obj, type, tasty, price, volume) VALUES"
        que += "(" + f"'{res[0]}', '{res[1]}', '{res[2]}', '{res[3]}', {res[4]}, {res[5]}" + ")"
        self.con.cursor().execute(que)
        self.con.commit()
        self.form.update()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
