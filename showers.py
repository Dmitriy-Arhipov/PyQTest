from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QDialog, QMessageBox, QLabel, QRadioButton,
                             QButtonGroup, QTableWidgetItem)
import sqlite3
from players import PyVideoPlayer, PyAudioPlayer, PyImagePlayer
from UI_design import UI_GameShowWidget, UI_ShowTest, UI_ShowGame
class ShowWidget:
    def see(self):
        '''
        показ медиа
        '''
        if self.fname != '':
            s = self.fname[(self.fname).rfind('.'):]
            if s in ['.jpg', '.jpeg', '.gif', '.png']:
                ip = PyImagePlayer(self, self.fname)
                ip.exec()
            elif s in ['.mp4', '.mpeg', '.mov', '.avi']:
                vp = PyVideoPlayer(self, self.fname)
                vp.exec()
            elif s == '.mp3':
                ap = PyAudioPlayer(self, self.fname)
                ap.exec()
            else:
                mb = QMessageBox()
                mb.setText('Файл был удален или перемещен!')

class TestShowWidget(ShowWidget, QWidget):
    def __init__(self, root, ask, cor, answers, mul):
        super().__init__(root)
        self.root = root
        self.fname = str(mul)
        self.answers = set(answers.split(';'))
        self.answers.add(cor)
        self.ask = ask
        self.load_UI()
        self.cor = cor

    def load_UI(self):
        vb = QVBoxLayout(self)
        self.setLayout(vb)
        self.ask_text = QLabel(self)
        self.ask_text.setText(self.ask)
        vb.addWidget(self.ask_text)
        self.see_btn = QPushButton(self)
        self.see_btn.clicked.connect(self.see)
        self.see_btn.setText('Просмотреть медиа')
        vb.addWidget(self.see_btn)
        self.ans_buttons = QButtonGroup(self)
        self.ab = QVBoxLayout(self)
        for ans in self.answers:
            a = QRadioButton(self)
            a.setText(ans)
            self.ans_buttons.addButton(a)
            self.ab.addWidget(a)
        vb.addLayout(self.ab)


class GameShowWidget(UI_GameShowWidget, ShowWidget, QDialog):
    def __init__(self, root, ask, cor, mul):
        super().__init__(root)
        self.root = root
        self.setupUi(self)
        self.fname = mul
        self.ask = ask
        self.cor = cor
        self.ask_text.setText(ask)
        self.see_btn.clicked.connect(self.see)
        self.check_btn.clicked.connect(self.check)

    def check(self):
        self.ans_text.setText(self.cor)

class ShowTest(UI_ShowTest, QDialog):
    def __init__(self, root, fname):
        super().__init__(root)
        self.root = root
        self.fname = fname
        self.setupUi(self)
        self.testlst = []
        self.setWindowTitle(self.fname)
        self.check_btn.clicked.connect(self.checkbtn)
        self.construct()

    def construct(self):
        '''
        получает тест из БД
        '''
        con = sqlite3.connect('PyQTest.db')
        req = f"""SELECT ASK, CORRECT, ANSWERS, MULTIMEDIA FROM {self.fname}"""
        tlst = con.cursor().execute(req).fetchall()
        con.close()
        for ask in tlst:
            a = TestShowWidget(self, ask=ask[0], cor=ask[1], answers=ask[2], mul=ask[3])
            self.testlst.append(a)
            self.test.addWidget(a)

    def checkbtn(self):
        '''
        проверка введенных ответов
        '''
        cnt = 0
        errors = []
        for ask in self.testlst:
            if ask.ans_buttons.checkedButton().text() == ask.cor:
                cnt += 1
            else:
                errors.append(f'{ask.ask}\nПравильный ответ:{ask.cor}')
        mb = QMessageBox(self)
        mb.setWindowTitle('Ваш результат:')
        e = '\n'.join(errors)
        e = f'Ошибки:\n{e}' if e else ''
        mb.setText(f'''Ваш результат:\n{cnt} из {len(self.testlst)}.
        Вы набрали {cnt / len(self.testlst) * 100} баллов из 100.\n{e}''')
        mb.show()

class ShowGame(UI_ShowGame, QDialog):
    def __init__(self, root, fname):
        super().__init__(root)
        self.root = root
        self.fname = fname
        self.setupUi(self)
        self.setWindowTitle(self.fname)
        self.construct()
        self.lst = [[0 for j in range(self.x + 1)] for i in range(self.y + 1)]
        self.table.setColumnCount(self.x)
        self.table.setRowCount(self.y)
        self.table.setHorizontalHeaderLabels(self.themes)
        self.table.setVerticalHeaderLabels(self.points)
        for val in self.values:
            self.lst[val[3] - 1][val[4] - 1] = GameShowWidget(self, *val[:3])
            self.table.setItem(val[3] - 1, val[4] - 1, QTableWidgetItem(f'{val[6]}-{val[5]}'))
        for i in range(self.y):
            for j in range(self.x):
                self.table.cellClicked.connect(self.cell_show)

    def cell_show(self):
        '''
        обработка нажатия на ячейку
        '''
        try:
            dlg = self.lst[self.table.currentRow()][self.table.currentColumn()]
            dlg.show()
        except Exception:
            pass

    def construct(self):
        '''
        получает записи из БД
        '''
        try:
            req = f'SELECT ASK, CORRECT, MULTIMEDIA, Y, X, POINT, THEME FROM {self.fname}'
            reqt = f'SELECT DISTINCT THEME FROM {self.fname}'
            reqp = f'SELECT DISTINCT POINT FROM {self.fname}'
            con = sqlite3.connect('PyQTest.db')
            self.themes = list(map(lambda x: ''.join(x), con.cursor().execute(reqt).fetchall()))
            self.points = list(map(lambda x: ''.join(x), con.cursor().execute(reqp).fetchall()))
            self.x, self.y = len(self.themes), len(self.points)
            self.values = list(con.cursor().execute(req).fetchall())
            con.close()
        except Exception as e:
            pass
