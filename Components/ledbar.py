from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from GUI.grid import snap_to_grid
from Components.comp import Comp

class Ledbar(Comp):
    """ Ledbar component with multiple LEDs """
    def __init__(self):
        super().__init__()
        self.num_leds = 4  # Number of LEDs

        self.conns = []
        for i in range(self.num_leds):
            # Create connectors for each LED
            conn = self.create_connector(f'input', f'in{i+1}', QPointF(0, 20 + i * 20))
            conn.state = False
            self.height = 20 * self.num_leds + 20 
            self.conns.append(conn)

    def boundingRect(self):
        """ Returns the bounding rectangle """
        return QRectF(0, 0, 60, self.height)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        """ Paints the switchbar component """
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor("white"), 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)  # No fill color
        painter.drawRect(self.boundingRect())

        # Draw each LED
        for i, conn in enumerate(self.conns):
            y = 15 + i * 20  # vertical spacing for each switch

            led_color = Qt.GlobalColor.yellow if conn.state else Qt.GlobalColor.darkYellow
            painter.setBrush(QBrush(led_color))
            painter.setPen(QPen(Qt.GlobalColor.white, 1))
            painter.drawRect(10, y, 40, 10)

    def update_state(self, state: bool):
        """ Updates the state of the component with the provided state. """
        for conn in self.conns:
            conn.update_state(state)