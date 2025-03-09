import sys
from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QMainWindow,
    QApplication,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QScrollArea,
)
from PyQt6.QtCore import Qt
import pathlib

# Add the root directory to sys.path to allow importing version information
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))
from version import VERSION  # Import the version number


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("neuronote")
        self.resize(1000, 600)
        self.setStyleSheet("background-color: black; color: white;")
        self.center_window()  # Position the window at the center of the screen

        # Main title label
        self.logo_text = QLabel("neuronote", self)
        self.logo_text.setStyleSheet("color: white; font-size: 100px")
        self.logo_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Version number displayed in the bottom-right corner
        self.version_text = QLabel(f"{VERSION}", self)
        self.version_text.setStyleSheet("color: gray; font: 10px;")

        # Search bar for filtering folders
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search bag../")
        self.search_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.search_bar.setFocusPolicy(
            Qt.FocusPolicy.ClickFocus
        )  # Only focus when clicked
        self.search_bar.textChanged.connect(self.filter_folders)
        self.search_bar.focusInEvent = self.show_scroll_area
        self.search_bar.focusOutEvent = self.hide_scroll_area

        # Open button placed next to the search bar
        self.open_button = QPushButton("Open", self)

        # Scrollable area for displaying folder names, initially hidden
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")
        self.scroll_area.setVisible(False)

        # Container for folder labels inside the scroll area
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)

        # Load all available folders inside the "bag" directory
        self.bag = pathlib.Path("../../storage/bag/")
        self.all_folders = [folder for folder in self.bag.iterdir() if folder.is_dir()]
        self.load_folders(self.all_folders)

        self.scroll_area.setWidget(self.scroll_widget)

        # Apply styles, set up layout, and position elements
        self.set_styles()
        self.adjust_layout()
        self.update_version_position()

    def show_scroll_area(self, event):
        # Display the folder list when the search bar gains focus
        self.scroll_area.setVisible(True)
        QLineEdit.focusInEvent(self.search_bar, event)

    def hide_scroll_area(self, event):
        # Hide the folder list when the search bar loses focus
        self.scroll_area.setVisible(False)
        QLineEdit.focusOutEvent(self.search_bar, event)

    def load_folders(self, folders):
        # Remove existing folder labels before updating
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().deleteLater()

        # If no folders match the search, reload the full list
        if not folders:
            self.load_folders(self.all_folders)
            return

        # Create labels for each folder and add them to the layout
        for folder in folders:
            label = QLabel(folder.name)
            label.setStyleSheet("color: white; font-size: 20px; padding: 5px;")
            label.mousePressEvent = lambda event, folder=folder: self.folder_clicked(
                folder
            )
            self.scroll_layout.addWidget(label)

    def filter_folders(self):
        # Update folder list based on search query
        search_text = self.search_bar.text().strip().lower()
        if not search_text:
            self.load_folders(self.all_folders)
            return

        # Filter folders that contain the search text
        filtered_folders = [
            folder for folder in self.all_folders if search_text in folder.name.lower()
        ]
        self.load_folders(filtered_folders)

    def folder_clicked(self, folder):
        # Update the search bar with the selected folder path
        self.search_bar.setText(str(folder))
        # Load subfolders when a folder is clicked
        self.all_folders = [sub for sub in folder.iterdir() if sub.is_dir()]
        self.load_folders(self.all_folders)

    def set_styles(self):
        # Apply styles to the search bar
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

        # Apply styles to the open button
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
        # Recalculate layout when the window becomes visible
        super().showEvent(event)
        self.adjust_layout()
        self.search_bar.clearFocus()

    def resizeEvent(self, event):
        # Adjust layout when the window is resized
        self.adjust_layout()
        self.update_version_position()
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        # Clear search bar focus if the user clicks outside of it
        if self.search_bar.hasFocus() and not self.search_bar.geometry().contains(
            event.pos()
        ):
            self.search_bar.clearFocus()
        super().mousePressEvent(event)

    def adjust_layout(self):
        # Calculate window dimensions
        window_width, window_height = self.width(), self.height()

        # Center the main title
        self.logo_text.adjustSize()
        label_width, label_height = self.logo_text.width(), self.logo_text.height()
        top_margin = window_height // 10
        self.logo_text.move((window_width - label_width) // 2, top_margin)

        # Set dimensions for search bar and open button
        search_bar_width = 300
        button_width = 100
        search_height = 50
        self.search_bar.setFixedSize(search_bar_width, search_height)
        self.open_button.setFixedSize(button_width, search_height)

        # Adjust font size based on the search bar height
        search_font = QApplication.font()
        search_font.setPointSize(int(search_height * 0.4))
        self.search_bar.setFont(search_font)
        self.open_button.setFont(search_font)

        # Position search bar and open button
        total_width = search_bar_width + button_width + 10
        search_x = (window_width - total_width) // 2
        search_y = top_margin + label_height + 80
        self.search_bar.move(search_x, search_y)
        self.open_button.move(search_x + search_bar_width + 10, search_y)

        self.adjust_scroll_area()

    def adjust_scroll_area(self):
        # Position the scroll area below the search bar
        window_width, window_height = self.width(), self.height()
        scroll_width, scroll_height = 300, 200
        scroll_x = (window_width - scroll_width) // 2
        scroll_y = self.search_bar.y() + self.search_bar.height() + 20
        self.scroll_area.setGeometry(scroll_x, scroll_y, scroll_width, scroll_height)

    def update_version_position(self):
        # Position the version number in the bottom-right corner
        margin = 5
        self.version_text.adjustSize()
        x = self.width() - self.version_text.width() - margin
        y = self.height() - self.version_text.height() - margin
        self.version_text.move(x, y)

    def center_window(self):
        # Center the window on the screen
        screen = QApplication.primaryScreen().geometry()
        window = self.frameGeometry()
        self.move(
            (screen.width() - window.width()) // 2,
            (screen.height() - window.height()) // 2,
        )


def main():
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
