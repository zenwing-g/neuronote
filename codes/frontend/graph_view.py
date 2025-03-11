import sys
import subprocess
import pathlib
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt6.QtCore import Qt, QPoint, QPointF, QRect
from PyQt6.QtGui import QPainter, QBrush, QPen, QFont

# Add the root directory to sys.path to allow importing version information
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent))
from version import VERSION  # Import the version number


class MovableViewport(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graph View")
        self.resize(800, 600)
        self.setMouseTracking(True)

        # Coordinate label for hover effect
        self.coord_label = QLabel(self)
        self.coord_label.setStyleSheet(
            "color: white; background-color: black; padding: 2px; border-radius: 3px;"
        )
        font = QFont()
        font.setPixelSize(9)  # Set font size to 9px
        self.coord_label.setFont(font)
        self.coord_label.hide()

        # Variables for tracking panning
        self.dragging = False
        self.last_mouse_pos = QPoint()

        # Grid settings
        self.grid_spacing = 50
        self.offset = QPointF(0, 0)

        # Store dot positions
        self.dot_positions = {}

        # Version label (bottom-right)
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

        # Grid drawing
        start_x = (center_x % self.grid_spacing) - self.grid_spacing
        start_y = (center_y % self.grid_spacing) - self.grid_spacing

        for x in range(start_x, self.width(), self.grid_spacing):
            for y in range(start_y, self.height(), self.grid_spacing):
                rel_x = (x - center_x) // self.grid_spacing
                rel_y = (center_y - y) // self.grid_spacing  # Inverted Y-axis

                # Store dot positions with relative coordinates
                self.dot_positions[(x, y)] = (rel_x, rel_y)

                # Draw normal dots
                if x == center_x and y == center_y:
                    continue
                painter.setPen(QPen(Qt.GlobalColor.darkGray, 1))
                painter.drawPoint(QPoint(x, y))

        # Draw the center dot
        painter.setPen(QPen(Qt.GlobalColor.white, 2))
        painter.drawPoint(QPoint(center_x, center_y))

        # Label center as (0x0)
        font = QFont()
        font.setPixelSize(8)
        painter.setFont(font)
        painter.drawText(center_x - 10, center_y + 12, "(0x0)")

    def mouseMoveEvent(self, event):
        # Track mouse for panning
        if self.dragging:
            delta = event.pos() - self.last_mouse_pos
            self.offset += QPointF(delta.x(), delta.y())
            self.last_mouse_pos = event.pos()
            self.update()
            return

        # Check if mouse is near a dot
        hover_radius = 5
        for (x, y), (rel_x, rel_y) in self.dot_positions.items():
            if (
                abs(event.pos().x() - x) <= hover_radius
                and abs(event.pos().y() - y) <= hover_radius
            ):
                # Show coordinate label
                self.coord_label.setText(f"({rel_x}x{rel_y})")
                self.coord_label.move(event.pos().x() + 10, event.pos().y() - 20)
                self.coord_label.show()
                return

        # Hide label if not near any dot
        self.coord_label.hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.last_mouse_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False

    def update_version_position(self):
        """Position the version text in the bottom-right corner."""
        margin = 5
        self.version_text.adjustSize()
        x = self.width() - self.version_text.width() - margin
        y = self.height() - self.version_text.height() - margin
        self.version_text.move(x, y)

    def resizeEvent(self, event):
        self.update_version_position()
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovableViewport()
    window.show()
    sys.exit(app.exec())
