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
        self.days = []
        self.tables = []
        self._create_schedule_tab()
        
    
    def _connect_to_db(self): #метод для подключение к БД
        self.conn = psycopg2.connect(database = 'timetable', user = 'postgres',
                                     password = 'k30042004', host = 'localhost', port = '5432')
        self.cursor = self.conn.cursor()
        self.conn.autocommit = True
    
    def _create_schedule_tab(self): #метод для отображения вкладки с расписанием
        self.schedule_tab1 = QTabWidget() #класс QWidget() создаёт виджет, который будет вкладкой в нашем приложении
        self.schedule_tab2 = QTabWidget()
        self.schedule_tab3 = QTabWidget()
        self.tabs.addTab(self.schedule_tab1, "Нечётная неделя") #Добавляет в структуру с вкладками новую вкладку с названием Schedule
        self.tabs.addTab(self.schedule_tab2, "Чётная неделя")
        self.tabs.addTab(self.schedule_tab3, "Таблицы")

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

        self._create_table(1, self.schedule_tab3)
        self._create_table(2, self.schedule_tab3)
        self._create_table(3, self.schedule_tab3)
        
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

        self._full_update()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(day_table)
        self.day_gbox.setLayout(self.mvbox)

        self.update_schedule_button = QPushButton("Обновиить")
        self.shbox2.addWidget(self.update_schedule_button)

        self.update_schedule_button.clicked.connect(lambda: self._full_update())

        widget.setLayout(self.svbox)
        self.days.append([day_table, type_of_week, day_of_week])

        

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
        self._full_update()
    
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
        self._full_update()

    def _delete_day_table(self, rowNum, type_of_week, day_of_week, day_table):
        row = day_table.item(rowNum, 0).text()
        try:
            self.cursor.execute("""
            CALL delete_values(%s,%s, %s)
            """,(str(type_of_week), str(day_of_week), str(row)))
        except:
            QMessageBox.about(self, "Ошибка", "невозможно удалить")
        self._full_update()
        

    def _create_table(self, type_of_table, schedule_tab):
        tables = ['subject', 'teacher', 'timetable']
        widget = QWidget()
        schedule_tab.addTab(widget, tables[type_of_table-1])

        self.table_gbox = QGroupBox("таблица")
        self.dsvbox = QVBoxLayout()
        self.dshbox1 = QHBoxLayout()
        self.dshbox2 = QHBoxLayout()

        self.dsvbox.addLayout(self.dshbox1)
        self.dsvbox.addLayout(self.dshbox2)

        self.dshbox1.addWidget(self.table_gbox)

        table = QTableWidget()
        table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        if type_of_table == 1:
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(['id','title','type', 'edit','delete'])
        elif type_of_table == 2:
            table.setColumnCount(5)
            table.setHorizontalHeaderLabels(['id',"full_name",'subject_id', 'edit','delete'])
        else:
            table.setColumnCount(8)
            table.setHorizontalHeaderLabels(['id','week','day','subject_id','room_numb','num', 'edit','delete'])
        
        self._full_update()

        self.dmvbox = QVBoxLayout()
        self.dmvbox.addWidget(table)
        self.table_gbox.setLayout(self.dmvbox)

        self.update_table_button = QPushButton("Обновить")
        self.dshbox2.addWidget(self.update_table_button)

        self.update_table_button.clicked.connect(lambda: self._full_update())

        widget.setLayout(self.dsvbox)
        self.tables.append([table, type_of_table])



    def _update_table(self, type_of_table, table):
        if type_of_table == 1:
            self.cursor.execute("""SELECT *
            FROM subject ORDER BY id""")
        elif type_of_table == 2:
            self.cursor.execute("""SELECT *
            FROM teacher ORDER BY id""")
        else:
            self.cursor.execute("""SElECT *
            FROM timetable ORDER BY id""")
        records = list(self.cursor.fetchall())
        table.setRowCount(len(records)+1)
        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Изменить")
            deleteButton = QPushButton("Удалить")
            for j in range(len(r)):
                table.setItem(i, j, QTableWidgetItem(str(r[j])))
            table.setCellWidget(i, len(r), joinButton)
            table.setCellWidget(i, len(r)+1, deleteButton)

            joinButton.clicked.connect(lambda ch, num = i, arr = r: self._change_value_from_table(num,type_of_table, table, arr[0]))
            deleteButton.clicked.connect(lambda ch, num = i: self._delete_row_table(num, type_of_table, table))

            table.resizeRowsToContents()
        
        insertButton = QPushButton("Добавить")
        clickButton = QPushButton("кликни")
        if type_of_table==1 or type_of_table==2:
            table.setItem(len(records), 0, QTableWidgetItem())
            table.setItem(len(records), 1, QTableWidgetItem())
            table.setItem(len(records), 2, QTableWidgetItem())
            table.setCellWidget(len(records), 3, insertButton)
            table.setCellWidget(len(records), 4, clickButton)
        else:
            table.setItem(len(records), 0, QTableWidgetItem())
            table.setItem(len(records), 1, QTableWidgetItem())
            table.setItem(len(records), 2, QTableWidgetItem())
            table.setItem(len(records), 3, QTableWidgetItem())
            table.setItem(len(records), 4, QTableWidgetItem())
            table.setItem(len(records), 5, QTableWidgetItem())
            table.setCellWidget(len(records), 6, insertButton)
            table.setCellWidget(len(records), 7, clickButton)
        insertButton.clicked.connect(lambda ch: self._create_row(len(records), type_of_table, table))
        clickButton.clicked.connect(lambda: QMessageBox.about(self, 'нееееееет', "Зачем вы это сделали? Больше так не делайте"))

    def _change_value_from_table(self, rowNum, type_of_table, table, id):
        row = list()
        for i in range(table.columnCount()):
            try:
                row.append(table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            if type_of_table==1:
                self.cursor.execute("""
                CALL update_subject(%s,%s,%s,%s)
                """, (str(id),row[0],row[1],row[2], ))
            elif type_of_table==2:
                self.cursor.execute("""
                UPDATE teacher SET id = %s, full_name=%s, subject_id=%s WHERE id = %s
                """,(row[0],row[1],row[2], str(id)))
            else:
                self.cursor.execute("""
                UPDATE timetable SET id=%s, week = %s, day=%s, subject_id = %s, room_numb=%s, num = %s
                WHERE id = %s
                """,(row[0],row[1],row[2],row[3], row[4], row[5], str(id)))
        except:
            QMessageBox.about(self, "ошибка","Проверьте правильность введёных данных")
        self._full_update()

    def _create_row(self, rowNum, type_of_table, table):
        row = list()
        for i in range(table.columnCount()):
            try:
                row.append(table.item(rowNum,i).text())
            except:
                row.append(None)
        try:
            if type_of_table == 1:
                self.cursor.execute("""
                INSERT INTO subject VALUES(%s,%s,%s)
                """,(row[0],row[1],row[2]))
            elif type_of_table == 2:
                self.cursor.execute("""
                INSERT INTO teacher VALUES(%s,%s,%s)
                """,(row[0],row[1],row[2]))
            else:
                self.cursor.execute("""
                INSERT INTO timetable VALUES(%s,%s,%s,%s,%s,%s)
                """,(row[0], row[1], row[2], row[3], row[4], row[5]))
        except:
            QMessageBox.about(self, "Ошибка", "Проверьте правильность заполнения полей")
        self._full_update()

    def _delete_row_table(self, rowNum, type_of_table, table):
        rea = table.item(rowNum, 0).text()
        if type_of_table==1:
            self.cursor.execute("""
            DELETE FROM subject WHERE id=
            """+str(rea))
        elif type_of_table==2:
            self.cursor.execute("""
            DELETE FROM teacher WHERE id=
            """ + str(rea))
        else:
            self.cursor.execute("""
            DELETE FROM timetable WHERE id=
            """+(str(rea)))
        self._full_update()
    
    def _full_update(self):
        for i in range(len(self.days)):
            self._update_day_table(self.days[i][1], self.days[i][2],self.days[i][0])
        for i in range(len(self.tables)):
            self._update_table(self.tables[i][1],self.tables[i][0])

#запуск приложения
app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
