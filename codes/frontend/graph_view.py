import sys
import pathlib
import json
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt6.QtCore import (
    Qt,
    QPoint,
    QPointF,
    QTimer,
    QPropertyAnimation,
    QEasingCurve,
)
from PyQt6.QtGui import QMouseEvent, QPainter, QBrush, QPen, QFont

# Add the root directory to sys.path to allow importing version information
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))
from version import VERSION  # Import the version number


class MovableViewport(QWidget):
    def __init__(self, book_name="Unknown Book"):
        super().__init__()
        self.setWindowTitle(book_name)
        self.resize(800, 600)
        self.setMouseTracking(True)
        self.book_name = book_name

        # Navbar visibility tracking
        self.navbar_visible = False
        self.navbar_timer = QTimer(self)
        self.navbar_timer.setInterval(500)
        self.navbar_timer.timeout.connect(self.hide_navbar)

        self.labels = []

        # Navbar container
        self.navbar = QWidget(self)
        self.navbar.setStyleSheet(
            "background-color: black; border: 2px solid white; border-radius: 8px;"
        )
        self.navbar.setFixedHeight(40)
        self.navbar.move(0, -40)  # Start hidden above the window

        # Animation for navbar
        self.navbar_animation = QPropertyAnimation(self.navbar, b"pos")
        self.navbar_animation.setDuration(200)  # Smooth animation
        self.navbar_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Back button (default PyQt style)
        self.back_button = QPushButton("Back", self.navbar)
        self.back_button.setFixedSize(60, 30)

        # Book name label
        self.book_label = QLabel(self.book_name, self.navbar)
        self.book_label.setStyleSheet(
            "color: white; font-size: 14px; background: none;"
        )
        self.book_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Coordinate label
        self.coord_label = QLabel(self)
        self.coord_label.setStyleSheet(
            "color: white; background-color: black; padding: 2px; border-radius: 3px;"
        )
        font = QFont()
        font.setPixelSize(9)
        self.coord_label.setFont(font)
        self.coord_label.hide()

        # Panning variables
        self.dragging = False
        self.last_mouse_pos = QPoint()

        # Grid settings
        self.grid_spacing = 50
        self.offset = QPointF(0, 0)

        # Store dot positions
        self.dot_positions = {}

        # Version label
        self.version_text = QLabel(f"{VERSION}", self)
        self.version_text.setStyleSheet("color: gray; font: 10px;")
        self.update_version_position()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QBrush(Qt.GlobalColor.black))

        # Get center position
        center_x = self.width() // 2 + int(self.offset.x())
        center_y = self.height() // 2 + int(self.offset.y())

        # Store dot positions
        self.dot_positions.clear()
        start_x = (center_x % self.grid_spacing) - self.grid_spacing
        start_y = (center_y % self.grid_spacing) - self.grid_spacing

        for x in range(start_x, self.width(), self.grid_spacing):
            for y in range(start_y, self.height(), self.grid_spacing):
                rel_x = (x - center_x) // self.grid_spacing
                rel_y = (center_y - y) // self.grid_spacing
                self.dot_positions[(x, y)] = (rel_x, rel_y)
                painter.setPen(QPen(Qt.GlobalColor.darkGray, 1))
                painter.drawPoint(QPoint(x, y))

        # Draw center dot
        painter.setPen(QPen(Qt.GlobalColor.white, 2))
        painter.drawPoint(QPoint(center_x, center_y))

    def mouseMoveEvent(self, event):
        if self.dragging:
            delta = event.pos() - self.last_mouse_pos
            self.offset += QPointF(delta.x(), delta.y())  # Update viewport offset
            self.last_mouse_pos = event.pos()

            # Move all labels based on updated offset
            for label, rel_pos in self.labels:
                label.move((self.offset + rel_pos).toPoint())

            self.update()
            return

    def show_navbar(self):
        if not self.navbar_visible:
            self.navbar_visible = True
            self.adjust_navbar()
            self.navbar_animation.setStartValue(self.navbar.pos())
            self.navbar_animation.setEndValue(QPoint(0, 0))
            self.navbar_animation.start()

    def hide_navbar(self):
        if self.navbar_visible:
            self.navbar_visible = False
            self.navbar_animation.setStartValue(self.navbar.pos())
            self.navbar_animation.setEndValue(QPoint(0, -40))
            self.navbar_animation.start()

    def adjust_navbar(self):
        self.navbar.setGeometry(0, 0, self.width(), 40)
        self.back_button.move(10, 5)
        self.book_label.setGeometry((self.width() // 2) - 100, 5, 200, 30)

    def resizeEvent(self, event):
        self.update_version_position()
        self.adjust_navbar()
        super().resizeEvent(event)

    def update_version_position(self):
        margin = 5
        self.version_text.adjustSize()
        x = self.width() - self.version_text.width() - margin
        y = self.height() - self.version_text.height() - margin
        self.version_text.move(x, y)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.last_mouse_pos = event.pos()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False

    def loadPages(self, book_name):
        book_path = pathlib.Path(f"../../storage/bag/{book_name}")
        print(f"Loading pages from: {book_path}")

        extension = ".json"
        pages = list(book_path.glob(f"*{extension}"))

        # Get the center of the viewport as the reference point
        viewport_center_x = self.width() // 2
        viewport_center_y = self.height() // 2

        for page in pages:
            print(f"Reading: {page.name}")
            with page.open("r", encoding="utf-8") as node:
                data = json.load(node)

                node_title = data.get("page_title", "Untitled Page")
                location_data = data.get("page_location", {"x": 0, "y": 0})

                node_x = location_data.get("x", 0)
                node_y = location_data.get("y", 0)

                # Adjust position so (0,0) aligns with the viewport center
                adjusted_x = viewport_center_x + node_x
                adjusted_y = viewport_center_y - node_y  # Invert Y-axis if needed

                print(
                    f"Creating label '{node_title}' at adjusted ({adjusted_x}, {adjusted_y})"
                )  # Debug

                label = QLabel(node_title, self)
                label.setStyleSheet(
                    "color: white; background-color: black; border: 1px solid white; padding: 3px;"
                )
                label.adjustSize()
                label.move(adjusted_x, adjusted_y)  # Move relative to viewport center
                label.show()

                self.labels.append((label, QPointF(adjusted_x, adjusted_y)))

        self.update()  # Refresh UI


if __name__ == "__main__":
    app = QApplication(sys.argv)
    book_name = "Example Book"  # Replace with actual book name from start_view.py
    window = MovableViewport(book_name)
    window.show()
    sys.exit(app.exec())
