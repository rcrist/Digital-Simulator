from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import QRectF
from GUI.GridScene import GridScene

class AppView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)

    # Called by the Qt framework whenever the background needs to be redrawn
    def drawBackground(self, painter: QPainter, rect: QRectF):
        if self.scene():
            GridScene.drawBackground(self.scene(), painter, rect)