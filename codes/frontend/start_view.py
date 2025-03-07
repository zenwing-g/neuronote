import sys
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QMainWindow,
    QApplication,
    QPushButton,
)
from PyQt6.QtCore import Qt
import pathlib

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))
from version import VERSION


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("neuronote")
        self.resize(1000, 600)

        self.setStyleSheet("background-color: black; color: white;")
        self.center_window()

        # Title Label
        self.logo_text = QLabel("neuronote", self)
        self.logo_text.setStyleSheet("color: white; font-size: 100px")
        self.logo_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Version Label (Bottom-Right)
        self.version_text = QLabel(f"{VERSION}", self)
        self.version_text.setStyleSheet("color: gray; font: 10px;")

        # Search Bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search bag../")
        self.search_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.search_bar.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        # Search Button
        self.open_button = QPushButton("Open", self)

        self.set_styles()
        self.adjust_layout()
        self.update_version_position()

    def set_styles(self):
        """Sets styles for search bar and button."""
        self.search_bar.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid white;
                border-radius: 10px;
                padding: 10px;
                background-color: black;
                color: white;
                selection-background-color: gray;
                font: 20px;
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
                font: 20px;
            }
            QPushButton:hover {
                background-color: gray;
                color: white;
            }
        """
        )

    def showEvent(self, event):
        super().showEvent(event)
        self.adjust_layout()
        self.search_bar.clearFocus()

    def resizeEvent(self, event):
        self.adjust_layout()
        self.update_version_position()
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        """Remove focus when clicking outside."""
        if self.search_bar.hasFocus() and not self.search_bar.geometry().contains(
            event.pos()
        ):
            self.search_bar.clearFocus()
        super().mousePressEvent(event)

    def adjust_layout(self):
        """Positions title, search bar, and button with fixed sizes."""
        window_width, window_height = self.width(), self.height()

        # Adjust title label
        self.logo_text.adjustSize()
        label_width, label_height = self.logo_text.width(), self.logo_text.height()
        top_margin = window_height // 10
        self.logo_text.move((window_width - label_width) // 2, top_margin)

        # Fixed search bar and button sizes
        search_bar_width = 300
        button_width = 100
        search_height = 50

        self.search_bar.setFixedSize(search_bar_width, search_height)
        self.open_button.setFixedSize(button_width, search_height)

        # Match font size
        search_font = QApplication.font()
        search_font.setPointSize(int(search_height * 0.4))
        self.search_bar.setFont(search_font)
        self.open_button.setFont(search_font)

        # Center both elements (fixed position) with more spacing
        total_width = search_bar_width + button_width + 10  # 10px gap
        search_x = (window_width - total_width) // 2
        search_y = top_margin + label_height + 80  # Increased spacing

        self.search_bar.move(search_x, search_y)
        self.open_button.move(search_x + search_bar_width + 10, search_y)  # 10px gap

    def update_version_position(self):
        """Keeps version label at bottom-right."""
        margin = 5
        self.version_text.adjustSize()
        x = self.width() - self.version_text.width() - margin
        y = self.height() - self.version_text.height() - margin
        self.version_text.move(x, y)

    def center_window(self):
        """Centers the window on screen."""
        screen = QApplication.primaryScreen().geometry()
        window = self.frameGeometry()
        center_x = (screen.width() - window.width()) // 2
        center_y = (screen.height() - window.height()) // 2
        self.move(center_x, center_y)


def main():
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
