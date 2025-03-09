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
from PyQt6.QtGui import QPainter, QBrush


class MovableViewport(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graph View")
        self.resize(800, 600)
        self.setMouseTracking(True)

        # Create and configure the navigation bar.
        self.navbar = QWidget(self)
        self.navbar.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.navbar.setFixedHeight(50)
        self.navbar.setGeometry(0, -50, self.width(), 50)  # Initially hidden

        # Layout for the navbar
        navbar_layout = QHBoxLayout()
        navbar_layout.setContentsMargins(10, 0, 10, 0)
        self.navbar.setLayout(navbar_layout)

        # Back button for navigation
        self.back_button = QPushButton("Back", self.navbar)
        self.back_button.setFixedSize(80, 40)
        self.back_button.setStyleSheet("font-size: 16px;")
        self.back_button.clicked.connect(self.go_back)  # Connect back button
        navbar_layout.addWidget(self.back_button)
        navbar_layout.addStretch()

        # Title label in the navbar
        self.title_label = QLabel("Book_name_placeholder", self.navbar)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("color: white; font-size: 16px;")
        navbar_layout.addWidget(self.title_label)
        navbar_layout.addStretch()

        # Button to create a new label/page
        self.new_page_button = QPushButton("New Label", self.navbar)
        self.new_page_button.setFixedSize(100, 40)
        self.new_page_button.setStyleSheet(
            "border-radius: 10px; color: black; background-color: white; padding: 5px 10px;"
        )
        navbar_layout.addWidget(self.new_page_button)

        # Timer to hide navbar after inactivity
        self.navbar_timer = QTimer()
        self.navbar_timer.setInterval(1000)  # 1-second delay
        self.navbar_timer.timeout.connect(self.hide_navbar)

        # Animation for showing/hiding navbar
        self.navbar_animation = QPropertyAnimation(self.navbar, b"geometry")
        self.navbar_animation.setDuration(200)  # Animation speed

        # Variables for mouse panning
        self.dragging = False
        self.last_mouse_pos = QPoint()

        # Grid settings for background dots
        self.min_spacing = 40
        self.max_spacing = 70
        self.grid_spacing = 50
        self.zoom_step = 1
        self.dot_radius = 1

        # Initialize viewport properties
        self.update_canvas_size()
        self.center_viewport()

    def go_back(self):
        """Closes the current window and runs start_view.py"""
        subprocess.Popen(["python3", "start_view.py"])  # Run start_view.py
        self.close()  # Close the current window

    def update_canvas_size(self):
        """Updates the canvas size based on the window dimensions."""
        self.canvas_size = 10 * min(self.width(), self.height())

    def center_viewport(self):
        """Centers the viewport at the middle of the canvas."""
        self.offset = QPointF(
            self.canvas_size / 2 - self.width() / 2,
            self.canvas_size / 2 - self.height() / 2,
        )

    def paintEvent(self, event):
        """Handles painting the grid dots and background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Set black background
        painter.fillRect(self.rect(), QBrush(Qt.GlobalColor.black))

        # Draw grid dots in white
        painter.setPen(Qt.GlobalColor.darkGray)
        start_x = int(-self.offset.x() % self.grid_spacing)
        start_y = int(-self.offset.y() % self.grid_spacing)
        for x in range(start_x, self.width(), self.grid_spacing):
            for y in range(start_y, self.height(), self.grid_spacing):
                painter.drawEllipse(QPoint(x, y), self.dot_radius, self.dot_radius)

    def enterEvent(self, event):
        """Enables mouse tracking when the cursor enters the window."""
        self.setMouseTracking(True)

    def leaveEvent(self, event):
        """Starts the navbar hide timer when the cursor leaves the window."""
        self.navbar_timer.start()

    def show_navbar(self, event=None):
        """Animates the navbar to slide into view."""
        self.navbar_animation.setStartValue(QRect(0, -50, self.width(), 50))
        self.navbar_animation.setEndValue(QRect(0, 0, self.width(), 50))
        self.navbar_animation.start()
        self.navbar_timer.stop()

    def hide_navbar(self):
        """Animates the navbar to slide out of view."""
        if not self.navbar.underMouse():
            self.navbar_animation.setStartValue(QRect(0, 0, self.width(), 50))
            self.navbar_animation.setEndValue(QRect(0, -50, self.width(), 50))
            self.navbar_animation.start()
            self.navbar_timer.stop()

    def mouseMoveEvent(self, event):
        """Handles mouse movement for dragging and showing the navbar."""
        if event.pos().y() < 20 or self.navbar.underMouse():
            self.show_navbar()
        if self.dragging:
            delta = event.pos() - self.last_mouse_pos
            self.offset -= QPointF(delta.x(), delta.y())
            self.last_mouse_pos = event.pos()
            self.update()

    def mousePressEvent(self, event):
        """Detects mouse press to start dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.last_mouse_pos = event.pos()

    def mouseReleaseEvent(self, event):
        """Detects mouse release to stop dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False

    def wheelEvent(self, event):
        """Handles zooming in and out with the scroll wheel."""
        angle = event.angleDelta().y()
        new_spacing = self.grid_spacing + (
            self.zoom_step if angle > 0 else -self.zoom_step
        )
        if self.min_spacing <= new_spacing <= self.max_spacing:
            self.grid_spacing = new_spacing
            self.update()

    def resizeEvent(self, event):
        """Adjusts viewport settings when the window is resized."""
        self.update_canvas_size()
        self.center_viewport()
        self.navbar.setGeometry(0, -50, self.width(), 50)
        self.update()


# Entry point for the application.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovableViewport()
    window.show()
    sys.exit(app.exec())
