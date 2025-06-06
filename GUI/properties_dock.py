from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from GUI.led_widget import LEDWidget

class PropertiesDock(QDockWidget):
    """ Dock widget for displaying component properties """
    def __init__(self, parent=None, scene=None):
        super().__init__("Properties", parent)
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable |
                         QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        
        # Custom title bar to allow styling
        title = QLabel("Properties")
        title.setObjectName("PropertiesDockTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setTitleBarWidget(title)

        self.scene = scene
        self.selected_item = None
        
        self.properties_widget = QWidget()
        self.layout = QVBoxLayout(self.properties_widget)

        # Add controls for component type, rotation, and states
        self.type_label = QLabel("Type: None")
        self.layout.addWidget(self.type_label)

        # Add rotation controls
        self.rotation_slider = QSlider(Qt.Orientation.Horizontal)
        self.rotation_label = QLabel("Angle: 0°")
        self.rotation_slider.setRange(0, 360)
        self.rotation_slider.setSingleStep(90)
        self.rotation_title = QLabel("Rotation")
        self.layout.addWidget(self.rotation_title)
        self.layout.addWidget(self.rotation_slider)
        self.layout.addWidget(self.rotation_label)

        # Add a separator line above the LED States label
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(self.separator)
        self.state_title = QLabel("<b>States</b>")
        self.layout.addWidget(self.state_title)

        # Container for connector LEDs
        self.leds_container = QWidget()
        self.leds_layout = QVBoxLayout(self.leds_container)
        self.layout.addWidget(self.leds_container)

        # Add LED color selector (hidden by default)
        self.led_color_title = QLabel("LED Color")
        self.led_color_combo = QComboBox()
        self.led_color_combo.addItems(["red", "green", "yellow", "blue"])
        self.layout.addWidget(self.led_color_title)
        self.layout.addWidget(self.led_color_combo)
        self.led_color_title.setVisible(False)
        self.led_color_combo.setVisible(False)
        self.led_color_combo.currentTextChanged.connect(self.change_led_color)

        self.layout.addStretch()

        self.setWidget(self.properties_widget)

        self.rotation_slider.valueChanged.connect(self.update_rotation)

        # Hide all controls initially
        self.show_controls(False, None)

    def set_rotation_slider(self):
        angle = int(self.item.rotation() if hasattr(self.item, "rotation") else 0)
        self.rotation_slider.setValue(round(angle / 90) * 90)

    def update_rotation(self, value):
        selected_items = self.scene.selectedItems()
        if selected_items:
            self.selected_item = selected_items[0]

        # Snap to nearest 90 degrees
        snapped_value = round(value / 90) * 90
        if self.rotation_slider.value() != snapped_value:
            self.rotation_slider.setValue(snapped_value)
            return
        self.rotation_label.setText(f"Angle: {snapped_value}°")

        if self.selected_item:
            # Set transform origin to center
            bounding_rect = self.selected_item.boundingRect()
            center = bounding_rect.center()
            self.selected_item.setTransformOriginPoint(center)
            if hasattr(self.selected_item, "setRotationAngle"):
                self.selected_item.setRotationAngle(snapped_value)
            else:
                self.selected_item.setRotation(snapped_value)
            self.selected_item.update()
            self.refresh_scene_views()

    def show_controls(self, show: bool, selected: QGraphicsItem):
        """Show or hide all controls in the properties dock."""
        self.type_label.setVisible(show)
        self.rotation_title.setVisible(show)
        self.rotation_label.setVisible(show)
        self.rotation_slider.setVisible(show)
        self.separator.setVisible(show)
        self.state_title.setVisible(show)
        self.leds_container.setVisible(show)

        # Remove old LEDs and labels
        while self.leds_layout.count():
            child = self.leds_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Hide color selector by default
        self.led_color_title.setVisible(False)
        self.led_color_combo.setVisible(False)

        if selected:
            self.type_label.setText(f"Type: {type(selected).__name__}")

            # Show color selector if LED
            if type(selected).__name__ == "LED":
                self.led_color_title.setVisible(True)
                self.led_color_combo.setVisible(True)
                # Set combo to current color
                if hasattr(selected, "led_color"):
                    idx = self.led_color_combo.findText(selected.led_color)
                    if idx >= 0:
                        self.led_color_combo.setCurrentIndex(idx)
                self.led_color_combo.blockSignals(False)
                self.led_color_combo.currentTextChanged.disconnect()
                self.led_color_combo.currentTextChanged.connect(self.change_led_color)
                self.led_color_combo.blockSignals(False)
                self.selected_led = selected
            else:
                self.selected_led = None

            # Special handling for Wire
            if type(selected).__name__ == "Wire":
                row = QWidget()
                row_layout = QHBoxLayout(row)
                row_layout.setContentsMargins(0, 0, 0, 0)
                # Assume wire has an attribute 'state'
                led = LEDWidget(state=getattr(selected, "state", False))
                label = QLabel("Wire State")
                row_layout.addWidget(led)
                row_layout.addWidget(label)
                self.leds_layout.addWidget(row)

                # Connect LED click to toggle function
                led.clicked.connect(lambda: self.toggle_wire_state(selected))
            # Default: show connector LEDs if present
            elif hasattr(selected, "conns"):
                is_dip_switch = type(selected).__name__.lower() == "dipswitch"
                for idx, conn in enumerate(selected.conns):
                    conn_name = conn["name"]
                    row = QWidget()
                    row_layout = QHBoxLayout(row)
                    row_layout.setContentsMargins(0, 0, 0, 0)
                    led = LEDWidget(state=conn.get("state", False))
                    label = QLabel(str(conn_name))
                    row_layout.addWidget(led)
                    row_layout.addWidget(label)
                    self.leds_layout.addWidget(row)

                     # Only connect LED click if not a DIP switch
                    if not is_dip_switch:
                        led.clicked.connect(lambda i=idx: self.toggle_connector_state(selected, i))

        elif selected:
            self.type_label.setText(f"Type: {type(selected).__name__}")

    def refresh_scene_views(self):
        """Update the scene and all its views."""
        if self.selected_item:
            scene = self.selected_item.scene()
            if scene:
                scene.update()
                for view in scene.views():
                    view.viewport().update()

    def toggle_connector_state(self, selected, idx):
        """Toggle the state of the connector and update the LED."""
        if hasattr(selected, "conns") and 0 <= idx < len(selected.conns):
            conn = selected.conns[idx]
            conn["state"] = not conn.get("state", False)
            selected.update_state()
            self.show_controls(True, selected)  # Refresh LEDs

    def toggle_wire_state(self, selected):
        """Toggle the state of the wire and update the LED."""
        if hasattr(selected, "state"):
            selected.update_state()
            self.show_controls(True, selected)  # Refresh LED

    def change_led_color(self, color):
        """Change the color of the currently selected component if it is an LED."""
        selected_items = self.scene.selectedItems() if self.scene else []
        if selected_items:
            selected = selected_items[0]
            if type(selected).__name__ == "LED" and hasattr(selected, "set_led_color"):
                selected.set_led_color(color)
                self.refresh_scene_views()
