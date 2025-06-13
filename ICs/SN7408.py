from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from GUI.grid import snap_to_grid
from Components.comp import Comp
from ICs.packages import pkg_14

class SN7408(Comp):
    """ SN7408 Quad 2-Input AND Gate IC component """
    def __init__(self):
        super().__init__()
        self.width = 60
        self.height = 100
        self.pkg = None

        # Create connectors for the SN7408 IC
        self.conns = []
        
        # Connector locations
        off_x = 0
        off_y = 30
        self.conn_A1 = self.create_connector('input', 'A1', QPointF(0, off_y))
        self.conn_B1 = self.create_connector('input', 'B1', QPointF(0, off_y + 10))
        self.conn_Y1 = self.create_connector('output', 'Y1', QPointF(0, off_y + 20))
        self.conn_A2 = self.create_connector('input', 'A2', QPointF(0, off_y + 30))
        self.conn_B2 = self.create_connector('input', 'B2', QPointF(0, off_y + 40))
        self.conn_Y2 = self.create_connector('output', 'Y2', QPointF(0, off_y + 50))
        self.conn_GND = self.create_connector('input', 'GND', QPointF(0, off_y + 60))

        self.conn_VCC = self.create_connector('input', 'VCC', QPointF(self.width, off_y))
        self.conn_B4 = self.create_connector('input', 'B4', QPointF(self.width, off_y + 10))
        self.conn_A4 = self.create_connector('input', 'A4', QPointF(self.width, off_y + 20))
        self.conn_Y4 = self.create_connector('output', 'Y4', QPointF(self.width, off_y + 30))
        self.conn_B3 = self.create_connector('input', 'B3', QPointF(self.width, off_y + 40))
        self.conn_A3 = self.create_connector('input', 'A3', QPointF(self.width, off_y + 50))
        self.conn_Y3 = self.create_connector('output', 'Y3', QPointF(self.width, off_y + 60))

        # Add all connectors to self.conns
        self.conns = [
            self.conn_A1, self.conn_B1, self.conn_Y1,
            self.conn_A2, self.conn_B2, self.conn_Y2,
            self.conn_GND, self.conn_VCC,
            self.conn_B4, self.conn_A4, self.conn_Y4,
            self.conn_B3, self.conn_A3, self.conn_Y3
        ]

    def boundingRect(self):
        """ Returns the bounding rectangle """
        return QRectF(0, 0, self.width, self.height)
    
    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        pkg_14(painter, self)
        self.draw_conns(painter)
        self.draw_conn_text(painter)

    def draw_conn_text(self, painter: QPainter):
        from GUI.theme_state import is_dark_mode
        pen_color = Qt.GlobalColor.white if is_dark_mode else Qt.GlobalColor.black
        painter.setPen(QColor(pen_color))
        painter.setFont(QFont("Arial", 6))

        # Determine text position
        for conn in self.conns:
            text_offset_x = -20 if conn.x() > self.width / 2 else 8  # Left of pin for right-side connectors
            text_offset_y = 3
            painter.drawText(int(conn.x() + text_offset_x), int(conn.y() + text_offset_y), conn.name)

    def update(self):
        gates = [
            (self.conn_A1, self.conn_B1, self.conn_Y1),
            (self.conn_A2, self.conn_B2, self.conn_Y2),
            (self.conn_A3, self.conn_B3, self.conn_Y3),
            (self.conn_A4, self.conn_B4, self.conn_Y4)
        ]

        for A, B, Y in gates:
            if A.state and B.state:
                Y.state = True
            else:
                Y.state = False