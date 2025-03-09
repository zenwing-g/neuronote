import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import QPropertyAnimation, Qt, QPoint, QPointF, QTimer, QRect
from PyQt6.QtGui import QPainter, QBrush, QPen, QFont


class MovableViewport(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graph View")
        self.resize(800, 600)
        self.setMouseTracking(True)

        # Navbar starts hidden and appears when the mouse moves near the top
        self.navbar = QWidget(self)
        self.navbar.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.navbar.setFixedHeight(50)
        self.navbar.setGeometry(
            0, -50, self.width(), 50
        )  # Initially hidden above the viewport

        # Layout for the navbar (horizontal arrangement for buttons and title)
        navbar_layout = QHBoxLayout()
        navbar_layout.setContentsMargins(10, 0, 10, 0)
        self.navbar.setLayout(navbar_layout)

        # Back button on the left side of the navbar
        self.back_button = QPushButton("Back", self.navbar)
        self.back_button.setFixedSize(80, 40)
        self.back_button.setStyleSheet("font-size: 16px;")
        self.back_button.clicked.connect(self.go_back)
        navbar_layout.addWidget(self.back_button)
        navbar_layout.addStretch()  # Adds spacing between elements

        # Title label in the center of the navbar
        self.title_label = QLabel("Graph View", self.navbar)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("color: white; font-size: 16px;")
        navbar_layout.addWidget(self.title_label)
        navbar_layout.addStretch()

        # "New Label" button on the right side of the navbar
        self.new_page_button = QPushButton("New Label", self.navbar)
        self.new_page_button.setFixedSize(100, 40)
        self.new_page_button.setStyleSheet(
            "border-radius: 10px; color: black; background-color: white; padding: 5px 10px;"
        )
        navbar_layout.addWidget(self.new_page_button)

        # Timer to hide navbar after 2 seconds of inactivity
        self.navbar_timer = QTimer()
        self.navbar_timer.setInterval(2000)
        self.navbar_timer.timeout.connect(self.hide_navbar)

        # Smooth animation for navbar sliding in and out
        self.navbar_animation = QPropertyAnimation(self.navbar, b"geometry")
        self.navbar_animation.setDuration(200)

        # Variables for tracking mouse panning
        self.dragging = False
        self.last_mouse_pos = QPoint()

        # Grid settings
        self.min_spacing = 40
        self.max_spacing = 70
        self.grid_spacing = 50
        self.zoom_step = 5

        # Offset determines the current pan position of the viewport
        self.offset = QPointF(0, 0)

    def go_back(self):
        # Closes the current window and starts start_view.py
        subprocess.Popen(["python3", "start_view.py"])
        self.close()

    def show_navbar(self):
        # Moves the navbar down into view when activated
        self.navbar_animation.stop()
        self.navbar_animation.setStartValue(QRect(0, -50, self.width(), 50))
        self.navbar_animation.setEndValue(QRect(0, 0, self.width(), 50))
        self.navbar_animation.start()
        self.navbar_timer.start()  # Restart the timer to hide it later

    def hide_navbar(self):
        # Moves the navbar back up if the mouse isn't over it
        if not self.navbar.underMouse():
            self.navbar_animation.stop()
            self.navbar_animation.setStartValue(QRect(0, 0, self.width(), 50))
            self.navbar_animation.setEndValue(QRect(0, -50, self.width(), 50))
            self.navbar_animation.start()
            self.navbar_timer.stop()

    def paintEvent(self, event):
        # Handles rendering of the graph with grid dots
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Fill the background with black
        painter.fillRect(self.rect(), QBrush(Qt.GlobalColor.black))

        # Calculate the center dot position based on current pan offset
        center_x = self.width() // 2 + int(self.offset.x())
        center_y = self.height() // 2 + int(self.offset.y())

        # Set pen for regular grid dots (dark gray, 1px)
        dot_pen = QPen(Qt.GlobalColor.darkGray)
        dot_pen.setWidth(1)
        painter.setPen(dot_pen)

        # Calculate starting positions for rendering the grid
        start_x = (center_x % self.grid_spacing) - self.grid_spacing
        start_y = (center_y % self.grid_spacing) - self.grid_spacing

        # Draw grid dots across the viewport
        for x in range(start_x, self.width(), self.grid_spacing):
            for y in range(start_y, self.height(), self.grid_spacing):
                if x == center_x and y == center_y:
                    continue  # Skip center dot, it will be drawn separately
                painter.drawPoint(QPoint(x, y))  # 1-pixel dark gray dot

        # Draw the center dot (2px wide, white)
        center_dot_pen = QPen(Qt.GlobalColor.white)
        center_dot_pen.setWidth(2)
        painter.setPen(center_dot_pen)
        painter.drawPoint(QPoint(center_x, center_y))

        # Label the center dot with "(0x0)" slightly below it
        font = QFont()
        font.setPixelSize(8)
        painter.setFont(font)
        painter.drawText(center_x - 10, center_y + 12, "(0x0)")

    def mouseMoveEvent(self, event):
        # Handles panning and detects when the navbar should appear
        if event.pos().y() < 20 or self.navbar.underMouse():
            self.show_navbar()

        if self.dragging:
            delta = event.pos() - self.last_mouse_pos
            self.offset += QPointF(delta.x(), delta.y())
            self.last_mouse_pos = event.pos()
            self.update()

    def mousePressEvent(self, event):
        # Detects left mouse button press to start dragging
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.last_mouse_pos = event.pos()

    def mouseReleaseEvent(self, event):
        # Stops dragging when the left mouse button is released
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False

    def wheelEvent(self, event):
        # Handles zooming in and out by adjusting grid spacing
        angle = event.angleDelta().y()
        new_spacing = self.grid_spacing + (
            self.zoom_step if angle > 0 else -self.zoom_step
        )
        if self.min_spacing <= new_spacing <= self.max_spacing:
            self.grid_spacing = new_spacing
            self.update()


# Start the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovableViewport()
    window.show()
    sys.exit(app.exec())
