import sys
import pathlib
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
)
from PyQt6.QtCore import Qt
from graph_view import (
    MovableViewport,
)  # Ensure graph_view.py is in the same directory or set up as module

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))
from version import VERSION


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("neuronote")
        self.resize(1000, 600)
        self.setStyleSheet("background-color: black; color: white;")
        self.center_window()

        self.logo_text = QLabel("neuronote", self)
        self.logo_text.setStyleSheet("font-size: 100px; color: white;")
        self.logo_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.version_text = QLabel(f"{VERSION}", self)
        self.version_text.setStyleSheet("color: gray; font-size: 10px;")

        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search ../")
        self.search_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.search_bar.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.search_bar.textChanged.connect(self.filter_folders)
        self.search_bar.focusInEvent = self.show_dropdown
        self.search_bar.focusOutEvent = self.hide_dropdown

        self.open_button = QPushButton("Open", self)
        self.open_button.clicked.connect(self.open_graph_view)

        self.dropdown_list = QListWidget(self)
        self.dropdown_list.setStyleSheet(
            "background-color: black; color: white; border: 1px solid white;"
        )
        self.dropdown_list.setVisible(False)
        self.dropdown_list.itemClicked.connect(self.select_folder)

        self.bag = pathlib.Path("../../storage/bag/")
        self.all_folders = sorted([f.name for f in self.bag.iterdir() if f.is_dir()])
        self.dropdown_list.addItems(self.all_folders)

        self.set_styles()
        self.adjust_layout()
        self.update_version_position()

    def open_graph_view(self):
        book_name = self.search_bar.text().strip()
        if book_name:
            self.graph_view = MovableViewport(book_name)
            self.graph_view.loadPages(book_name)
            self.graph_view.show()
            self.close()

    def show_dropdown(self, event):
        self.dropdown_list.setGeometry(
            self.search_bar.x(),
            self.search_bar.y() + self.search_bar.height(),
            self.search_bar.width(),
            150,
        )
        self.dropdown_list.setVisible(True)
        self.filter_folders()
        QLineEdit.focusInEvent(self.search_bar, event)

    def hide_dropdown(self, event):
        self.dropdown_list.setVisible(False)
        QLineEdit.focusOutEvent(self.search_bar, event)

    def filter_folders(self):
        search_text = self.search_bar.text().strip().lower()
        self.dropdown_list.clear()
        matches = [f for f in self.all_folders if search_text in f.lower()]
        self.dropdown_list.addItems(matches)

    def select_folder(self, item):
        self.search_bar.setText(item.text())
        self.dropdown_list.setVisible(False)

    def set_styles(self):
        self.search_bar.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid white;
                border-radius: 10px;
                padding: 10px;
                background-color: black;
                color: white;
                font-size: 20px;
            }
        """
        )
        self.open_button.setStyleSheet(
            """
            QPushButton {
                border: 2px solid white;
                border-radius: 10px;
                padding: 10px;
                background-color: white;
                color: black;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: gray;
                color: white;
            }
        """
        )

    def adjust_layout(self):
        self.logo_text.adjustSize()
        w, h = self.width(), self.height()
        lw, lh = self.logo_text.width(), self.logo_text.height()
        top_margin = h // 10

        self.logo_text.move((w - lw) // 2, top_margin)

        search_width, btn_width, height = 300, 100, 50
        total_width = search_width + btn_width + 10
        sx = (w - total_width) // 2
        sy = top_margin + lh + 80

        self.search_bar.setFixedSize(search_width, height)
        self.search_bar.move(sx, sy)
        self.open_button.setFixedSize(btn_width, height)
        self.open_button.move(sx + search_width + 10, sy)

    def update_version_position(self):
        margin = 5
        self.version_text.adjustSize()
        x = self.width() - self.version_text.width() - margin
        y = self.height() - self.version_text.height() - margin
        self.version_text.move(x, y)

    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        frame = self.frameGeometry()
        self.move(
            (screen.width() - frame.width()) // 2,
            (screen.height() - frame.height()) // 2,
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = StartWindow()
    win.show()
    sys.exit(app.exec())
