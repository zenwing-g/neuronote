import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import QPropertyAnimation, Qt, QPoint, QPointF, QTimer, QRect
from PyQt6.QtGui import QPainter, QBrush


class MovableViewport(QWidget):
    def __init__(self):
        """Initialize the movable viewport with a centered dot grid and navigation bar."""
        super().__init__()
        self.setWindowTitle("Graph View")
        self.resize(800, 600)
        self.setMouseTracking(True)

        # Navigation bar setup
        self.navbar = QWidget(self)
        self.navbar.setStyleSheet("background-color: rgb(50, 50, 50);")  # Fully opaque
        self.navbar.setFixedHeight(50)
        self.navbar.setGeometry(0, -50, self.width(), 50)

        # Navigation bar layout
        navbar_layout = QHBoxLayout()
        navbar_layout.setContentsMargins(10, 0, 10, 0)
        self.navbar.setLayout(navbar_layout)

        # Back button
        self.back_button = QPushButton("⬅", self.navbar)
        self.back_button.setFixedSize(40, 40)
        navbar_layout.addWidget(self.back_button)

        # Spacer to push title to the center
        navbar_layout.addStretch()

        # Title label
        self.title_label = QLabel("Graph View", self.navbar)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("color: white; font-size: 16px;")
        navbar_layout.addWidget(self.title_label)

        # Spacer to push the new page button to the right
        navbar_layout.addStretch()

        # New Page button
        self.new_page_button = QPushButton("New Label", self.navbar)
        navbar_layout.addWidget(self.new_page_button)

        # Timer to auto-hide navbar
        self.navbar_timer = QTimer()
        self.navbar_timer.setInterval(1000)
        self.navbar_timer.timeout.connect(self.hide_navbar)

        # Animation setup
        self.navbar_animation = QPropertyAnimation(self.navbar, b"geometry")
        self.navbar_animation.setDuration(200)

        # Variables for viewport movement
        self.dragging = False
        self.last_mouse_pos = QPoint()

        # Grid settings
        self.min_spacing = 40
        self.max_spacing = 70
        self.grid_spacing = 50
        self.zoom_step = 1
        self.dot_radius = 1

        self.update_canvas_size()
        self.center_viewport()

    def update_canvas_size(self):
        """Update the canvas size dynamically based on the window size."""
        self.canvas_size = 10 * min(self.width(), self.height())

    def center_viewport(self):
        """Center the viewport so (0,0) aligns with the middle of the window."""
        self.offset = QPointF(
            self.canvas_size / 2 - self.width() / 2,
            self.canvas_size / 2 - self.height() / 2,
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.black)
        painter.setBrush(QBrush(Qt.GlobalColor.white))
        for x in range(0, self.canvas_size, self.grid_spacing):
            for y in range(0, self.canvas_size, self.grid_spacing):
                screen_x = x - self.offset.x()
                screen_y = y - self.offset.y()
                if 0 <= screen_x <= self.width() and 0 <= screen_y <= self.height():
                    painter.drawEllipse(
                        int(screen_x),
                        int(screen_y),
                        self.dot_radius * 2,
                        self.dot_radius * 2,
                    )

    def mouseMoveEvent(self, event):
        """Show navbar when mouse moves near the top on hover."""
        if event.pos().y() < 20:
            self.show_navbar()
        if self.dragging:
            delta = event.pos() - self.last_mouse_pos
            self.offset -= QPointF(delta.x(), delta.y())
            self.last_mouse_pos = event.pos()
            self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.last_mouse_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False

    def wheelEvent(self, event):
        angle = event.angleDelta().y()
        new_spacing = self.grid_spacing + (
            self.zoom_step if angle > 0 else -self.zoom_step
        )
        if self.min_spacing <= new_spacing <= self.max_spacing:
            self.grid_spacing = new_spacing
            self.update()

    def resizeEvent(self, event):
        self.update_canvas_size()
        self.center_viewport()
        self.navbar.setGeometry(0, -50, self.width(), 50)
        self.update()

    def show_navbar(self):
        """Slide down the navbar with animation."""
        self.navbar_animation.setStartValue(QRect(0, -50, self.width(), 50))
        self.navbar_animation.setEndValue(QRect(0, 0, self.width(), 50))
        self.navbar_animation.start()
        self.navbar_timer.start()

    def hide_navbar(self):
        """Slide up the navbar with animation."""
        self.navbar_animation.setStartValue(QRect(0, 0, self.width(), 50))
        self.navbar_animation.setEndValue(QRect(0, -50, self.width(), 50))
        self.navbar_animation.start()
        self.navbar_timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovableViewport()
    window.show()
    sys.exit(app.exec())
