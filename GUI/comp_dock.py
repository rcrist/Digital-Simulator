from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from GUI.theme_state import is_dark_mode
from Components.and_gate import AndGate
from Components.or_gate import OrGate
from Components.not_gate import NotGate
from Components.nand_gate import NandGate
from Components.nor_gate import NorGate
from Components.xor_gate import XorGate
from Components.xnor_gate import XnorGate
from Components.dip_switch import DipSwitch
from Components.slider_switch import SliderSwitch
from Components.led import LED
from Components.seven_segment import SevenSegment
from Components.clock import Clock
from Components.switchbar import Switchbar
from Components.ledbar import Ledbar
from ICs.SN7408 import SN7408

class ComponentDock(QDockWidget):
    """ Component widget for selecting and displaying components """
    def __init__(self, parent=None, scene=None, simulator=None):
        super().__init__("Properties", parent)
        self.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable |
                         QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        
        # Custom title bar to allow styling
        title = QLabel("Components")
        title.setObjectName("ComponentsDockTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setContentsMargins(10, 0, 0, 0)  # Add 10px left margin
        self.setTitleBarWidget(title)

        self.scene = scene
        self.simulator = simulator
        self.library_images = {}

        self.properties_widget = QWidget()
        self.layout = QVBoxLayout(self.properties_widget)

        # Gate image buttons (logic gates only) in a 3x3 grid
        self.gate_buttons = {}
        gate_images = {
            "And": "Digital Simulator Tool/Images/and-gate_64x64_blue.png",
            "Or": "Digital Simulator Tool/Images/or-gate_64x64_blue.png",
            "Not": "Digital Simulator Tool/Images/not-gate_64x64_blue.png",
            "Nand": "Digital Simulator Tool/Images/nand-gate_64x64_blue.png",
            "Nor": "Digital Simulator Tool/Images/nor-gate_64x64_blue.png",
            "Xor": "Digital Simulator Tool/Images/xor-gate_64x64_blue.png",
            "Xnor": "Digital Simulator Tool/Images/xnor-gate_64x64_blue.png"
        }
        # Gates
        grid_widget = self.create_image_buttons(gate_images, layout_class=QGridLayout)
        self.layout.addWidget(grid_widget)

        # Label for Switches
        switch_label = QLabel("Switches")
        switch_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(switch_label)

        # Add input/output components as image buttons below the grid
        switch_images = {
            "Dip Switch": "Digital Simulator Tool/Images/dip_switch_32x32.png",
            "Slider Switch": "Digital Simulator Tool/Images/slider_switch_32x32_blue.png",
            "Clock": "Digital Simulator Tool/Images/clock_32x32.png",
            "Switchbar": "Digital Simulator Tool/Images/switchbar_32x32.png"
        }
        # Switches
        switch_widget = self.create_image_buttons(switch_images, layout_class=QGridLayout)
        self.layout.addWidget(switch_widget)

        # Label for Displays
        display_label = QLabel("Displays")
        display_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(display_label)

        # Add display components as image buttons below the switches
        display_images = {
            "LED": "Digital Simulator Tool/Images/led_32x32.png",
            "Ledbar": "Digital Simulator Tool/Images/ledbar_32x32.png",
            "Seven Segment": "Digital Simulator Tool/Images/seven-segment.png"
        }

        display_widget = self.create_image_buttons(display_images, layout_class=QGridLayout)
        self.layout.addWidget(display_widget)

        # Label for Circuit Library
        library_label = QLabel("Circuit Library")
        library_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(library_label)

        self.library_images = {
            "SN7400": "Digital Simulator Tool/Images/integrated-circuit_32x32.png",
            "SN7402": "Digital Simulator Tool/Images/integrated-circuit_32x32.png",
            "SN7408": "Digital Simulator Tool/Images/integrated-circuit_32x32.png",
        }

        library_widget = self.create_image_buttons(self.library_images, layout_class=QGridLayout)
        self.layout.addWidget(library_widget)

        self.layout.addStretch()
        self.setWidget(self.properties_widget)

    def create_image_buttons(self, items, layout_class=QHBoxLayout, icon_size=QSize(48, 48), button_size=QSize(40, 40)):
        widget = QWidget()
        layout = layout_class(widget)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        if (items == self.library_images):
            layout.setSpacing(0)
            row, col = 0, 0
            for idx, (name, img_path) in enumerate(items.items()):
                # Create button with image
                btn = QPushButton()
                btn.setIcon(QIcon(img_path))
                btn.setIconSize(icon_size)
                btn.setToolTip(name)
                btn.setFixedSize(button_size)
                btn.clicked.connect(lambda checked=False, g=name: self.add_gate(g))
                self.gate_buttons[name] = btn

                # Create label with component name
                name_label = QLabel(name)
                name_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

                # Create a vertical layout for button + label
                vbox = QVBoxLayout()
                vbox.setContentsMargins(0, 0, 6, 0)
                vbox.addWidget(btn)
                vbox.addWidget(name_label)

                # Create a container widget for the vbox
                container = QWidget()
                container.setLayout(vbox)

                layout.addWidget(container, row, col)
                col += 1
                if col >= 3:
                    col = 0
                    row += 1
        else:
            row, col = 0, 0
            for idx, (name, img_path) in enumerate(items.items()):
                btn = QPushButton()
                btn.setIcon(QIcon(img_path))
                btn.setIconSize(icon_size)
                btn.setToolTip(name)
                btn.setFixedSize(button_size)
                btn.clicked.connect(lambda checked=False, g=name: self.add_gate(g))
                layout.addWidget(btn, row, col)
                self.gate_buttons[name] = btn
                col += 1
                if col >= 3:
                    col = 0
                    row += 1

        return widget

    def add_gate(self, gate_type):
        """Create the associated gate on the canvas/scene """
        if self.scene is not None:
            # You may need to adapt this to your scene's API
            if gate_type == "And":
                gate = AndGate()
            elif gate_type == "Or":
                gate = OrGate()
            elif gate_type == "Not":
                gate = NotGate()
            elif gate_type == "Nand":
                gate = NandGate()
            elif gate_type == "Nor":
                gate = NorGate()
            elif gate_type == "Xor":
                gate = XorGate()
            elif gate_type == "Xnor":
                gate = XnorGate()
            elif gate_type == "Dip Switch":
                gate = DipSwitch(self.simulator)
            elif gate_type == "Slider Switch":
                gate = SliderSwitch(self.simulator)
            elif gate_type == "LED":
                gate = LED()
            elif gate_type == "Seven Segment":
                gate = SevenSegment()
            elif gate_type == "Clock":
                gate = Clock(self.simulator)
            elif gate_type == "Switchbar":
                gate = Switchbar(self.simulator)
            elif gate_type == "Ledbar":
                gate = Ledbar()
            elif gate_type == "SN7408":
                gate = SN7408()
            else:
                return

            gate.setPos(100, 100)
            self.scene.addItem(gate)