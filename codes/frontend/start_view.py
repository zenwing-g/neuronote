import sys
from PyQt6.QtWidgets import QLabel, QLineEdit, QMainWindow, QApplication
from PyQt6.QtCore import Qt


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # Initialize the parent QMainWindow

        self.setWindowTitle("neuronote.")  # Set the window title
        self.resize(1000, 600)  # Set initial window size

        # Set window background to black and text color to white
        self.setStyleSheet("background-color: black; color: white;")
        self.center_window()  # Center the window on the screen

        # Create the label (title)
        self.logo_text = QLabel("neuronote.", self)
        self.logo_text.setStyleSheet("color: white;")  # Set label text color to white
        self.logo_text.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )  # Center the label text

        # Set fixed font size for the label
        label_font = QApplication.font()
        label_font.setPointSize(100)  # Large font size for the title
        self.logo_text.setFont(label_font)

        # Create the search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search bag../")  # Set placeholder text
        self.search_bar.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )  # Center text inside search bar

        # Allow focus when clicked and remove focus when clicked elsewhere
        self.search_bar.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        # Set search bar styling
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
        self.adjust_layout()  # Recalculate layout based on new size
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

        # Compute y position to maintain 1:10 margin from the top
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
        screen = QApplication.primaryScreen().geometry()  # Get screen size
        window = self.frameGeometry()  # Get current window size

        # Compute center position
        center_x = (screen.width() - window.width()) // 2
        center_y = (screen.height() - window.height()) // 2
        self.move(center_x, center_y)  # Move window to center


def main():
    """Entry point for the application."""
    app = QApplication(sys.argv)  # Initialize the application
    window = StartWindow()  # Create main window instance
    window.show()  # Show the main window
    sys.exit(app.exec())  # Start event loop


if __name__ == "__main__":
    main()  # Run the application
