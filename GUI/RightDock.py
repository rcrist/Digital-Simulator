from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from GUI.GridScene import *

class RightDock(QDockWidget):
    def __init__(self, parent=None, scene=None, view=None):
        super().__init__("Properties", parent)
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.setMinimumWidth(150)
        self.scene = scene
        self.view = view
        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        # Position properties
        self.position_label = QLabel("Position:")
        self.position_x = QLineEdit()
        self.position_y = QLineEdit()
        self.layout.addWidget(self.position_label)
        self.layout.addWidget(QLabel("X:"))
        self.layout.addWidget(self.position_x)
        self.layout.addWidget(QLabel("Y:"))
        self.layout.addWidget(self.position_y)

        # Rotation controls
        self.rotation_label = QLabel("Rotation:")
        self.rotation_combo = QComboBox()
        angles = [str(angle) + "°" for angle in range(0, 361, 45)]
        self.rotation_combo.addItems(angles)
        self.layout.addWidget(self.rotation_label)
        self.layout.addWidget(self.rotation_combo)

        self.layout.addStretch()
        self.main_widget.setLayout(self.layout)
        self.setWidget(self.main_widget)

        # Connect rotation change to slot
        self.rotation_combo.currentIndexChanged.connect(self.rotate_selected_item)

        # Connect scene selection change to update position fields
        if self.scene is not None:
            self.scene.selectionChanged.connect(self.update_position_fields)
            # Install event filter for real-time position updates
            self.scene.installEventFilter(self)

        # Connect manual edits to move the item
        self.position_x.editingFinished.connect(self.move_selected_item)
        self.position_y.editingFinished.connect(self.move_selected_item)
    def closeEvent(self, event):
        if self.scene is not None:
            try:
                self.scene.selectionChanged.disconnect(self.update_position_fields)
            except Exception:
                pass
        super().closeEvent(event)
        
    def update_position_fields(self):
        try:
            selected_items = self.scene.selectedItems() if self.scene else []
            if selected_items:
                item = selected_items[0]
                pos = item.scenePos()
                self.position_x.setText(str(int(pos.x())))
                self.position_y.setText(str(int(pos.y())))
            else:
                self.position_x.setText("")
                self.position_y.setText("")
        except RuntimeError:
            # Scene or item was deleted, ignore update
            pass

    def move_selected_item(self):
        if not self.scene:
            return
        selected_items = self.scene.selectedItems()
        if not selected_items:
            return
        try:
            x = float(self.position_x.text())
            y = float(self.position_y.text())
        except ValueError:
            return
        item = selected_items[0]
        item.setPos(x, y)

    def eventFilter(self, obj, event):
        # Real-time update: listen for item position changes
        if event.type() in (QEvent.Type.GraphicsSceneMouseMove, QEvent.Type.GraphicsSceneMouseRelease):
            self.update_position_fields()
        return super().eventFilter(obj, event)

    def rotate_selected_item(self):
        if not self.scene:
            return
        selected_items = self.scene.selectedItems()
        if not selected_items:
            return
        angle_str = self.rotation_combo.currentText().replace("°", "")
        try:
            angle = float(angle_str)
        except ValueError:
            angle = 0
        for item in selected_items:
            # Set the transform origin to the center of the item's bounding rect
            center = item.boundingRect().center()
            item.setTransformOriginPoint(center)
            item.setRotation(angle)
            if self.scene is not None:
                for view in self.scene.views():
                    view.viewport().update()