from PyQt5.QtWidgets import QApplication
from app.launch_screen import LaunchScreen
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LaunchScreen()
    window.show()
    sys.exit(app.exec_())
