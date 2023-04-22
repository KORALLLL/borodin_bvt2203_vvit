#импорт необходимых модулей и адаптеров
import psycopg2
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QTabWidget, QAbstractScrollArea,
                             QHBoxLayout, QVBoxLayout, QTableWidget, QGroupBox, QTableWidgetItem,
                             QPushButton, QMessageBox)

#Создаём класс MainWindow с конструктором
class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._connect_to_db()
        self.setWindowTitle("Пользовательский интерфейс")
        self.vbox = QVBoxLayout(self)
        self.tabs = QTabWidget(self) #класс создаёт структуру, которую можно заполнять вкладками
        self.vbox.addWidget(self.tabs)
        self._create_schedule_tab()
    
    def _connect_to_db(self): #метод для подключение к БД
        self.conn = psycopg2.connect(database = 'timetable', user = 'postgres',
                                     password = 'k30042004', host = 'localhost', port = '5432')
        self.cursor = self.conn.cursor()
        self.conn.autocommit = True
    
    def _create_schedule_tab(self): #метод для отображения вкладки с расписанием
        self.schedule_tab1 = QTabWidget() #класс QWidget() создаёт виджет, который будет вкладкой в нашем приложении
        self.schedule_tab2 = QTabWidget()
        self.tabs.addTab(self.schedule_tab1, "Нечётная неделя") #Добавляет в структуру с вкладками новую вкладку с названием Schedule
        self.tabs.addTab(self.schedule_tab2, "Чётная неделя")

        self._create_day_table(1, 1, self.schedule_tab1)
        self._create_day_table(1, 2, self.schedule_tab1)
        self._create_day_table(1, 3, self.schedule_tab1)
        self._create_day_table(1, 4, self.schedule_tab1)
        self._create_day_table(1, 5, self.schedule_tab1)
        self._create_day_table(1, 6, self.schedule_tab1)
        self._create_day_table(2, 1, self.schedule_tab2)
        self._create_day_table(2, 2, self.schedule_tab2)
        self._create_day_table(2, 3, self.schedule_tab2)
        self._create_day_table(2, 4, self.schedule_tab2)
        self._create_day_table(2, 5, self.schedule_tab2)
        self._create_day_table(2, 6, self.schedule_tab2)
        
    def _create_day_table(self, type_of_week, day_of_week, schedule_tab): #Метод для отображение таблицы с расписанием на понедельних четной недели
        days = ['понедельник','вторник','среда','четверг','пятница','суббота']
        widget = QWidget()
        schedule_tab.addTab(widget, days[day_of_week-1])
        
        self.day_gbox = QGroupBox("расписание") #класс может группировать виджеты, он предоставляет рамку, заголовок вверху
        #и может отображать несколько виджетов внутри. В нашем случае он нужен в качестве декорации.

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.day_gbox)

        day_table = QTableWidget() #создание пустой пользовательской таблицы
        
        day_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents) #Установка возможности изменения размера под размер данных в ячейке

        day_table.setColumnCount(7) #Задание количества колонок
        day_table.setHorizontalHeaderLabels(['номер пары', 'кабинет','тип занятия',
                                             'преподаватель', "дисциплина", 'редактирование', "удаление"]) #Задание колонкам подписей

        self._update_day_table(type_of_week, day_of_week, day_table)

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(day_table)
        self.day_gbox.setLayout(self.mvbox)

        self.update_schedule_button = QPushButton("Обновиить")
        self.shbox2.addWidget(self.update_schedule_button)

        self.update_schedule_button.clicked.connect(lambda: self._update_schedule(type_of_week, day_of_week, day_table))

        widget.setLayout(self.svbox)

    def _update_day_table(self, type_of_week, day_of_week, day_table): #метод для обновления таблицы с расписанием на понедельник четной недели
        self.cursor.execute("""SELECT timetable.num, 
        timetable.room_numb, subject.type, teacher.full_name, subject.title
        FROM subject
        JOIN teacher ON (subject.id = teacher.subject_id)
        JOIN timetable ON (subject.id = timetable.subject_id)
        WHERE timetable.week = %s AND timetable.day = %s
        ORDER BY timetable.num""",(str(type_of_week), str(day_of_week)))
        records = list(self.cursor.fetchall())

        day_table.setRowCount(len(records)+1) #задание количества строк

        for i, r in enumerate(records): #цикл для динамической обработки изменения в количестве записей
            r = list(r)
            joinButton = QPushButton("изменить") #кнопка не отдельное свойство класса MainWindow, тк нам не нужно её
            #запоминать. Далее интерпретатор запоминает её с помощь функции-обработчика clicked.connect()
            deleteButton =QPushButton("Удалить")
            day_table.setItem(i, 0, QTableWidgetItem(str(r[0]))) #запись в ячейку с определённым адресом строковые данные
            day_table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            day_table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            day_table.setItem(i, 3, QTableWidgetItem(str(r[3])))
            day_table.setItem(i, 4, QTableWidgetItem(str(r[4])))
            day_table.setCellWidget(i, 5, joinButton) #Помещение в ячейку с определённым адресом виджет(кнопка join)
            day_table.setCellWidget(i, 6, deleteButton)

            joinButton.clicked.connect(lambda ch, num = i: self._change_day_from_table(num, type_of_week, day_of_week, day_table))
            deleteButton.clicked.connect(lambda ch, num = i: self._delete_day_table(num, type_of_week, day_of_week, day_table))

            day_table.resizeRowsToContents() #автоматическая адаптация размеров ячеек таблицы под размер данных внутри этой
            #ячейки. Это необходимо использовать для экономии визуального пространства
        day_table.setItem(len(records), 0, QTableWidgetItem()) #запись в ячейку с определённым адресом строковые данные
        day_table.setItem(len(records), 1, QTableWidgetItem())
        day_table.setItem(len(records), 2, QTableWidgetItem())
        day_table.setItem(len(records), 3, QTableWidgetItem())
        day_table.setItem(len(records), 4, QTableWidgetItem())
        
        insertButton = QPushButton("Добавить")
        day_table.setCellWidget(len(records), 5, insertButton)
        insertButton.clicked.connect(lambda ch: self._create_row_table(len(records), day_table, type_of_week, day_of_week))
        clickButton = QPushButton("кликни")
        day_table.setCellWidget(len(records), 6, clickButton)
        clickButton.clicked.connect(lambda: QMessageBox.about(self, 'неееееет', "Зачем вы это сделали? Больше так не делайте"))

    def _change_day_from_table(self, rowNum, type_of_week, day_of_week, day_table): #метод изменяющий запись в базе данных по нажатию кнопки join
        row = list()
        for i in range(day_table.columnCount()): #метод columnCount возвращает количество колонок в таблице
            try:
                row.append(day_table.item(rowNum, i).text()) #конструкция item(row,col) возвращает текст, записанный в определённой ячейке
            except:
                row.append(None)
        
        try:
            self.cursor.execute("""
            CALL update_values(%s,%s,%s,%s,%s,%s,%s)
            """,(str(type_of_week),str(day_of_week),row[0],row[1],row[2],row[3],row[4]))
        except:
            QMessageBox.about(self, "ошибка", 'Заполните все поля')
    
    def _create_row_table(self, rowNum, day_table, type_of_week, day_of_week):
        row = list()
        for i in range(day_table.columnCount()):
            try:
                row.append(day_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("""
            CALL insert_values(%s, %s, %s, %s, %s, %s, %s)
            """,(str(type_of_week), str(day_of_week), row[0],row[1],row[2],row[3],row[4]))
        except:
            QMessageBox.about(self, "ошибка", "Заполните все поля или убедитесь, что номер пары целое число")
        self._update_schedule(type_of_week, day_of_week, day_table)

    def _delete_day_table(self, rowNum, type_of_week, day_of_week, day_table):
        row = day_table.item(rowNum, 0).text()
        try:
            self.cursor.execute("""
            CALL delete_values(%s,%s, %s)
            """,(str(type_of_week), str(day_of_week), str(row)))
        except:
            QMessageBox.about(self, "Ошибка", "невозможно удалить")
        self._update_schedule(type_of_week, day_of_week, day_table)
        

    def _update_schedule(self, type_of_week,day_of_week, day_table): #метод обновляющий все таблицы на вкладке
        self._update_day_table(type_of_week,day_of_week, day_table)
        #здесь дописать методы обновления таблиц

#запуск приложения
app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
