from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from GUI.grid import snap_to_grid
from Components.comp import Comp
from Components.conn import Conn

class Clock(Comp):
    """ Clock component """
    def __init__(self, simulator):
        super().__init__()
        self.simulator = simulator
        self.toggle_timer = None
        self.is_toggling = False

        self.conn_out = self.create_connector('output', 'out', QPointF(50, 20))
        self.conns = [self.conn_out]

    def boundingRect(self):
        """ Returns the bounding rectangle """
        return QRectF(0, 0, 50, 40)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        """ Paints the Clock component """
        # Draw the clock body

        from GUI.theme_state import is_dark_mode
        self.pen_color = QColor(255, 255, 255) if is_dark_mode else QColor(0, 0, 0)
        painter.setPen(QPen(self.pen_color, 2))
        self.brush_color = QColor(0, 0, 0) if is_dark_mode else QColor(255, 255, 255)
        painter.setBrush(QBrush(self.brush_color))
        painter.drawRect(0, 0, 
                int(self.boundingRect().width()), 
                int(self.boundingRect().height()))
        
        # Draw the square wave
        painter.setPen(QPen(Qt.GlobalColor.green, 2))
        path = QPainterPath()
        margin = 8
        offset = 4
        top = margin + 5
        mid = self.boundingRect().height() / 2
        bottom = self.boundingRect().height() - margin - 5
        left = margin - offset
        width = self.boundingRect().width() - 2 * margin
        step = width / 4

        # Start at left-middle
        path.moveTo(left, mid)
        path.lineTo(left, top)
        path.lineTo(left + step, top)
        path.lineTo(left + step, bottom)
        path.lineTo(left + 2*step, bottom)
        path.lineTo(left + 2*step, top)
        path.lineTo(left + 3*step, top)
        path.lineTo(left + 3*step, bottom)
        path.lineTo(left + 4*step, bottom)
        path.lineTo(left + 4*step, mid)
        painter.drawPath(path)
        
        # Draw the output LED
        led_color = Qt.GlobalColor.yellow if self.conn_out.state else Qt.GlobalColor.darkYellow
        painter.setBrush(QBrush(led_color))
        painter.setPen(QPen(Qt.GlobalColor.white, 1))
        painter.drawRect(41, 10, 5, 20)

    def update_state(self, state: bool):
        """ Updates the state of the component with the provided state. """
        self.conns[0].state = state
        super().update()

    def mousePressEvent(self, event):
        """Toggle the clock state when clicked."""
        self.conn_out.state = not self.conn_out.state
        self.update()
        self.is_toggling = not self.is_toggling
        self.is_toggling = self.start_toggling() if self.is_toggling else self.stop_toggling()
        self.simulator.simulate()
        # Update the properties dock LED if available
        main_window = self.scene().views()[0].window() if self.scene().views() else None
        if main_window and hasattr(main_window, "properties_dock"):
            self.setSelected(True)  # Ensure selection so properties dock updates
            main_window.properties_dock.show_controls(True, self)
        super().mousePressEvent(event)

    def start_toggling(self):
        """ Start toggling the clock output state at regular intervals. """
        self.toggle_timer = QTimer()
        self.toggle_timer.timeout.connect(self.toggle_output)
        self.toggle_timer.start(1000)

    def toggle_output(self):
        """ Toggle the clock output state. """
        if self.toggle_timer is not None:
            self.is_toggling = True
            self.conn_out.state = not self.conn_out.state
            self.update()
            self.simulator.simulate()
            # Update the properties dock LED if available
            main_window = self.scene().views()[0].window() if self.scene().views() else None
            if main_window and hasattr(main_window, "properties_dock"):
                main_window.properties_dock.show_controls(True, self)

    def stop_toggling(self):
        """ Stop toggling the clock output state. """
        if hasattr(self, 'toggle_timer'):
            self.is_toggling = False
            self.toggle_timer.stop()
            self.toggle_timer = None

    def to_dict(self):
            """ Save file JSON fields for the component """
            pos = self.pos()
            rect = self.boundingRect()
            conn_states = {conn["name"]: conn["state"] for conn in self.conns}
            return {
                "type": "clock",
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

