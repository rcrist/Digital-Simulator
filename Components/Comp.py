from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class Comp(QGraphicsItem):
    def __init__(self):
        super().__init__()
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        # self.setAcceptHoverEvents(True)

    def boundingRect(self) -> QRectF:
        """ Sets the size of the item as a bounding rectangle 
            OVERRIDE THIS METHOD IN DERIVED CLASSES """
        return QRectF(0, 0, 100, 100)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None) -> None:
        """ Paints the item on the scene
            If selected, draws a dashed outline
            OVERRIDE THIS METHOD IN DERIVED CLASSES """
        # Set the pen and brush for the item
        painter.setBrush(QBrush(Qt.GlobalColor.blue))
        painter.drawRect(self.boundingRect())

        # Draw selection dashed outline if selected
        if option.state & QStyle.StateFlag.State_Selected:
            self.draw_selection_outline(painter)

    def draw_selection_outline(self, painter: QPainter) -> None:
        """ Draws a selection outline around the item """
        pen = QPen(Qt.GlobalColor.yellow)
        pen.setStyle(Qt.PenStyle.DashLine)
        pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(self.boundingRect())