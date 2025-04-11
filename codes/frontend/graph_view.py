# graph_view.py

import sys
import subprocess
import pathlib
import json
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt6.QtCore import Qt, QPoint, QPointF, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPainter, QBrush, QPen, QFont, QMouseEvent

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))
from version import VERSION


class MovableViewport(QWidget):
    def __init__(self, book_name="Unknown Book"):
        super().__init__()
        self.setWindowTitle(book_name)
        self.resize(800, 600)
        self.book_name = book_name
        self.setMouseTracking(True)

        self.offset = QPointF(0, 0)
        self.dragging = False
        self.last_mouse_pos = QPoint()

        self.grid_spacing = 50
        self.dot_positions = {}
        self.labels = []

        self.init_ui()

    def init_ui(self):
        self.version_text = QLabel(f"{VERSION}", self)
        self.version_text.setStyleSheet("color: gray; font-size: 10px;")

        self.coord_label = QLabel(self)
        self.coord_label.setStyleSheet(
            "color: white; background-color: black; padding: 2px; border-radius: 3px;"
        )
        self.coord_label.setFont(QFont("", 9))
        self.coord_label.hide()

        self.navbar = QWidget(self)
        self.navbar.setStyleSheet(
            "background-color: black; border: 2px solid white; border-radius: 8px;"
        )
        self.navbar.setFixedHeight(40)
        self.navbar.move(0, -40)

        self.navbar_visible = False
        self.navbar_timer = QTimer(self)
        self.navbar_timer.setInterval(500)
        self.navbar_timer.timeout.connect(self.hide_navbar)

        self.navbar_animation = QPropertyAnimation(self.navbar, b"pos")
        self.navbar_animation.setDuration(200)
        self.navbar_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.back_button = QPushButton("Back", self.navbar)
        self.back_button.setFixedSize(60, 30)
        self.back_button.clicked.connect(self.open_start_view)

        self.book_label = QLabel(self.book_name, self.navbar)
        self.book_label.setStyleSheet(
            "color: white; font-size: 14px; background: none;"
        )
        self.book_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.adjust_navbar()
        self.update_version_position()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QBrush(Qt.GlobalColor.black))

        center_x = self.width() // 2 + int(self.offset.x())
        center_y = self.height() // 2 + int(self.offset.y())

        self.dot_positions.clear()
        for x in range(
            (center_x % self.grid_spacing) - self.grid_spacing,
            self.width(),
            self.grid_spacing,
        ):
            for y in range(
                (center_y % self.grid_spacing) - self.grid_spacing,
                self.height(),
                self.grid_spacing,
            ):
                painter.setPen(QPen(Qt.GlobalColor.darkGray, 1))
                painter.drawPoint(QPoint(x, y))

        painter.setPen(QPen(Qt.GlobalColor.white, 2))
        painter.drawPoint(QPoint(center_x, center_y))

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            delta = event.pos() - self.last_mouse_pos
            self.offset += QPointF(delta.x(), delta.y())
            self.last_mouse_pos = event.pos()
            for label, rel_pos in self.labels:
                label.move((self.offset + rel_pos).toPoint())
            self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.last_mouse_pos = event.pos()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False

    def resizeEvent(self, event):
        self.adjust_navbar()
        self.update_version_position()
        super().resizeEvent(event)

    def adjust_navbar(self):
        self.navbar.setGeometry(0, 0, self.width(), 40)
        self.back_button.move(10, 5)
        self.book_label.setGeometry((self.width() // 2) - 100, 5, 200, 30)

    def show_navbar(self):
        if not self.navbar_visible:
            self.navbar_visible = True
            self.navbar_animation.setStartValue(self.navbar.pos())
            self.navbar_animation.setEndValue(QPoint(0, 0))
            self.navbar_animation.start()

    def hide_navbar(self):
        if self.navbar_visible:
            self.navbar_visible = False
            self.navbar_animation.setStartValue(self.navbar.pos())
            self.navbar_animation.setEndValue(QPoint(0, -40))
            self.navbar_animation.start()

    def update_version_position(self):
        self.version_text.adjustSize()
        self.version_text.move(
            self.width() - self.version_text.width() - 5,
            self.height() - self.version_text.height() - 5,
        )

    def open_start_view(self):
        subprocess.Popen(["python3", "start_view.py"])
        self.close()

    def loadPages(self, book_name):
        book_path = pathlib.Path(f"../../storage/bag/{book_name}")
        if not book_path.exists():
            return

        center_x = self.width() // 2
        center_y = self.height() // 2

        for page in book_path.glob("*.json"):
            with page.open("r", encoding="utf-8") as f:
                data = json.load(f)

            title = data.get("page_title", "Untitled")
            pos = data.get("page_location", {"x": 0, "y": 0})
            style = data.get("page_style", {})

            label = QLabel(title, self)
            style_string = "; ".join(
                f"{k.replace('_', '-')}: {v}" for k, v in style.items()
            )
            label.setStyleSheet(style_string)
            label.adjustSize()

            x = center_x + pos.get("x", 0)
            y = center_y - pos.get("y", 0)
            label.move(x, y)
            label.show()

            self.labels.append((label, QPointF(x, y)))

        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = MovableViewport("Example Book")
    view.show()
    sys.exit(app.exec())
