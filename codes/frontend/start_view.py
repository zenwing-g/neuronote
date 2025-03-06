import sys
from PyQt6.QtWidgets import QLabel, QLineEdit, QMainWindow, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("neuronote.")
        self.resize(1000, 600)  # Allows resizing

        self.setStyleSheet("background-color: black; color: white;")
        self.center_window()

        # Create the label (title)
        self.logo_text = QLabel("neuronote.", self)
        self.logo_text.setStyleSheet("color: white;")
        self.logo_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set fixed font size for label
        label_font = QApplication.font()
        label_font.setPointSize(100)  # Keep label font size constant
        self.logo_text.setFont(label_font)

        # Create the search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search bag../")
        self.search_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Allow focus on click but not auto-focus
        self.search_bar.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

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

        self.adjust_layout()  # Set initial sizes and positions

    def showEvent(self, event):
        """Ensure correct font size on first display and remove focus from search bar."""
        super().showEvent(event)
        self.adjust_layout()  # Resize font properly after window is shown
        self.search_bar.clearFocus()  # Ensure placeholder is visible

    def resizeEvent(self, event):
        """Called automatically when the window is resized."""
        self.adjust_layout()
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        """Remove focus from search bar if clicking outside of it."""
        if self.search_bar.hasFocus() and not self.search_bar.geometry().contains(
            event.pos()
        ):
            self.search_bar.clearFocus()
        super().mousePressEvent(event)

    def adjust_layout(self):
        """Adjusts search bar font size and positioning dynamically based on window size."""
        window_width = self.width()
        window_height = self.height()

        # Resize label to fit text (but font remains fixed)
        self.logo_text.adjustSize()
        label_width = self.logo_text.width()
        label_height = self.logo_text.height()

        # Compute y position to maintain 1:3 ratio
        top_margin = window_height // 10
        center_x = (window_width - label_width) // 2
        self.logo_text.move(center_x, top_margin)

        # Set search bar size dynamically (max width: 400px)
        search_width = min(400, window_width - 100)
        search_height = 50
        self.search_bar.setFixedSize(search_width, search_height)

        # Adjust font size of search bar dynamically (keep it readable)
        search_font = QApplication.font()
        search_font.setPointSize(int(search_height * 0.4))  # 40% of search bar height
        self.search_bar.setFont(search_font)

        # Position the search bar below the label
        search_x = (window_width - search_width) // 2
        search_y = top_margin + label_height + 30
        self.search_bar.move(search_x, search_y)

    def center_window(self):
        """Centers the window on the screen."""
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
