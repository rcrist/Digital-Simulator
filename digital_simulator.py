from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys

from GUI.grid_scene import GridScene
from GUI.properties_dock import PropertiesDock
from GUI.comp_dock import ComponentDock
from GUI.menu_bar import MenuBar

class MainWindow(QMainWindow):
    """ Main application window for the gate simulator. """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Component Editor")
        self.setGeometry(400, 200, 800, 400)

        self.scene = GridScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setSceneRect(0, 0, 1400, 600)
        self.setCentralWidget(self.view)

        # Create the menu bar
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Create the component dock
        self.component_dock = ComponentDock(self, self.scene)
        self.component_dock.setObjectName("ComponentDock")
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.component_dock)
        self.component_dock.setMinimumWidth(150)

        # Create the properties dock
        self.properties_dock = PropertiesDock(self, self.scene)
        self.properties_dock.setObjectName("PropertiesDock")
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.properties_dock)
        self.properties_dock.setMinimumWidth(200)

        # Connect selection change to show/hide controls
        self.scene.selectionChanged.connect(self.on_selection_changed)

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