import sys

from PySide6.QtWidgets import QApplication

from mahoyo_patcher.gui import Window


def main() -> int:
    app: QApplication = QApplication(sys.argv)
    window: Window = Window()
    window.show()
    return app.exec()
