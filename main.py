import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from index import Index


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('media/app.ico'))
    ex = Index()
    ex.show()
    ex.setWindowIcon(QIcon('media/app.ico'))
    sys.excepthook = except_hook
    sys.exit(app.exec())
