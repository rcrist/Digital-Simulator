from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from GUI.grid import snap_to_grid
from Components.comp import Comp
from Components.conn import Conn

class LED(Comp):
    """ LED component """
    def __init__(self):
        super().__init__()
        self.width = 20
        self.height = 20
        self.led_color = "yellow"  # Default color

        self.conn_in = Conn('input','in')
        self.conn_in.setParentItem(self)
        self.conn_in.setPos(0, self.boundingRect().height() / 2)

        self.conns = [self.conn_in]

    def boundingRect(self):
        """ Returns the bounding rectangle """
        return QRectF(0, 0, self.width, self.height)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        """ Paints the component """       
        # Draw the component symbol and connectors
        self.draw_comp_symbol(painter)
        self.draw_conns(painter)

        # Draw selection outline if selected
        if option.state & QStyle.StateFlag.State_Selected:
            self.draw_selection_outline(painter)

    def draw_comp_symbol(self, painter: QPainter) -> None:
        """ Draws the component symbol """
        # Draw the LED body
        rad = self.width / 2
        painter.setBrush(Qt.GlobalColor.darkRed)
        painter.drawEllipse(QPointF(self.width/2, self.height/2), rad, rad)

        # Draw the LED light
        rad = self.width / 2 - 3
        color_map = {
            "red": (Qt.GlobalColor.red, Qt.GlobalColor.darkRed),
            "green": (Qt.GlobalColor.green, Qt.GlobalColor.darkGreen),
            "yellow": (Qt.GlobalColor.yellow, Qt.GlobalColor.darkYellow),
            "blue": (Qt.GlobalColor.blue, Qt.GlobalColor.darkBlue),
        }
        on_color, off_color = color_map.get(self.led_color, (Qt.GlobalColor.yellow, Qt.GlobalColor.darkYellow))
        color = on_color if self.conn_in.state else off_color
        painter.setBrush(color)
        painter.drawEllipse(QPointF(self.width/2, self.height/2), rad, rad)

    def update_state(self, state: bool):
        """ Updates the state of the component with the provided state. """
        self.conn_in.update_state(state)

    def set_led_color(self, color: str):
        """ Sets the LED color. """
        if color in ["red", "green", "yellow", "blue"]:
            self.led_color = color
            self.update()

    def draw_conns(self, painter: QPainter):
        for conn in self.conns:
            if conn.type == "input":
                painter.setPen(Qt.GlobalColor.green)
                painter.setBrush(Qt.GlobalColor.green)
            else:
                painter.setPen(Qt.GlobalColor.red)
                painter.setBrush(Qt.GlobalColor.red)
            painter.drawRect(QRectF(conn.pos().x() - self.c_rad, conn.pos().y() - self.c_rad,
                             self.c_rad * 2, self.c_rad * 2))

    def mousePressEvent(self, event):
        """Toggle the switch state when clicked."""
        self.update_state(not self.conn_in.state)
        self.update()
        # Update the properties dock LED if available
        main_window = self.scene().views()[0].window() if self.scene().views() else None
        if main_window and hasattr(main_window, "properties_dock"):
            self.setSelected(True)  # Ensure selection so properties dock updates
            main_window.properties_dock.show_controls(True, self)
        super().mousePressEvent(event)

    def to_dict(self):
        """ Save file JSON fields for the component """
        pos = self.pos()
        rect = self.boundingRect()
        conn_states = {conn["name"]: conn["state"] for conn in self.conns}
        return {
            "type": "led",
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
            if conn["name"] in conn_states:
                conn["state"] = conn_states[conn["name"]]
        return obj
