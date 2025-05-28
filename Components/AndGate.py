from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from Components.Comp import Comp
import GUI.TopMenu as TopMenu

class AndGate(QGraphicsRectItem, Comp):
    def __init__(self, x, y, w=40, h=40):
        super().__init__(QRectF(x, y, w, h))
        self.rect = QRectF(x, y, w, h)

    def paint(self, painter, option, widget):
        # Set pen color based on theme
        if TopMenu.is_dark_mode and not getattr(TopMenu, "is_printing", False):
            gate_pen = QPen(Qt.GlobalColor.white, 2)
            circle_pen = QPen(Qt.GlobalColor.white)
        else:
            gate_pen = QPen(Qt.GlobalColor.black, 2)
            circle_pen = QPen(Qt.GlobalColor.black)

        painter.setPen(gate_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        margin = 3
        x = self.rect.x() + margin
        y = self.rect.y() + margin
        w = self.rect.width() - 2 * margin
        h = self.rect.height() - 2 * margin

        # Draw AND gate shape facing right using QPainterPath
        path = QPainterPath()

        # Start at left-middle
        path.moveTo(x, y)
        path.lineTo(x, y + h)
        path.arcTo(x, y, w, h, 270, 180)
        path.lineTo(x, y)

        painter.drawPath(path)

        # Draw three circles - 2 inputs and 1 output
        painter.setPen(circle_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(QPointF(self.rect.x(), self.rect.y() + 10), 3, 3)
        painter.drawEllipse(QPointF(self.rect.x(), self.rect.y() + 30), 3, 3)
        painter.drawEllipse(QPointF(self.rect.x() + self.rect.width(), self.rect.y() + 20), 3, 3)

        # Draw selection rectangle if selected
        if option.state & QStyle.StateFlag.State_Selected:
            selection_pen = QPen(Qt.GlobalColor.blue, 1, Qt.PenStyle.DashLine)
            painter.setPen(selection_pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(self.rect)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemSelectedHasChanged:
            scene = self.scene()
            if scene is not None:
                for view in scene.views():
                    view.viewport().update()
    
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            from GUI.GridScene import GridScene
            snapped_point = GridScene.snap_to_grid(value.x(), value.y())
            snapped_pos = QPointF(snapped_point[0], snapped_point[1])
            scene = self.scene()
            if scene is not None:
                for view in scene.views():
                    view.viewport().update()
            return snapped_pos
        return super().itemChange(change, value)
    
    def to_dict(self):
        pos = self.pos()
        return {
            "type": "and_gate",
            "x": self.rect.x(),
            "y": self.rect.y(),
            "width": self.rect.width(),
            "height": self.rect.height(),
            "rotation": self.rotation(),
            "pos_x": pos.x(),
            "pos_y": pos.y()
        }

    @classmethod
    def from_dict(cls, data):
        rect = cls(
            data.get("x", 0),
            data.get("y", 0),
            data.get("w", 40),
            data.get("h", 40)
        )
        rect.setRotation(data.get("rotation", 0))
        # Set the scene position after creation
        rect.setPos(data.get("pos_x", 0), data.get("pos_y", 0))
        return rect