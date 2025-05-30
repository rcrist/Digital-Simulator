from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class Comp(QGraphicsItem):
    def __init__(self):
        super().__init__()
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.radius = 3

        # Define the connector locations in local coordinates
        self.conns = [
            { "name": "in1", "type": "input", "x": 0, "y": 10, "state": False },
            { "name": "in2", "type": "input", "x": 0, "y": 30, "state": False },
            { "name": "out", "type": "output", "x": self.boundingRect().width(), "y": 20, "state": False },
        ]

        self.leds = [
            { "name": "in_led1", "x": 11, "y": 11, "state": False },
            { "name": "in_led2", "x": 11, "y": 29, "state": False },
            { "name": "out_led", "x": self.boundingRect().width() - 11, "y": 20, "state": False },
        ]

    def boundingRect(self) -> QRectF:
        """ Sets the size of the item as a bounding rectangle 
            OVERRIDE IN DERIVED CLASSES """
        return QRectF(0, 0, 100, 100)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None) -> None:
        """ Paints the item on the scene
            If selected, draws a dashed outline
            OVERRIDE IN DERIVED CLASSES """
        # Set the pen and brush for the item
        painter.setBrush(QBrush(Qt.GlobalColor.blue))
        painter.drawRect(self.boundingRect())

        # Draw selection dashed outline if selected
        if option.state & QStyle.StateFlag.State_Selected:
            self.draw_selection_outline(painter)

    def draw_selection_outline(self, painter: QPainter) -> None:
        """ Draws a selection outline around the item """
        pen = QPen(Qt.GlobalColor.blue)
        pen.setStyle(Qt.PenStyle.DotLine)
        pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(self.boundingRect())

    def drawConn(self, painter) -> None:
        for conn in self.conns:
            painter.setPen(QPen(Qt.GlobalColor.white, 1))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(
                int(conn["x"] - self.radius),
                int(conn["y"] - self.radius),
                int(self.radius * 2),
                int(self.radius * 2)
            )

    def drawStateLeds(self, painter) -> None:
        for led in self.leds:
            color = Qt.GlobalColor.yellow if led["state"] else Qt.GlobalColor.darkYellow
            painter.setPen(QPen(color, 1))
            painter.setBrush(color)
            painter.drawEllipse(
                int(led["x"] - self.radius),
                int(led["y"] - self.radius),
                int(self.radius * 2),
                int(self.radius * 2)
            )

    def itemChange(self, change, value):
        """ Ensure the item, scene, and view are properly redrawn when moved to avoid artifacts """
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            self.update()  # Request a repaint of the item
            if self.scene():
                self.scene().update()  # Request a repaint of the scene
                views = self.scene().views()
                if views:
                    for view in views:
                        view.viewport().update()  # Request a repaint of the view
        return super().itemChange(change, value)
    
    def sync_leds_with_conns(self):
        """Set each LED's state to match the corresponding connector's state by index."""
        for i, led in enumerate(self.leds):
            if i < len(self.conns):
                led["state"] = self.conns[i]["state"]

    def setRotationAngle(self, angle):
        # Set the transform origin to the center of the bounding rect
        rect = self.boundingRect()
        center = rect.center()
        self.setTransformOriginPoint(center)
        self.setRotation(angle)
        self.rotation_angle = angle