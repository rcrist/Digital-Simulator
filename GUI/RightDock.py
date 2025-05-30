from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from Components.AndGate import AndGate

class RightDock(QDockWidget):
    def __init__(self, parent=None, scene=None):
        super().__init__("Properties", parent)
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable | 
                         QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        self.setFloating(False)

        self.scene = scene
        self.main_widget = QWidget()
        self.form_layout = QFormLayout()

        # Location label
        self.location_label = QLabel("X: 0, Y: 0")
        self.form_layout.addRow(QLabel("Position"), self.location_label)

        self.rotation_slider = QSlider(Qt.Orientation.Horizontal)
        self.rotation_label = QLabel("0°")

        self.rotation_slider.setRange(0, 360)
        self.rotation_slider.setSingleStep(90)
        self.rotation_slider.setTickInterval(90)
        self.rotation_slider.setTickPosition(QSlider.TickPosition.TicksBelow)

        self.form_layout.addRow(QLabel("Rotation"), self.rotation_slider)
        self.form_layout.addRow(QLabel("Angle"), self.rotation_label)

        self.main_widget.setLayout(self.form_layout)
        self.setWidget(self.main_widget)
        self.item = None

        self.rotation_slider.valueChanged.connect(self.update_rotation)

    def set_controls(self, item):
        self.item = item
        # Update location label
        pos = item.pos()
        self.location_label.setText(f"X: {int(pos.x())}, Y: {int(pos.y())}")
        if hasattr(item, "getRotationAngle"):
            angle = item.getRotationAngle()
            self.rotation_slider.setValue(angle)
            self.rotation_label.setText(f"{angle}°")
        else:
            self.rotation_slider.setValue(0)
            self.rotation_label.setText("0°")

        # Connect to item's position change if not already connected
        if hasattr(item, "scene") and item.scene():
            item.scene().selectionChanged.connect(self.update_location_from_item)
        if hasattr(item, "itemChange"):
            item.itemChange = self._wrap_itemChange(item.itemChange)

    def update_location_from_item(self):
        if self.item:
            pos = self.item.pos()
            self.location_label.setText(f"X: {int(pos.x())}, Y: {int(pos.y())}")

    def _wrap_itemChange(self, original_itemChange):
        def new_itemChange(change, value):
            if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
                if self.item:
                    pos = value
                    self.location_label.setText(f"X: {int(pos.x())}, Y: {int(pos.y())}")
            return original_itemChange(change, value)
        return new_itemChange

    def update_rotation(self, value):
        # Snap to nearest 90 degrees
        snapped_value = round(value / 90) * 90
        if self.rotation_slider.value() != snapped_value:
            self.rotation_slider.setValue(snapped_value)
            return
        self.rotation_label.setText(f"{snapped_value}°")
        if self.item:
            self.item.setRotationAngle(snapped_value)
            self.item.update()
            scene = self.item.scene()
            if scene:
                scene.update()
                for view in scene.views():
                    view.viewport().update()