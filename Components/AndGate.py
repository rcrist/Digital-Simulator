from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from GUI.GridScene import GridScene
from Components.Comp import Comp

class AndGate(QGraphicsRectItem, Comp):
    def __init__(self, x, y, w=40, h=40):
        super().__init__(QRectF(x, y, w, h))
        self.rect = QRectF(x, y, w, h)
        self.image = QPixmap("Digital Simulator Tool/Images/and_gate_32x32_white.png")
        if self.image.isNull():
            print("Failed to load image: Images/and_gate_32x32_white.png")

    def paint(self, painter, option, widget):
        # Draw the default rectangle & selection border 
        super().paint(painter, option, widget)
        
        # Draw rectangle
        painter.setPen(QPen(Qt.GlobalColor.white, 1))
        painter.setBrush(QBrush(Qt.GlobalColor.black))
        painter.drawRect(self.rect)

        # Draw AND gate image centered in the rectangle
        img_x = self.rect.x() + (self.rect.width() - 32) / 2
        img_y = self.rect.y() + (self.rect.height() - 32) / 2
        painter.drawPixmap(int(img_x), int(img_y), 32, 32, self.image)

        # Draw three circles (inputs/outputs) on top
        painter.setBrush(Qt.GlobalColor.white)
        painter.setPen(QPen(Qt.GlobalColor.white))
        painter.drawEllipse(QPointF(self.rect.x(), self.rect.y() + 10), 3, 3)
        painter.drawEllipse(QPointF(self.rect.x(), self.rect.y() + 30), 3, 3)
        painter.drawEllipse(QPointF(self.rect.x() + self.rect.width(), self.rect.y() + 20), 3, 3)

        # Draw a more prominent selection border if selected
        if self.isSelected():
            pen = QPen(Qt.GlobalColor.blue, 2, Qt.PenStyle.DotLine)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(self.rect)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            snapped_point = GridScene.snap_to_grid(value.x(), value.y())
            snapped_pos = QPointF(snapped_point[0], snapped_point[1])
            scene = self.scene()
            if scene is not None:
                for view in scene.views():
                    view.viewport().update()
            return snapped_pos
        return super().itemChange(change, value)