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
from graph_view import MovableViewport  # Import the graph view window

# Add the root directory to sys.path to allow importing version information
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))
from version import VERSION  # Import the version number


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("neuronote")
        self.resize(1000, 600)
        self.setStyleSheet("background-color: black; color: white;")
        self.center_window()

        # Title label
        self.logo_text = QLabel("neuronote", self)
        self.logo_text.setStyleSheet("color: white; font-size: 100px;")
        self.logo_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Version label (bottom-right)
        self.version_text = QLabel(f"{VERSION}", self)
        self.version_text.setStyleSheet("color: gray; font: 10px;")

        # Search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search ../")
        self.search_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.search_bar.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.search_bar.textChanged.connect(self.filter_folders)
        self.search_bar.focusInEvent = self.show_dropdown
        self.search_bar.focusOutEvent = self.hide_dropdown

        # Open button
        self.open_button = QPushButton("Open", self)
        self.open_button.clicked.connect(self.open_graph_view)

        # Dropdown list for folder selection
        self.dropdown_list = QListWidget(self)
        self.dropdown_list.setStyleSheet(
            "background-color: black; color: white; border: 1px solid white;"
        )
        self.dropdown_list.setVisible(False)
        self.dropdown_list.itemClicked.connect(self.select_folder)

        # Load all folders from storage/bag
        self.bag = pathlib.Path("../../storage/bag/")
        self.all_folders = sorted(
            [folder.name for folder in self.bag.iterdir() if folder.is_dir()]
        )
        self.dropdown_list.addItems(self.all_folders)

        # Apply styles and layout positioning
        self.set_styles()
        self.adjust_layout()
        self.update_version_position()

    def open_graph_view(self):
        """Open the graph view window with the book name from the search bar."""
        book_name = self.search_bar.text().strip()
        if book_name:
            self.graph_view = MovableViewport(book_name)
            self.graph_view.loadPages(book_name)  # Load pages after opening the window
            self.graph_view.show()

    def show_dropdown(self, event):
        """Show dropdown list when search bar is focused."""
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
        """Hide dropdown list when focus is lost."""
        self.dropdown_list.setVisible(False)
        QLineEdit.focusOutEvent(self.search_bar, event)

    def filter_folders(self):
        """Dynamically arrange dropdown list based on search query."""
        search_text = self.search_bar.text().strip().lower()
        self.dropdown_list.clear()
        filtered_folders = sorted(
            [folder for folder in self.all_folders if search_text in folder.lower()]
        )
        self.dropdown_list.addItems(filtered_folders)

    def select_folder(self, item):
        """Set the search bar text when a folder is selected from dropdown."""
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

    def adjust_layout(self):
        window_width, window_height = self.width(), self.height()

        # Center the title
        self.logo_text.adjustSize()
        label_width, label_height = self.logo_text.width(), self.logo_text.height()
        top_margin = window_height // 10
        self.logo_text.move((window_width - label_width) // 2, top_margin)

        # Set dimensions for search bar and button
        search_bar_width = 300
        button_width = 100
        search_height = 50
        self.search_bar.setFixedSize(search_bar_width, search_height)
        self.open_button.setFixedSize(button_width, search_height)

        # Position search bar & button
        total_width = search_bar_width + button_width + 10
        search_x = (window_width - total_width) // 2
        search_y = top_margin + label_height + 80
        self.search_bar.move(search_x, search_y)
        self.open_button.move(search_x + search_bar_width + 10, search_y)

    def update_version_position(self):
        margin = 5
        self.version_text.adjustSize()
        x = self.width() - self.version_text.width() - margin
        y = self.height() - self.version_text.height() - margin
        self.version_text.move(x, y)

    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        window = self.frameGeometry()
        self.move(
            (screen.width() - window.width()) // 2,
            (screen.height() - window.height()) // 2,
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec())
