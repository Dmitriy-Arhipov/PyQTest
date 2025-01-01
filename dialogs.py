from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QPushButton, QDialog, QFileDialog
import sqlite3
from functions import from_file_to_sql, from_sql_to_file
from constructors import ConstructorTest, ConstructorGame
from showers import ShowTest, ShowGame
from UI_design import UI_CreateDialog, UI_ExportDialog
import os
import shutil

class CreateDialog(UI_CreateDialog, QDialog):
    def __init__(self, root):
        super().__init__(root)
        self.setWindowTitle("Создать")
        self.setupUi(self)
        self.create_btn.clicked.connect(self.createbtn)
        self.root = root

    def createbtn(self):
        '''
        диалог создания нового теста/игры
        '''
        self.fname = self.filename.text()
        con = sqlite3.connect('PyQTest.db')
        if self.cbtype.currentText() == 'Тест':
            req = f'''CREATE TABLE {str(self.fname)} (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
            ASK TEXT, ANSWERS TEXT, CORRECT TEXT, MULTIMEDIA TEXT)'''
            type = 'test'
        else:
            type = 'game'
            req = f'''CREATE TABLE {str(self.fname)} (X INTEGER, Y INTEGER, THEME TEXT, POINT TEXT, ASK TEXT, 
            CORRECT TEXT, MULTIMEDIA TEXT)'''
        req2 = f"INSERT INTO FILES(name, type) values('{str(self.fname)}', '{type}')"
        try:
            os.mkdir(f'media/{str(self.fname)}')
            con.cursor().execute(req)
            con.cursor().execute(req2)
            con.commit()
            con.close()
        except Exception as e:
            print('sqlerror:', e)
        cbm, cbt = self.cbmode.currentText(), self.cbtype.currentText()
        if cbm == 'Конструктор':
            if cbt == 'Тест':
                self.root.construct = ConstructorTest(self.root, self.fname)
            else:
                self.root.construct = ConstructorGame(self.root, self.fname)
        elif cbm == 'Из файла':
            name = QFileDialog.getOpenFileName(self, 'c:\\', '', "Table files (*.csv *.xlsx)")[0]
            from_file_to_sql(ext=str(name).split('.')[1], type='test' if cbt == 'Тест' else 'game',
                             filename=name, sqlname=self.fname)
            if cbt == 'Тест':
                self.root.construct = ConstructorTest(self.root, self.fname)
            else:
                self.root.construct = ConstructorGame(self.root, self.fname)
        self.close()
        self.root.construct.show()


class DeleteDialog(QDialog):
    def __init__(self, root):
        super().__init__(root)
        self.opn = QComboBox(self)
        self.delete_btn = QPushButton(self)
        self.delete_btn.setText('Удалить')
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.opn)
        hbox.addWidget(self.delete_btn)
        self.con = sqlite3.connect('PyQTest.db')
        req = """SELECT type, name FROM files"""
        self.delete_btn.clicked.connect(self.deletebtn)
        result = self.con.cursor().execute(req).fetchall()
        self.opn_lst = []
        for t in result:
            self.opn.addItem(f'{t[1]}.{t[0]}')
            self.opn_lst.append(f'{t[1]}.{t[0]}')
        self.setWindowTitle("Удалить")

    def deletebtn(self):
        '''
        диалог удаления теста/игры
        '''
        d = self.opn.currentText().split('.')
        self.opn_lst.remove(self.opn.currentText())
        req = '''DELETE FROM FILES WHERE NAME = ? AND TYPE = ?'''
        req2 = f'DROP TABLE {d[0]}'
        self.con.cursor().execute(req, (d[0], d[1])),
        self.con.cursor().execute(req2)
        self.opn.clear()
        self.opn.addItems(self.opn_lst)
        shutil.rmtree(f'media/{d[0]}')
        self.con.commit()
        self.close()


class OpenDialog(QDialog):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.setWindowTitle("Открыть")
        self.opn = QComboBox(self)
        self.open_btn = QPushButton()
        self.open_btn.setText('Открыть')
        self.open_btn.clicked.connect(self.openbtn)
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.opn)
        hbox.addWidget(self.open_btn)
        self.setLayout(hbox)
        con = sqlite3.connect('PyQTest.db')
        req = """SELECT type, name FROM files"""
        result = con.cursor().execute(req).fetchall()
        con.close()
        for t in result:
            self.opn.addItem(f'{t[1]}.{t[0]}')

    def openbtn(self):
        '''
        диалог открытия теста/игры
        '''
        d = self.opn.currentText().split('.')
        if len(d) > 1 and d[1] == 'test':
            self.root.construct = ConstructorTest(self.root, d[0])
        else:
            self.root.construct = ConstructorGame(self.root, d[0])
        self.root.construct.show()
        self.close()


class ExportDialog(UI_ExportDialog, QDialog):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.setupUi(self)
        con = sqlite3.connect('PyQTest.db')
        req = """SELECT type, name FROM files"""
        result = con.cursor().execute(req).fetchall()
        con.close()
        for t in result:
            self.opn.addItem(f'{t[1]}.{t[0]}')
        self.export_btn.clicked.connect(self.exportbtn)

    def exportbtn(self):
        '''
        диалог экспорта
        '''
        sqlname, type = self.opn.currentText().split('.')
        fname = self.fname.text()
        ext = self.sqltype.currentText()
        from_sql_to_file(sqlname=sqlname, filename=fname, type=type, ext=ext.lower())
        self.close()


class RunDialog(QDialog):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.setWindowTitle("Запуск")
        self.opn = QComboBox(self)
        self.open_btn = QPushButton()
        self.open_btn.setText('Запустить')
        self.open_btn.clicked.connect(self.openbtn)
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.opn)
        hbox.addWidget(self.open_btn)
        self.setLayout(hbox)
        con = sqlite3.connect('PyQTest.db')
        req = """SELECT type, name FROM files"""
        result = con.cursor().execute(req).fetchall()
        con.close()
        for t in result:
            self.opn.addItem(f'{t[1]}.{t[0]}')

    def openbtn(self):
        '''
        диалог запуска
        '''
        d = self.opn.currentText().split('.')
        if len(d) > 1 and d[1] == 'test':
            self.root.construct = ShowTest(self.root, d[0])
        else:
            self.root.construct = ShowGame(self.root, d[0])
        self.root.construct.show()
        self.close()

