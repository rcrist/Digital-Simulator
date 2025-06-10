from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

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

        self.properties_widget = QWidget()
        self.layout = QVBoxLayout(self.properties_widget)

        # Label for Gates
        gates_label = QLabel("Gates")
        gates_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(gates_label)

        # Gate image buttons (logic gates only) in a 3x3 grid
        self.gate_buttons = {}
        gate_images = {
            "And": "Digital Simulator Tool/Images/and-gate_32x32_blue.png",
            "Or": "Digital Simulator Tool/Images/or-gate_32x32_blue.png",
            "Not": "Digital Simulator Tool/Images/not-gate_32x32_blue.png",
            "Nand": "Digital Simulator Tool/Images/nand-gate_32x32_blue.png",
            "Nor": "Digital Simulator Tool/Images/nor-gate_32x32_blue.png",
            "Xor": "Digital Simulator Tool/Images/xor-gate_32x32_blue.png",
            "Xnor": "Digital Simulator Tool/Images/xnor-gate_32x32_blue.png"
        }
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(8)
        for idx, (gate, img_path) in enumerate(gate_images.items()):
            btn = QPushButton()
            btn.setIcon(QIcon(img_path))
            btn.setIconSize(QSize(24, 24))
            btn.setToolTip(f"{gate} gate")
            btn.setFixedSize(32, 32)
            btn.clicked.connect(lambda checked=False, g=gate: self.add_gate(g))
            row = idx // 3
            col = idx % 3
            grid_layout.addWidget(btn, row, col)
            self.gate_buttons[gate] = btn
        self.layout.addWidget(grid_widget)

        # Label for IO
        io_label = QLabel("IO")
        io_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(io_label)

        # Add input/output components as image buttons below the grid
        io_images = {
            "Dip Switch": "Digital Simulator Tool/Images/dip_switch_32x32.png",
            "Slider Switch": "Digital Simulator Tool/Images/slider_switch_32x32_blue.png",
            "LED": "Digital Simulator Tool/Images/led_32x32.png"
        }
        io_widget = QWidget()
        io_layout = QHBoxLayout(io_widget)
        io_layout.setSpacing(8)
        for io, img_path in io_images.items():
            btn = QPushButton()
            btn.setIcon(QIcon(img_path))
            btn.setIconSize(QSize(24, 24))
            btn.setToolTip(io)
            btn.setFixedSize(32, 32)
            btn.clicked.connect(lambda checked=False, g=io: self.add_gate(g))
            io_layout.addWidget(btn)
            self.gate_buttons[io] = btn
        self.layout.addWidget(io_widget)

        self.layout.addStretch()
        self.setWidget(self.properties_widget)

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
            else:
                return

            gate.setPos(100, 100)
            self.scene.addItem(gate)