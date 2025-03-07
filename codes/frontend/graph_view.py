import sys
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

        # Navigation bar setup
        self.navbar = QWidget(self)
        self.navbar.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.navbar.setFixedHeight(50)
        self.navbar.setGeometry(0, -50, self.width(), 50)

        navbar_layout = QHBoxLayout()
        navbar_layout.setContentsMargins(10, 0, 10, 0)
        self.navbar.setLayout(navbar_layout)

        self.back_button = QPushButton("⬅", self.navbar)
        self.back_button.setFixedSize(40, 40)
        self.back_button.setStyleSheet("font-size: 24px;")  # Make arrow bigger
        navbar_layout.addWidget(self.back_button)
        navbar_layout.addStretch()

        self.title_label = QLabel("Book_name_placeholder", self.navbar)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("color: white; font-size: 16px;")
        navbar_layout.addWidget(self.title_label)
        navbar_layout.addStretch()

        self.new_page_button = QPushButton("New Label", self.navbar)
        self.new_page_button.setFixedSize(100, 40)
        self.new_page_button.setStyleSheet(
            "border-radius: 10px; color: black; background-color: white; padding: 5px 10px;"
        )
        navbar_layout.addWidget(self.new_page_button)

        self.navbar_timer = QTimer()
        self.navbar_timer.setInterval(1000)
        self.navbar_timer.timeout.connect(self.hide_navbar)

        self.navbar_animation = QPropertyAnimation(self.navbar, b"geometry")
        self.navbar_animation.setDuration(200)

        self.dragging = False
        self.last_mouse_pos = QPoint()

        self.min_spacing = 40
        self.max_spacing = 70
        self.grid_spacing = 50
        self.zoom_step = 1
        self.dot_radius = 1

        self.update_canvas_size()
        self.center_viewport()

    def update_canvas_size(self):
        self.canvas_size = 10 * min(self.width(), self.height())

    def center_viewport(self):
        self.offset = QPointF(
            self.canvas_size / 2 - self.width() / 2,
            self.canvas_size / 2 - self.height() / 2,
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Set black background
        painter.fillRect(self.rect(), QBrush(Qt.GlobalColor.black))

        # Draw white grid dots
        painter.setPen(Qt.GlobalColor.white)
        start_x = int(-self.offset.x() % self.grid_spacing)
        start_y = int(-self.offset.y() % self.grid_spacing)
        for x in range(start_x, self.width(), self.grid_spacing):
            for y in range(start_y, self.height(), self.grid_spacing):
                painter.drawEllipse(QPoint(x, y), self.dot_radius, self.dot_radius)

    def enterEvent(self, event):
        self.setMouseTracking(True)

    def leaveEvent(self, event):
        self.navbar_timer.start()

    def show_navbar(self, event=None):
        self.navbar_animation.setStartValue(QRect(0, -50, self.width(), 50))
        self.navbar_animation.setEndValue(QRect(0, 0, self.width(), 50))
        self.navbar_animation.start()
        self.navbar_timer.stop()

    def hide_navbar(self):
        if not self.navbar.underMouse():
            self.navbar_animation.setStartValue(QRect(0, 0, self.width(), 50))
            self.navbar_animation.setEndValue(QRect(0, -50, self.width(), 50))
            self.navbar_animation.start()
            self.navbar_timer.stop()

    def mouseMoveEvent(self, event):
        if event.pos().y() < 20 or self.navbar.underMouse():
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovableViewport()
    window.show()
    sys.exit(app.exec())
