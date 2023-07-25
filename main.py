import sys
from PyQt6.QtWidgets import QApplication

from gui import GUI
from sovellus import Sovellus


def main():
    sovellus = Sovellus()

    global app
    app = QApplication(sys.argv)
    gui = GUI(sovellus)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

