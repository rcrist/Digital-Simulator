from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

def pkg_14(painter, self):
    # Set the pen and brush colors based on the theme
    from GUI.theme_state import is_dark_mode
    self.pen_color = Qt.GlobalColor.white if is_dark_mode else Qt.GlobalColor.black
    painter.setPen(self.pen_color)
    self.brush_color = Qt.GlobalColor.black if is_dark_mode else Qt.GlobalColor.white
    painter.setBrush(self.brush_color)

    # Draw the IC body rectangle
    painter.drawRect(0, 0, 60, 100)

    # Draw pin 1 indicator circle
    painter.drawEllipse(5, 18, 6, 6)

    # Draw IC name box
    painter.setBrush(QColor("#6070FF"))
    painter.drawRect(0, 0, self.width, 15)
    painter.drawText(10, 12, "SN7408")
