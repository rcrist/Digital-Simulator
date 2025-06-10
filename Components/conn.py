from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class Conn(QGraphicsEllipseItem):
    """ Connector on a component. """
    def __init__(self, type=None, name=None):
        super().__init__()
        self.type = type # Type can be 'input', 'output', or 'tristate'
        self.name = name
        self.state = False
        self.rad = 3

    def paint(self, painter, option, widget=None):
        painter.setPen(Qt.PenStyle.NoPen)
        if self.type == 'input':
            painter.setBrush(QBrush(Qt.GlobalColor.green))
        elif self.type == 'output':
            painter.setBrush(QBrush(Qt.GlobalColor.red))
        elif self.type == 'tristate':
            painter.setBrush(QBrush(Qt.GlobalColor.gray))
        rect = QRectF(-self.rad, -self.rad, self.rad * 2, self.rad * 2)
        painter.drawRect(rect)

    def update_state(self, state):
        self.state = state