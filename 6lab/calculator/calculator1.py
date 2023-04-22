import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton
from decimal import Decimal


'''
QApplication - управление потоком управления и основными настройками приложения с графическим интерфейсом
QWidget - базовый класс для всех объектов пользовательского интерфейса
QLineEdit - виджет, разрешающий работы ввода и редактирования одной строки текста
QHBoxLayot - выстраивание виджетов по горизонтали
QVBoxLayot - выстраивание виджетов по вертикали
QPushButton - кнопка на которую можно нажать
'''


class Calculator(QWidget):
    def __init__(self):
        super(Calculator, self).__init__()
        self.op = ""
        self.num_1 = 0
        self.num_2 = 0

        
        #создание и наследование класса

        self.vbox = QVBoxLayout(self)
        self.hbox_input = QHBoxLayout()
        self.hbox_first = QHBoxLayout()
        self.hbox_second = QHBoxLayout()
        self.hbox_third = QHBoxLayout()
        self.hbox_null = QHBoxLayout()
        self.hbox_result = QHBoxLayout()

        self.vbox.addLayout(self.hbox_input)
        self.vbox.addLayout(self.hbox_first)
        self.vbox.addLayout(self.hbox_second)
        self.vbox.addLayout(self.hbox_third)
        self.vbox.addLayout(self.hbox_null)
        self.vbox.addLayout(self.hbox_result)

        #создание осей выравнивания

        self.input = QLineEdit(self)
        self.hbox_input.addWidget(self.input)

        self.b_1 = QPushButton("1", self)
        self.hbox_first.addWidget(self.b_1)

        self.b_2 = QPushButton("2", self)
        self.hbox_first.addWidget(self.b_2)

        self.b_3 = QPushButton("3", self)
        self.hbox_first.addWidget(self.b_3)

        self.b_4 = QPushButton("4", self)
        self.hbox_second.addWidget(self.b_4)

        self.b_5 = QPushButton("5", self)
        self.hbox_second.addWidget(self.b_5)
        
        self.b_6 = QPushButton("6", self)
        self.hbox_second.addWidget(self.b_6)

        self.b_7 = QPushButton("7", self)
        self.hbox_third.addWidget(self.b_7)

        self.b_8 = QPushButton("8", self)
        self.hbox_third.addWidget(self.b_8)

        self.b_9 = QPushButton("9", self)
        self.hbox_third.addWidget(self.b_9)

        self.b_0 = QPushButton("0", self)
        self.hbox_null.addWidget(self.b_0)

        self.b_dot = QPushButton(".", self)
        self.hbox_null.addWidget(self.b_dot)

        self.b_plus = QPushButton("+", self)
        self.hbox_first.addWidget(self.b_plus)

        self.b_minus = QPushButton("-", self)
        self.hbox_second.addWidget(self.b_minus)

        self.b_mul = QPushButton("*", self)
        self.hbox_third.addWidget(self.b_mul)

        self.b_div = QPushButton("/", self)
        self.hbox_null.addWidget(self.b_div)

        self.b_result = QPushButton("=", self)
        self.hbox_result.addWidget(self.b_result)

        self.b_clear = QPushButton("CE", self)
        self.hbox_result.addWidget(self.b_clear)

        #создание виджетов и привязка их к соответствующим осям выравнивания
        #привязка виджетов к осям осуществляется с помощью функции addWidget()]
        
        self.b_plus.clicked.connect(lambda: self._operation("+"))
        self.b_minus.clicked.connect(lambda: self._operation("-"))
        self.b_mul.clicked.connect(lambda: self._operation("*"))
        self.b_div.clicked.connect(lambda: self._operation("/"))
        self.b_result.clicked.connect(self._result)
        self.b_clear.clicked.connect(self._clear)

        self.b_1.clicked.connect(lambda: self._button("1"))
        self.b_2.clicked.connect(lambda: self._button("2"))
        self.b_3.clicked.connect(lambda: self._button("3"))
        self.b_4.clicked.connect(lambda: self._button("4"))
        self.b_5.clicked.connect(lambda: self._button("5"))
        self.b_6.clicked.connect(lambda: self._button("6"))
        self.b_7.clicked.connect(lambda: self._button("7"))
        self.b_8.clicked.connect(lambda: self._button("8"))
        self.b_9.clicked.connect(lambda: self._button("9"))
        self.b_0.clicked.connect(lambda: self._button("0"))
        self.b_dot.clicked.connect(lambda: self._button("."))

        #Создание события, отвечающих за реакции на нажатия по кнопкам
        #функция connect(funk) вызывает функции с именем, указанным в скобках
        #у указанную функцию нельзя передавать аргументы
        #для решения этой проблемы используются lambda-функциии

    def _button(self, param):
        line = self.input.text()
        if "division by zero" in line or "enter correct number" in line:
            line = ""
        self.input.setText(line + param)

        #создание метода класса для обработки кнопок, овтечающий за ввод цифр в линиию ввода текста
        #уже существующая строка в линии ввода конкатенируетя с аргументом param
        #и устанавливается как отображаемые в линии ввода текст

    def _operation(self, op):
        self.num_1 = (self.input.text())
        if self.num_1 == "":
            pass
        else:
            try:
                self.num_1 = Decimal(self.num_1)
                self.op = op
                self.input.setText("")
            except:
                self.num_1 = 0
                self.num_2 = 0
                self.input.setText("enter correct number")

        #создание метода класса для обработки нажатия на кнопку математической операции
        #запоминаем первое введеное число в decimal типе данных
        #запоминаем в качестве операции аргумент ор
        #очищаем линию ввода

    def _result(self):
        try:
            self.num_2 = Decimal(self.input.text())
        except:
            pass
        if self.op == "+":
            if (self.num_1 + self.num_2) == Decimal(int(self.num_1 + self.num_2)):
                 self.input.setText(str(int(self.num_1 + self.num_2)))
            else:
                self.input.setText(str(self.num_1 + self.num_2))
        elif self.op == "-":
            if (self.num_1 - self.num_2) == Decimal(int(self.num_1 - self.num_2)):
                self.input.setText(str(int(self.num_1 - self.num_2)))
            else:
                self.input.setText(str(self.num_1 - self.num_2))
        elif self.op == "*":
            if (self.num_1 * self.num_2) == Decimal(int(self.num_1 * self.num_2)):
                self.input.setText(str(int(self.num_1 * self.num_2)))
            else:
                self.input.setText(str(self.num_1 * self.num_2))
        elif self.op == "/" and self.num_2 != 0:
            if (self.num_1 / self.num_2) == Decimal(self.num_1 // self.num_2):
                self.input.setText(str(int(self.num_1 / self.num_2)))
            else:
                self.input.setText(str(self.num_1 / self.num_2))
        elif self.op == "/" and self.num_2 == 0:
            self.input.setText("division by zero")
        elif self.op == "":
            self.num_1 = self.input.text()
            self.input.setText(str(self.num_1))

        #создание метода класса для обработки нажатия на кнопку результата
        #запоминаем второе введеное число в decimal типе данных
        #проивзодим вычисление в зависимости от операции и устанавливаем
        #его в качестве текста в линию вывода

    def _clear(self):
        self.num_1 = 0
        self.num_2 = 0
        self.input.setText("")



app = QApplication(sys.argv)

win = Calculator()
win.show()

sys.exit(app.exec_())
#запуск приложения