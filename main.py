import sys

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QFontDatabase
from design import Ui_MainWindow
from typing import Union, Optional
from operator import add, sub, mul, truediv

operations = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv
}

error_zero_div = 'Division by zero'
error_undefined = 'Result is undefined'


class Calculator(QMainWindow):
    def __init__(self):
        super(Calculator, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.entry_max_len = self.ui.le_entry.maxLength()

        # Added Rubick font
        QFontDatabase.addApplicationFont("fonts/Rubick-Regular.ttf")

        # Connect digits
        self.ui.btn_0.clicked.connect(self.add_digit)
        self.ui.btn_1.clicked.connect(self.add_digit)
        self.ui.btn_2.clicked.connect(self.add_digit)
        self.ui.btn_3.clicked.connect(self.add_digit)
        self.ui.btn_4.clicked.connect(self.add_digit)
        self.ui.btn_5.clicked.connect(self.add_digit)
        self.ui.btn_6.clicked.connect(self.add_digit)
        self.ui.btn_7.clicked.connect(self.add_digit)
        self.ui.btn_8.clicked.connect(self.add_digit)
        self.ui.btn_9.clicked.connect(self.add_digit)

        # actions ( there r connected action buttons)
        self.ui.btn_clear.clicked.connect(self.clear_all)
        self.ui.btn_ce.clicked.connect(self.clear_entry)
        self.ui.btn_point.clicked.connect(self.add_point)
        self.ui.btn_neg.clicked.connect(self.negate)
        self.ui.btn_backspace.clicked.connect(self.backspace)

        # math buttons
        self.ui.but_calc.clicked.connect(self.calculate)
        self.ui.btn_plus.clicked.connect(lambda: self.math_operation('+'))
        self.ui.btn_sub.clicked.connect(lambda: self.math_operation('-'))
        self.ui.btn_mul.clicked.connect(lambda: self.math_operation('*'))
        self.ui.btn_div.clicked.connect(lambda: self.math_operation('/'))

    # Adding digit to lable entry
    # If lable has zero, zero becomes btn_text, if not zero - label digit + btn_text
    def add_digit(self):
        self.remove_error()
        self.clear_tmp_if_equality()
        btn = self.sender()

        digit_buttons = ('btn_0', 'btn_1', 'btn_2', 'btn_3', 'btn_4',
                         'btn_5', 'btn_6', 'btn_7', 'btn_8', 'btn_9')
        if btn.objectName() in digit_buttons:
            if self.ui.le_entry.text() == '0':
                self.ui.le_entry.setText(btn.text())
            else:
                self.ui.le_entry.setText(self.ui.le_entry.text() + btn.text())

    # func to add point
    def add_point(self) -> None:
        self.clear_tmp_if_equality()
        if '.' not in self.ui.le_entry.text():
            self.ui.le_entry.setText(self.ui.le_entry.text() + '.')

    # negative func
    def negate(self):
        self.clear_tmp_if_equality()
        entry = self.ui.le_entry.text()

        if '-' not in entry:
            if entry != '0':
                entry = '-' + entry
        else:
            entry = entry[1:]

        if len(entry) == self.entry_max_len + 1 and '-' in entry:
            self.ui.le_entry.setMaxLength(self.entry_max_len + 1)
        else:
            self.ui.le_entry.setMaxLength(self.entry_max_len)

        self.ui.le_entry.setText(entry)

    # backspace func
    def backspace(self):
        self.remove_error()
        self.clear_tmp_if_equality()
        entry = self.ui.le_entry.text()

        if len(entry) != 1:
            if len(entry) == 2 and '-' in entry:
                self.ui.le_entry.setText('0')
            else:
                self.ui.le_entry.setText(entry[:-1])
        else:
            self.ui.le_entry.setText('0')

    # func to clear entry and label
    def clear_all(self) -> None:
        self.remove_error()
        self.ui.le_entry.setText('0')
        self.ui.lbl_temp.clear()

    # function to clear only entry
    def clear_entry(self) -> None:
        self.remove_error()
        self.clear_tmp_if_equality()
        self.ui.le_entry.setText('0')

    def clear_tmp_if_equality(self):
        if self.get_math_sign() == '=':
            self.ui.lbl_temp.clear()

    # static method to delete zeros after point
    @staticmethod
    def remove_trailling_zeros(num: str) -> str:
        n = str(float(num))
        return n[:-2] if n[-2:] == '.0' else n

    # func to add nums and math sign in temp
    def add_temp(self, math_sign: str):
        if not self.ui.lbl_temp.text() or self.get_math_sign() == '=':
            self.ui.lbl_temp.setText(self.remove_trailling_zeros(self.ui.le_entry.text()) + f' {math_sign} ')
            self.ui.le_entry.setText('0')

    # Get num from entry
    def get_entry_num(self) -> Union[int, float]:
        entry = self.ui.le_entry.text().strip('.')

        return float(entry) if '.' in entry else int(entry)

    # Get num from temp
    def get_temp_num(self) -> Union[int, float, None]:
        temp = self.ui.lbl_temp.text().strip('.').split()[0]
        return float(temp) if '.' in temp else int(temp)

    # Get math sign from temp
    def get_math_sign(self) -> Optional[str]:
        if self.ui.lbl_temp.text():
            return self.ui.lbl_temp.text().strip('.').split()[-1]

    def calculate(self) -> Optional[str]:
        entry = self.ui.le_entry.text()
        temp = self.ui.lbl_temp.text()

        try:
            if temp:
                result = self.remove_trailling_zeros(
                    str(operations[self.get_math_sign()](self.get_temp_num(), self.get_entry_num()))
                )
                self.ui.lbl_temp.setText(temp + self.remove_trailling_zeros(entry) + ' =')
                self.ui.le_entry.setText(result)
                return result

        except KeyError:
            pass

        except ZeroDivisionError:
            if self.get_temp_num() == 0:
                self.show_error(error_undefined)
            else:
                self.show_error(error_zero_div)

    def math_operation(self, math_sign: str):
        temp = self.ui.lbl_temp.text()

        if not temp:
            self.add_temp(math_sign)
        else:
            if self.get_math_sign() != math_sign:
                if self.get_math_sign() == '=':
                    self.add_temp(math_sign)
                else:
                    self.ui.lbl_temp.setText(temp[:-2] + f' {math_sign} ')
            else:
                self.ui.lbl_temp.setText(self.calculate() + f' {math_sign} ')

    # function to show errors by div on zero or undefined result
    def show_error(self, text: str) -> None:
        self.ui.le_entry.setMaxLength(len(text))
        self.ui.le_entry.setText(text)
        self.disable_btn()

    def remove_error(self) -> None:
        if self.ui.le_entry.text() in (error_zero_div, error_undefined):
            self.ui.le_entry.setMaxLength(self.entry_max_len)
            self.ui.le_entry.setText('0')

    def disable_btn(self) -> None:
        self.ui.but_calc.setDisabled(True)
        self.ui.btn_plus.setDisabled(True)
        self.ui.btn_sub.setDisabled(True)
        self.ui.btn_mul.setDisabled(True)
        self.ui.btn_div.setDisabled(True)
        self.ui.btn_neg.setDisabled(True)
        self.ui.btn_point.setDisabled(True)
        self.ui.btn_backspace.setDisabled(True)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Calculator()
    window.show()
    sys.exit(app.exec())
