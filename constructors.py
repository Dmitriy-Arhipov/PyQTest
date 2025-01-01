import sqlite3
from PyQt6.QtWidgets import QWidget, QComboBox, QDialog, QLineEdit
from players import PyVideoPlayer, PyAudioPlayer, PyImagePlayer
from UI_design import UI_TestAskWidget, UI_GameAskWidget, UI_ConstructorTest, UI_ConstructorGame


class AskWidget:
    def add_media(self):
        '''
        добавляет медиафайл в вопрос
        '''
        dlg = QDialog()
        sel_t = QComboBox(dlg)
        sel_t.addItems(['Картинка', 'Аудио', 'Видео'])
        dlg.exec()
        s = sel_t.currentText()
        if s == 'Картинка':
            ip = PyImagePlayer(self)
            ip.exec()
        elif s == 'Видео':
            vp = PyVideoPlayer(self)
            vp.exec()
        elif s == 'Аудио':
            ap = PyAudioPlayer(self)
            ap.exec()
        dlg.close()
        self.file_label.setText(self.fname)

class TestAskWidget(UI_TestAskWidget, AskWidget, QWidget):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.setupUi(self)
        self.vars.clicked.connect(self.add_var)
        self.var_lst = []
        self.del_btn.clicked.connect(self.delete)
        self.fname = ''
        self.media.clicked.connect(self.add_media)
        self.id = 0

    def add_var(self):
        '''
        добавляет вариант ответа
        '''
        self.var = QLineEdit(self)
        self.ask.addWidget(self.var)
        self.var_lst.append(self.var)

    def delete(self):
        '''
        удаляет вопрос
        '''
        lst = []
        for i in self.var_lst:
            lst.append(i.text())
        try:
            con = sqlite3.connect('PyQTest.db')
            req = f'''DELETE FROM {self.root.fname} where ASK = "{self.ask_text.toPlainText()}" AND CORRECT = "{self.cor.text()}"
                AND ANSWERS = "{';'.join(lst)}"'''
            con.cursor().execute(req)
            con.commit()
            con.close()
        except Exception:
            pass


class GameAskWidget(UI_GameAskWidget, AskWidget, QWidget):
    def __init__(self, root):
        super().__init__(root)
        self.setupUi(self)
        self.root = root
        self.fname = ''
        self.media.clicked.connect(self.add_media)


class ConstructorTest(UI_ConstructorTest, QDialog):
    def __init__(self, root, fname):
        super().__init__(root)
        self.fname = fname
        self.setupUi(self)
        self.select_btn.clicked.connect(self.selectbtn)
        self.save_btn.clicked.connect(self.savebtn)
        self.update_lst, self.ask_lst = [], []
        self.get_update_lst()

    def selectbtn(self):
        '''
        создает новый тестовый вопрос
        :return:
        '''
        self.aw = TestAskWidget(self)
        self.ask.addWidget(self.aw)
        self.ask_lst.append(self.aw)

    def get_update_lst(self):
        '''
        получает записи из БД
        '''
        try:
            req = f'SELECT ASK, CORRECT, ANSWERS, MULTIMEDIA, ID FROM {self.fname}'
            con = sqlite3.connect('PyQTest.db')
            values = con.cursor().execute(req).fetchall()
            con.close()
            for vs in values:
                aw = TestAskWidget(self)
                self.ask.addWidget(aw)
                aw.ask_text.setPlainText(vs[0])
                aw.cor.setText(vs[1])
                aw.fname = vs[3]
                aw.id = vs[4]
                if aw.fname:
                    aw.file_label.setText(aw.fname)
                for t in vs[2].split(';'):
                    aw.add_var()
                    aw.var_lst[-1].setText(t)
                self.update_lst.append(aw)
        except Exception:
            pass

    def savebtn(self):
        '''
        сохраняет записи в БД/обновляет уже существующие
        '''
        con = sqlite3.connect('PyQTest.db')
        for aw in self.ask_lst:
            lst = []
            for i in aw.var_lst:
                lst.append(i.text())
            if not aw.fname:
                req = f'''INSERT INTO {self.fname}(ASK, CORRECT, ANSWERS) VALUES(
                "{aw.ask_text.toPlainText()}", "{aw.cor.text()}", "{';'.join(lst)}")'''
            else:
                req = f'''INSERT INTO {self.fname}(ASK, CORRECT, MULTIMEDIA, ANSWERS) VALUES(
                        "{aw.ask_text.toPlainText()}", "{aw.cor.text()}", "{aw.fname}", "{';'.join(lst)}")'''
            try:
                con.cursor().execute(req)
            except Exception:
                pass
        for aw in self.update_lst:
            lst = []
            for i in aw.var_lst:
                lst.append(i.text())
            if not aw.fname:
                req = f'''UPDATE {self.fname} SET ASK = "{aw.ask_text.toPlainText()}", CORRECT = "{aw.cor.text()}", 
                ANSWERS = "{';'.join(lst)}" WHERE ID={aw.id}'''
            else:
                req = f'''UPDATE {self.fname} SET ASK = "{aw.ask_text.toPlainText()}", CORRECT = "{aw.cor.text()}", 
                                ANSWERS = "{';'.join(lst)}", MULTIMEDIA = "{aw.fname}" WHERE ID={aw.id}'''
            try:
                con.cursor().execute(req)
            except Exception:
                pass
        con.commit()
        con.close()
        self.close()


class ConstructorGame(UI_ConstructorGame, QDialog):
    def __init__(self, root, fname):
        super().__init__(root)
        self.fname = fname
        self.setupUi(self)
        self.create.clicked.connect(self.create_table)
        self.save.clicked.connect(self.save_table)
        self.lst = []
        self.y, self.x = 1, 1

    def create_table(self):
        '''
        создает интерфейс таблицы
        '''
        self.x, self.y = self.themes.value() + 1, self.points.value() + 1
        self.lst = [[GameAskWidget(self) for i in range(self.x)] for j in range(self.y)]
        self.get_table()
        for i in range(1, self.y):
            for j in range(1, self.x):
                if (i, j) in self.values.keys():
                    asktxt, cortxt, mul = self.values[(i, j)]
                    self.lst[i][j].ask_text.setPlainText(asktxt)
                    self.lst[i][j].cor.setPlainText(cortxt)
                    self.lst[i][j].fname = mul
                    self.lst[i][j].file_label.setText(self.lst[i][j].fname)
                self.table.addWidget(self.lst[i][j], i, j)
        for j in range(1, self.x):
            if j in self.themes.keys():
                self.lst[0][j] = QLineEdit(self.themes[j], self)
            else:
                self.lst[0][j] = QLineEdit(f'Тема {j}', self)
            self.table.addWidget(self.lst[0][j], 0, j)
        for i in range(1, self.y):
            if i in self.points.keys():
                self.lst[i][0] = QLineEdit(self.points[i], self)
            else:
                self.lst[i][0] = QLineEdit(f'{i}00', self)
            self.table.addWidget(self.lst[i][0], i, 0)

    def save_table(self):
        '''
        сохраняет записи в БД/обновляет уже существующие
        '''
        con = sqlite3.connect('PyQTest.db')
        for i in range(1, self.y):
            for j in range(1, self.x):
                if (i, j) in self.values.keys():
                    req = f'''UPDATE {self.fname} SET ASK = "{self.lst[i][j].ask_text.toPlainText()}", CORRECT = "{self.lst[i][j].cor.toPlainText()}", MULTIMEDIA = "{self.lst[i][j].fname}" WHERE X = {j} AND Y = {i}'''
                else:
                    req = f'''INSERT INTO {self.fname}(ASK, CORRECT, MULTIMEDIA, X, Y) VALUES ("{self.lst[i][j].ask_text.toPlainText()}", "{self.lst[i][j].cor.toPlainText()}", "{self.lst[i][j].fname}",{j}, {i})'''
                try:
                    con.cursor().execute(req)
                    con.commit()
                except Exception:
                    pass
        for i in range(1, self.y):
            req = f'UPDATE {self.fname} SET POINT = "{self.lst[i][0].text()}" WHERE Y = {i}'
            try:
                con.cursor().execute(req)
                con.commit()
            except Exception:
                pass
        for j in range(1, self.x):
            req = f'UPDATE {self.fname} SET THEME = "{self.lst[0][j].text()}" WHERE X = {j}'
            try:
                con.cursor().execute(req)
                con.commit()
            except Exception:
                pass
        con.close()
        self.close()

    def get_table(self):
        '''
        получает записи из БД
        '''
        try:
            req = f'SELECT ASK, CORRECT, MULTIMEDIA, Y, X FROM {self.fname}'
            reqt = f'SELECT DISTINCT X, THEME FROM {self.fname}'
            reqp = f'SELECT DISTINCT Y, POINT FROM {self.fname}'
            con = sqlite3.connect('PyQTest.db')
            self.themes = dict(con.cursor().execute(reqt).fetchall())
            self.points = dict(con.cursor().execute(reqp).fetchall())
            self.values = dict(map(lambda t: ((t[3], t[4]), (t[0], t[1], t[2])), con.cursor().execute(req).fetchall()))
            con.close()
        except Exception:
            pass
