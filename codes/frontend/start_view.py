import sys
import pathlib
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QScrollArea,
)
from PyQt6.QtCore import Qt

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

        # Title label
        self.logo_text = QLabel("neuronote", self)
        self.logo_text.setStyleSheet("color: white; font-size: 100px;")
        self.logo_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Version label (bottom-right)
        self.version_text = QLabel(f"{VERSION}", self)
        self.version_text.setStyleSheet("color: gray; font: 10px;")

        # Search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search bag../")
        self.search_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.search_bar.setFocusPolicy(
            Qt.FocusPolicy.ClickFocus
        )  # Focus only when clicked
        self.search_bar.textChanged.connect(self.filter_folders)
        self.search_bar.focusInEvent = self.show_scroll_area
        self.search_bar.focusOutEvent = self.hide_scroll_area

        # Open button
        self.open_button = QPushButton("Open", self)

        # Scrollable area for folder list (initially hidden)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")
        self.scroll_area.setVisible(False)

        # Widget & Layout inside the scroll area
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)

        # Load all folders from storage/bag
        self.bag = pathlib.Path("../../storage/bag/")
        self.all_folders = [folder for folder in self.bag.iterdir() if folder.is_dir()]
        self.load_folders(self.all_folders)

        self.scroll_area.setWidget(self.scroll_widget)

        # Apply styles and layout positioning
        self.set_styles()
        self.adjust_layout()
        self.update_version_position()

    def show_scroll_area(self, event):
        """Show folder list when search bar is focused."""
        self.scroll_area.setVisible(True)
        QLineEdit.focusInEvent(self.search_bar, event)

    def hide_scroll_area(self, event):
        """Hide folder list when search bar loses focus."""
        self.scroll_area.setVisible(False)
        QLineEdit.focusOutEvent(self.search_bar, event)

    def load_folders(self, folders):
        """Load folder names into the scroll area."""
        # Clear existing folder labels before adding new ones
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().deleteLater()

        # If there are no folders, do nothing (prevents recursion error)
        if not folders:
            return

        # Add folders as clickable labels
        for folder in folders:
            label = QLabel(folder.name)
            label.setStyleSheet("color: white; font-size: 20px; padding: 5px;")
            label.mousePressEvent = lambda event, folder=folder: self.folder_clicked(
                folder
            )
            self.scroll_layout.addWidget(label)

    def filter_folders(self):
        """Filter folder list based on search query."""
        search_text = self.search_bar.text().strip().lower()
        if not search_text:
            self.load_folders(self.all_folders)
            return

        # Show only folders that match the search text
        filtered_folders = [
            folder for folder in self.all_folders if search_text in folder.name.lower()
        ]
        self.load_folders(filtered_folders)

    def folder_clicked(self, folder):
        """When a folder is clicked, display its subfolders (without overwriting the main list)."""
        self.search_bar.setText(str(folder))  # Show selected folder in search bar
        sub_folders = [sub for sub in folder.iterdir() if sub.is_dir()]
        self.load_folders(
            sub_folders
        )  # Load only subfolders without modifying self.all_folders

    def set_styles(self):
        """Set styles for UI elements."""
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
        """Recalculate layout when window becomes visible."""
        super().showEvent(event)
        self.adjust_layout()
        self.search_bar.clearFocus()

    def resizeEvent(self, event):
        """Adjust layout when window is resized."""
        self.adjust_layout()
        self.update_version_position()
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        """Remove search bar focus if user clicks outside of it."""
        if self.search_bar.hasFocus() and not self.search_bar.geometry().contains(
            event.pos()
        ):
            self.search_bar.clearFocus()
        super().mousePressEvent(event)

    def adjust_layout(self):
        """Position UI elements dynamically based on window size."""
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

        # Adjust font size
        search_font = QApplication.font()
        search_font.setPointSize(int(search_height * 0.4))
        self.search_bar.setFont(search_font)
        self.open_button.setFont(search_font)

        # Position search bar & button
        total_width = search_bar_width + button_width + 10
        search_x = (window_width - total_width) // 2
        search_y = top_margin + label_height + 80
        self.search_bar.move(search_x, search_y)
        self.open_button.move(search_x + search_bar_width + 10, search_y)

        self.adjust_scroll_area()

    def adjust_scroll_area(self):
        """Position the scroll area below the search bar."""
        window_width, window_height = self.width(), self.height()
        scroll_width, scroll_height = 300, 200
        scroll_x = (window_width - scroll_width) // 2
        scroll_y = self.search_bar.y() + self.search_bar.height() + 20
        self.scroll_area.setGeometry(scroll_x, scroll_y, scroll_width, scroll_height)

    def update_version_position(self):
        """Position the version text in the bottom-right corner."""
        margin = 5
        self.version_text.adjustSize()
        x = self.width() - self.version_text.width() - margin
        y = self.height() - self.version_text.height() - margin
        self.version_text.move(x, y)

    def center_window(self):
        """Center the window on the screen."""
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
