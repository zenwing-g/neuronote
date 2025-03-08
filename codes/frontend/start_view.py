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

# Append the root directory to sys.path to access version information from a higher-level directory
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))
from version import VERSION  # Import the version number from a separate version module


class StartWindow(QMainWindow):
    # The main startup window for neuronote. It includes:
    # - A title label displaying the application name
    # - A search bar for user input
    # - A button to initiate a search/open action
    # - A version label positioned at the bottom-right
    def __init__(self):
        super().__init__()

        # Set window title and dimensions
        self.setWindowTitle("neuronote")
        self.resize(1000, 600)

        # Apply a dark theme
        self.setStyleSheet("background-color: black; color: white;")
        self.center_window()  # Center the window on screen

        # Create and configure the title label
        self.logo_text = QLabel("neuronote", self)
        self.logo_text.setStyleSheet("color: white; font-size: 100px")
        self.logo_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a label to display the version number in the bottom-right corner
        self.version_text = QLabel(f"{VERSION}", self)
        self.version_text.setStyleSheet("color: gray; font: 10px;")

        # Create a search bar with placeholder text
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search bag../")
        self.search_bar.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )  # Center text inside the search bar
        self.search_bar.setFocusPolicy(
            Qt.FocusPolicy.ClickFocus
        )  # Focus only when clicked

        # Create an open/search button
        self.open_button = QPushButton("Open", self)

        # Apply custom styles and arrange UI elements
        self.set_styles()
        self.adjust_layout()
        self.update_version_position()

    # Applies custom styles to the search bar and button.
    def set_styles(self):
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

    # Called when the window is shown; ensures layout is adjusted properly.
    def showEvent(self, event):
        super().showEvent(event)
        self.adjust_layout()
        self.search_bar.clearFocus()  # Ensure the search bar is not focused initially

    # Handles window resizing to maintain proper UI element positions.
    def resizeEvent(self, event):
        self.adjust_layout()
        self.update_version_position()
        super().resizeEvent(event)

    # Removes focus from the search bar if the user clicks outside of it.
    def mousePressEvent(self, event):
        if self.search_bar.hasFocus() and not self.search_bar.geometry().contains(
            event.pos()
        ):
            self.search_bar.clearFocus()
        super().mousePressEvent(event)

    # Dynamically positions UI elements based on window size.
    def adjust_layout(self):
        window_width, window_height = self.width(), self.height()

        # Position the title label near the top
        self.logo_text.adjustSize()
        label_width, label_height = self.logo_text.width(), self.logo_text.height()
        top_margin = window_height // 10  # Position 10% from the top
        self.logo_text.move((window_width - label_width) // 2, top_margin)

        # Set fixed sizes for search bar and button
        search_bar_width = 300
        button_width = 100
        search_height = 50
        self.search_bar.setFixedSize(search_bar_width, search_height)
        self.open_button.setFixedSize(button_width, search_height)

        # Dynamically adjust font sizes based on element height
        search_font = QApplication.font()
        search_font.setPointSize(int(search_height * 0.4))
        self.search_bar.setFont(search_font)
        self.open_button.setFont(search_font)

        # Position search bar and button below the title label
        total_width = search_bar_width + button_width + 10  # 10px spacing
        search_x = (window_width - total_width) // 2
        search_y = top_margin + label_height + 80  # Spacing below the title
        self.search_bar.move(search_x, search_y)
        self.open_button.move(search_x + search_bar_width + 10, search_y)  # 10px gap

    # Keeps the version label anchored to the bottom-right corner.
    def update_version_position(self):
        margin = 5  # Small margin from the edges
        self.version_text.adjustSize()
        x = self.width() - self.version_text.width() - margin
        y = self.height() - self.version_text.height() - margin
        self.version_text.move(x, y)

    # Centers the application window on the user's screen.
    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        window = self.frameGeometry()
        center_x = (screen.width() - window.width()) // 2
        center_y = (screen.height() - window.height()) // 2
        self.move(center_x, center_y)


# Application entry point
# Initializes and runs the application.
def main():
    app = QApplication(sys.argv)  # Create the application instance
    window = StartWindow()  # Create the main window
    window.show()  # Display the window
    sys.exit(app.exec())  # Run the application event loop


# Ensures the script runs only when executed directly
if __name__ == "__main__":
    main()
