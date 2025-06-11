from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys
import os

# Add the parent directory to sys.path so 'Components' can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Components.seven_segment import SevenSegment

class MainWindow(QMainWindow):
    """ Main application window for the gate simulator. """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seven Segment Tester")
        self.setGeometry(400, 200, 800, 400)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setSceneRect(0, 0, 1400, 600)
        self.setCentralWidget(self.view)

        # Add a seven segment display to the scene
        self.seven_segment = SevenSegment()
        self.scene.addItem(self.seven_segment)
        self.seven_segment.setPos(100, 100)

    def closeEvent(self, event):
        try:
            self.scene.selectionChanged.disconnect(self.on_selection_changed)
        except Exception:
            pass
        super().closeEvent(event)

    def on_selection_changed(self):
        """Show controls if a component is selected, hide if not."""
        if hasattr(self, "scene") and self.scene is not None:
            try:
                selected = self.scene.selectedItems()
                self.properties_dock.show_controls(bool(selected), selected[0] if selected else None)
            except RuntimeError:
                # Scene has been deleted, ignore
                pass

if __name__ == "__main__":
    """ Main entry point for the application. """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())