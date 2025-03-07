import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPen, QBrush
from PyQt6.QtCore import Qt, QPoint, QPointF


class MovableViewport(QWidget):
    def __init__(self):
        """Initialize the movable viewport with a centered dot grid."""
        super().__init__()
        self.setWindowTitle("Graph View")

        # Set the initial window size (you can adjust this)
        self.resize(800, 600)  # Width x Height

        # Center the window on the screen
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()

        center_x = (screen_geometry.width() - window_geometry.width()) // 2
        center_y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(center_x, center_y)  # Move the window to the center

        # Variables for viewport movement
        self.dragging = False  # Tracks if the user is dragging
        self.last_mouse_pos = QPoint()  # Stores last mouse position

        # Grid settings (dots)
        self.min_spacing = 40  # Minimum distance between dots (px)
        self.max_spacing = 70  # Maximum distance between dots (px)
        self.grid_spacing = 50  # Default dot spacing (adjustable via scrolling)
        self.zoom_step = 1  # Change in spacing per scroll step
        self.dot_radius = 1  # Fixed dot radius (dots remain same size)

        # Set the canvas size and center the viewport
        self.update_canvas_size()
        self.center_viewport()  # Move viewport so (0,0) is at the window center

    def update_canvas_size(self):
        """Update the canvas size dynamically based on the window size.
        The canvas is always 10× larger than the current window.
        """
        self.canvas_size = 10 * min(self.width(), self.height())

    def center_viewport(self):
        """Centers the viewport so (0,0) aligns with the middle of the window."""
        self.offset = QPointF(
            self.canvas_size / 2 - self.width() / 2,  # Center horizontally
            self.canvas_size / 2 - self.height() / 2,  # Center vertically
        )

    def paintEvent(self, event):
        """Handles the drawing of the dot grid and background."""
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )  # Enable anti-aliasing for smooth rendering

        # Fill the background with black
        painter.fillRect(self.rect(), Qt.GlobalColor.black)

        # Set dot color (white dots on black background)
        painter.setPen(
            QPen(Qt.GlobalColor.black, 1)
        )  # Border color (not used for dots)
        painter.setBrush(QBrush(Qt.GlobalColor.white))  # Fill color for dots

        # Loop through the entire large canvas and draw dots at every grid point
        for x in range(0, self.canvas_size, self.grid_spacing):
            for y in range(0, self.canvas_size, self.grid_spacing):
                # Calculate where the dot should be drawn relative to the viewport offset
                screen_x = x - self.offset.x()
                screen_y = y - self.offset.y()

                # Only draw dots that are within the visible part of the window
                if 0 <= screen_x <= self.width() and 0 <= screen_y <= self.height():
                    painter.drawEllipse(
                        int(screen_x),
                        int(screen_y),
                        self.dot_radius * 2,  # Dot width (2× radius)
                        self.dot_radius * 2,  # Dot height (2× radius)
                    )

    def mousePressEvent(self, event):
        """Detect when the user starts dragging the viewport."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.last_mouse_pos = (
                event.pos()
            )  # Store the starting position of the mouse

    def mouseMoveEvent(self, event):
        """Handles dragging (panning) of the viewport when the user moves the mouse."""
        if self.dragging:
            # Calculate how much the mouse has moved since the last update
            delta = event.pos() - self.last_mouse_pos

            # Adjust the viewport offset based on the mouse movement
            self.offset -= QPointF(delta.x(), delta.y())

            # Prevent scrolling beyond the boundaries of the large canvas
            max_x = self.canvas_size - self.width()  # Max right movement
            max_y = self.canvas_size - self.height()  # Max bottom movement
            self.offset.setX(max(0, min(self.offset.x(), max_x)))
            self.offset.setY(max(0, min(self.offset.y(), max_y)))

            # Update the last known mouse position
            self.last_mouse_pos = event.pos()
            self.update()  # Redraw the screen with the new offset

    def mouseReleaseEvent(self, event):
        """Stops dragging when the user releases the left mouse button."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False  # Stop panning

    def wheelEvent(self, event):
        """Adjust the spacing between dots when the user scrolls."""
        angle = event.angleDelta().y()  # Get scroll direction
        new_spacing = self.grid_spacing + (
            self.zoom_step if angle > 0 else -self.zoom_step
        )

        # Ensure that spacing stays within the allowed range (40px to 70px)
        if self.min_spacing <= new_spacing <= self.max_spacing:
            self.grid_spacing = new_spacing  # Update spacing
            self.update()  # Redraw the screen with the new spacing

    def resizeEvent(self, event):
        """Updates the canvas size dynamically when the window is resized."""
        self.update_canvas_size()
        self.center_viewport()  # Recenter viewport when window is resized
        self.update()  # Redraw the dots to fit the new window size


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovableViewport()
    window.show()
    sys.exit(app.exec())
