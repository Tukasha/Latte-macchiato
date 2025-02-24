from PyQt6.QtWidgets import QWidget
from ui.addEditCoffeeForm import Ui_Form


class addCoffeeValue(QWidget, Ui_Form):
    def __init__(self, con):
        super().__init__()
        self.setupUi(self)
        self.con = con
        self.cur = self.con.cursor()
        self.initUI()

    def initUI(self):
        self.edits = [self.nameEdit, self.degreeEdit, self.groundbeansEdit, 
                      self.tasteEdit, self.priceEdit, self.volumeEdit]
        self.clearButton.clicked.connect(self.clear_edits)
        self.sendButton.clicked.connect(self.send_values)

    def clear_edits(self):
        self.clear_result()
        [item.clear() for item in self.edits]

    def send_values(self):
        self.clear_result()
        texts = [item.text() for item in self.edits]
        if len(list(filter(lambda x: str(x) != '', texts))) == len(self.edits):
            texts = [texts[i] if i < 5 else float(texts[i]) for i in range(len(texts))] 
            self.cur.execute('''INSERT INTO coffee_options VALUES (?, ?, ?, ?, ?, ?, ?)''', (None,) + tuple(texts))
            self.con.commit()
            self.resultLabel.setText("Значение успешно добавлено. Обновите таблицу.")
        else:
            self.resultLabel.setText("Одно или несколько значений некорректны, проверьте поля и повторите попытку.")

    def clear_result(self):
        self.resultLabel.clear()