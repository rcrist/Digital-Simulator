from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from GUI.grid import snap_to_grid
from Components.comp import Comp
from Components.conn import Conn

class SevenSegment(Comp):
    """ Seven Segment Display component """
    def __init__(self):
        super().__init__()
        self.color = "blue"  # Default color

        self.conns = self.create_connectors()

        # Initialize segment colors
        self.on_color = '#ff0'  # Color when segment is on
        self.off_color = '#880'  # Color when segment is off
        self.set_segment_colors(self.color)  # Set initial segment colors

    def create_connectors(self):
        # Create seven connectors labeled 'a' to 'g', spaced vertically by 10 pixels starting at y=20
        names = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        conns = []
        conn_positions = {}
        for i, name in enumerate(names):
            pos = QPointF(0, 20 + i * 10)
            conns.append(self.create_connector('input', name, pos))
            conn_positions[name] = pos
        # Assign each connector to an attribute for easy access
        (self.conn_a, self.conn_b, self.conn_c, self.conn_d, 
         self.conn_e, self.conn_f, self.conn_g) = conns
        self.conn_positions = conn_positions  # For drawing labels
        # conns[0].state = True  # Set 'a' to high by default
        return conns

    def boundingRect(self):
        """ Returns the bounding rectangle """
        return QRectF(0, 0, 70, 100)
    
    def hor_rect(self):
        """ Returns the rectangle for the horizontal segment """
        return QRectF(0, 0, 30, 5)
    
    def ver_rect(self):
        """ Returns the rectangle for the vertical segment """
        return QRectF(0, 0, 5, 30)
    
    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        """ Paints the seven segment display """
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor("white"), 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)  # No fill color
        painter.drawRect(self.boundingRect().adjusted(4, 0, 0, 0))

        # Draw connector labels
        painter.setPen(QPen(QColor("white")))
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)
        for name, pos in getattr(self, "conn_positions", {}).items():
            painter.drawText(int(pos.x()) + 5, int(pos.y()) + 4, name.lower())

        # Segment positions: (method, (x, y))
        segments = [
            (self.hor_rect, (25, 10)),  # a
            (self.ver_rect, (20, 15)),  # f
            (self.ver_rect, (55, 15)),  # b
            (self.hor_rect, (25, 45)),  # g
            (self.ver_rect, (20, 50)),  # e
            (self.ver_rect, (55, 50)),  # c
            (self.hor_rect, (25, 80)),  # d
        ]

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(self.color))

                # Draw segments with color based on connector state
        segment_conns = [
            self.conn_a,  # a
            self.conn_f,  # f
            self.conn_b,  # b
            self.conn_g,  # g
            self.conn_e,  # e
            self.conn_c,  # c
            self.conn_d,  # d
        ]

        for (rect_func, (x, y)), conn in zip(segments, segment_conns):
            rect = rect_func()
            rect.moveTo(x, y)
            # Use onColor if connector is "high"/True, else offColor
            color = self.onColor if getattr(conn, "state", False) else self.offColor
            painter.setBrush(QColor(color))
            painter.drawRect(rect)

    def set_segment_colors(self, color):
        color_map = {
            'yellow': ('#ff0', '#880'),
            'red':    ('#f00', '#800'),
            'green':  ('#0f0', '#080'),
            'blue':   ('#00f', '#008'),
        }
        self.onColor, self.offColor = color_map.get(color, ('#fff', '#888'))

    def update(self):
        """ Updates the state of the component based on the inputs """
        super().update()

    def to_dict(self):
        """ Save file JSON fields for the component """
        pos = self.pos()
        rect = self.boundingRect()
        conn_states = {conn.name: conn.state for conn in self.conns}
        return {
            "type": "seven_segment",
            "x": rect.x(),
            "y": rect.y(),
            "width": rect.width(),
            "height": rect.height(),
            "rotation": self.rotation(),
            "pos_x": pos.x(),
            "pos_y": pos.y(),
            "conn_states": conn_states
        }

    @classmethod
    def from_dict(cls, data):
        """ Load file JSON fields for the component """
        obj = cls()
        obj.setRotation(data.get("rotation", 0))
        obj.setPos(data.get("pos_x", 0), data.get("pos_y", 0))
        # Restore connector states by name if present
        conn_states = data.get("conn_states", {})
        for conn in obj.conns:
            if conn.name in conn_states:
                conn.state = conn_states[conn.name]
        return obj
