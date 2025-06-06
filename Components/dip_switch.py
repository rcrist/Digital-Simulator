from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from GUI.grid import snap_to_grid
from Components.comp import Comp

class DipSwitch(Comp):
    """ Dip switch with output LED """
    def __init__(self):
        super().__init__()

        self.conns = [
            {"name": "out", "type": "output", "pos": QPointF(50, 10), "state": False}
        ]

    def boundingRect(self):
        """ Returns the bounding rectangle """
        return QRectF(0, 0, 50, 20)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        """ Paints the Switch component """       
        # Draw the gate symbol and connectors
        self.draw_comp_symbol(painter)
        self.draw_conns(painter)

        # Draw selection outline if selected
        if option.state & QStyle.StateFlag.State_Selected:
            self.draw_selection_outline(painter)

    def draw_comp_symbol(self, painter: QPainter) -> None:
        """ Draws the component symbol (simple switch) """
        # Draw the switch body
        painter.setBrush(Qt.GlobalColor.darkRed)
        painter.drawRect(0, 0, 40, 20)

        # Draw the switch positions
        on_color = Qt.GlobalColor.black if self.conns[0]["state"] else Qt.GlobalColor.white
        off_color = Qt.GlobalColor.white if self.conns[0]["state"] else Qt.GlobalColor.black
        painter.setBrush(on_color)
        painter.drawRect(5, 5, 15, 10)
        painter.setBrush(off_color)
        painter.drawRect(20, 5, 15, 10)

        # Draw the output LED
        rad = 3
        led_color = Qt.GlobalColor.yellow if self.conns[0]["state"] else Qt.GlobalColor.darkYellow
        painter.setBrush(QBrush(led_color))
        painter.drawEllipse(QPointF(45, 10), rad, rad)

    def update_state(self, state: bool):
        """ Updates the state of the component with the provided state. """
        self.conns[0]["state"] = state

    def mousePressEvent(self, event):
        """Toggle the switch state when clicked."""
        self.conns[0]["state"] = not self.conns[0]["state"]
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
            "type": "dip_switch",
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
