from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Components.Comp import Comp

# And Gate reference: https://www.geeksforgeeks.org/and-gate/

class AndGate(Comp):
    def __init__(self):
        super().__init__()

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, 40, 40)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None) -> None:
        path = QPainterPath()
        # Left vertical line
        path.moveTo(5, 5)
        path.lineTo(5, 35)
        # Bottom line
        path.lineTo(20, 35)
        # Right semicircle (arc)
        rect = QRectF(5, 5, 30, 30)
        path.arcTo(rect, 270, 180)
        # Top line
        path.lineTo(5, 5)

        painter.setPen(QPen(Qt.GlobalColor.white, 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)

        # Draw the input and output connectors
        self.drawConn(painter)

        # Draw the LEDs for inputs and outputs
        self.drawStateLeds(painter)

        # Draw selection outline if selected
        if option.state & QStyle.StateFlag.State_Selected:
            self.draw_selection_outline(painter)