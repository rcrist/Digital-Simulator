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
        self.rotation_slider = QSlider(Qt.Orientation.Horizontal)

        self.rotation_slider.setRange(0, 360)
        self.rotation_slider.setSingleStep(90)
        self.rotation_slider.setTickInterval(90)
        self.rotation_slider.setTickPosition(QSlider.TickPosition.TicksBelow)


        self.form_layout.addRow(QLabel("Rotation"), self.rotation_slider)

        self.main_widget.setLayout(self.form_layout)
        self.setWidget(self.main_widget)
        self.item = None

        self.rotation_slider.valueChanged.connect(self.update_rotation)

    def set_controls(self, item):
        self.item = item
        if hasattr(item, "getRotationAngle"):
            angle = item.getRotationAngle()
            self.rotation_slider.setValue(angle)
        else:
            self.rotation_slider.setValue(0)

    def update_rotation(self, value):
        # Snap to nearest 90 degrees
        snapped_value = round(value / 90) * 90
        if self.rotation_slider.value() != snapped_value:
            self.rotation_slider.setValue(snapped_value)
            return
        if self.item:
            self.item.setRotationAngle(snapped_value)
            self.item.update()
            # Ensure the scene and all views are updated to clear artifacts
            scene = self.item.scene()
            if scene:
                scene.update()
                for view in scene.views():
                    view.viewport().update()