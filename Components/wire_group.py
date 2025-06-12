from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class WireGroup():
    def __init__(self, group):
        self.wires = group  # Store the list of wires as 'wires'
        if group:
            first_wire = group[0]
            last_wire = group[-1]
            self.startX = first_wire.line().p1().x()
            self.startY = first_wire.line().p1().y()
            self.endX = last_wire.line().p2().x()
            self.endY = last_wire.line().p2().y()
        else:
            self.startX = self.startY = self.endX = self.endY = 0
        self.color = "white"
        self.state = False

    def update(self):
        # Update the wire group state or appearance
        self.color = "green" if self.state else "white"

    def paint(self, painter, option, widget=None):
        for wire in self.wires:
            from GUI.theme_state import is_dark_mode
            self.default_line_color = Qt.GlobalColor.white if is_dark_mode else Qt.GlobalColor.black
            color = Qt.GlobalColor.green if self.state else self.default_line_color
            painter.setPen(QPen(color, self.line_width))
            painter.drawLine(self.line())

    def print_group(self):
        print(f"WireGroup start: ({self.startX}, {self.startY}), end: ({self.endx}, {self.endY})")
        print(f"WireGroup state: {self.state}")