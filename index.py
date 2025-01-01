from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QMessageBox
from UI_design import UI_main
from dialogs import OpenDialog, CreateDialog, DeleteDialog, RunDialog, ExportDialog
class Index(UI_main, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.description()

    def description(self):
        self.open_file.triggered.connect(self.f_open_file)
        self.delete_file.triggered.connect(self.f_delete_file)
        self.run.triggered.connect(self.f_run)
        self.info.triggered.connect(self.f_info)
        self.to_file.triggered.connect(self.f_to_file)
        self.create_file.triggered.connect(self.f_create_file)

    def f_open_file(self):
        dlg = OpenDialog(self)
        dlg.exec()

    def f_create_file(self):
        dlg = CreateDialog(self)
        dlg.exec()

    def f_delete_file(self):
        dlg = DeleteDialog(self)
        dlg.exec()
        dlg.con.close()

    def f_run(self):
        dlg = RunDialog(self)
        dlg.exec()

    def f_info(self):
        self.mb = QMessageBox(self)
        hbox = QHBoxLayout(self)
        hbox.addWidget(self.mb)
        self.mb.setWindowTitle('Возможности PyQTest')
        self.mb.setText(
            '''PyQTest - программа для создания тестов, викторин, квизов, интеллектуальных игр и т.д. Конструктор тестов позволяет создать викторину или квиз в тестовом формате, конструктор игр - игру в формате "Jeopardy"/"Своя игра". Результаты работы можно конвертировать в XLSX (таблицы Excel) или CSV. Вы также можете превратить файл CSV или XLSX в заданном формате в игру или тест PyQTest''')
        self.mb.show()

    def f_to_file(self):
        dlg = ExportDialog(self)
        dlg.exec()
