from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys

from GUI.grid import draw_grid, snap_to_grid
from Components.wire import Wire

class GridScene(QGraphicsScene):
    """ Custom QGraphicsScene that draws a grid in the background. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wire_start_pos = None
        self.wire_preview = None

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        draw_grid(painter, rect)  # Call your grid drawing function

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            x, y = snap_to_grid(event.scenePos().x(), event.scenePos().y())
            self.wire_start_pos = QPointF(x, y)
            self.wire_preview = Wire(self.wire_start_pos.x(), self.wire_start_pos.y(),
                                     self.wire_start_pos.x(), self.wire_start_pos.y())
            pen = self.wire_preview.pen()
            pen.setStyle(Qt.PenStyle.DashLine)
            self.wire_preview.setPen(pen)
            self.addItem(self.wire_preview)
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.wire_start_pos is not None and self.wire_preview is not None:
            x, y = snap_to_grid(event.scenePos().x(), event.scenePos().y())
            self.wire_preview.setLine(self.wire_start_pos.x(), self.wire_start_pos.y(), x, y)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton and self.wire_start_pos is not None:
            x, y = snap_to_grid(event.scenePos().x(), event.scenePos().y())
            wire = Wire(self.wire_start_pos.x(), self.wire_start_pos.y(), x, y)
            self.addItem(wire)
            if self.wire_preview is not None:
                self.removeItem(self.wire_preview)
                self.wire_preview = None
            self.wire_start_pos = None
        else:
            super().mouseReleaseEvent(event)