from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from GUI.grid import snap_to_grid
from Components.comp import Comp
from Components.conn import Conn

class Switchbar(Comp):
    """ Switchbar component with multiple switches """
    def __init__(self, simulator):
        super().__init__()
        self.simulator = simulator
        self.num_switches = 4  # Number of switches
        self.height = 20 * self.num_switches + 20  # Calculate height based on number of switches

        self.conns = []
        for i in range(self.num_switches):
            # Create connectors for each switch
            conn = self.create_connector(f'output', f'out{i+1}', QPointF(70, 20 + i * 20))
            conn.state = False
            self.conns.append(conn)

    def boundingRect(self):
        """ Returns the bounding rectangle """
        return QRectF(0, 0, 70, self.height)
    
    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        """ Paints the switchbar component """
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor("white"), 2))
        painter.setBrush(QBrush(Qt.GlobalColor.darkRed))
        painter.drawRect(self.boundingRect().adjusted(4, 0, 0, 0))

        # Draw each switch and its LED
        for i, conn in enumerate(self.conns):
            y = 15 + i * 20  # vertical spacing for each switch

            # Switch positions
            on_color = Qt.GlobalColor.white if conn.state else Qt.GlobalColor.black
            off_color = Qt.GlobalColor.black if conn.state else Qt.GlobalColor.white

            # Draw ON position
            painter.setBrush(on_color)
            painter.drawRect(10, y, 20, 10)
            # Draw OFF position
            painter.setBrush(off_color)
            painter.drawRect(30, y, 20, 10)

            # Draw the output LED
            led_color = Qt.GlobalColor.yellow if conn.state else Qt.GlobalColor.darkYellow
            painter.setBrush(QBrush(led_color))
            painter.setPen(QPen(Qt.GlobalColor.white, 1))
            painter.drawRect(55, y, 8, 10)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        """Toggle the switch state when clicked."""
        pos = event.pos()
        for i, conn in enumerate(self.conns):
            y = 15 + i * 20  # Match the y used in paint()
            switch_rect = QRectF(5, y, 35, 10)  # Covers both ON and OFF positions
            if switch_rect.contains(pos):
                conn.state = not conn.state
                self.update()
                self.simulator.simulate()
                event.accept()
                return
        super().mousePressEvent(event)