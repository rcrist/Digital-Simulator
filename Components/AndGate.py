from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from GUI.GridScene import GridScene

class AndGate(QGraphicsPathItem):
    def __init__(self, x, y, w=60, h=40):
        super().__init__()

        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )

        path = QPainterPath()
        # Start at top-left
        path.moveTo(x, y)
        path.lineTo(x, y + h)
        path.lineTo(x + w / 2, y + h)
        path.arcTo(x + w / 2, y, w / 2, h, 270, 180)
        path.lineTo(x, y)
        self.setPath(path)
        # Set pen color to white
        self.setPen(QPen(Qt.GlobalColor.white, 1))

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
                # Extract x and y from value (which is a QPointF)
                snapped_point = GridScene.snap_to_grid(value.x(), value.y())
                snapped_pos = QPointF(snapped_point[0], snapped_point[1])

                # Force the view to update to prevent artifacts
                scene = self.scene()
                if scene is not None:
                    for view in scene.views():
                        view.viewport().update()
                        
                return snapped_pos
        return super().itemChange(change, value)