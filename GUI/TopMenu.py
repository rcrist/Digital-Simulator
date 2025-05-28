from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
import GUI.config as config
from Components.AndGate import AndGate
import json

is_dark_mode = True
is_printing = False

class TopMenu(QMenuBar):
    def __init__(self, parent=None, scene=None, view=None):
        super().__init__(parent)
        self.scene = scene
        self.view = view

        # File Menu
        file_menu = self.addMenu("File")
        new_action = file_menu.addAction("New")
        new_action.triggered.connect(self.new_file)
        open_action = file_menu.addAction("Open")
        open_action.triggered.connect(self.open_file)
        save_action = file_menu.addAction("Save")
        save_action.triggered.connect(self.save_file)
        print_action = file_menu.addAction("Print")
        print_action.triggered.connect(self.print_diagram)
        file_menu.addSeparator()
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(QApplication.instance().quit)

        # Settings Menu
        settings_menu = self.addMenu("Settings")
        toggle_grid_action = settings_menu.addAction("Toggle Grid")
        toggle_grid_action.triggered.connect(self.toggle_grid)
        toggle_theme_action = settings_menu.addAction("Toggle Theme")
        toggle_theme_action.triggered.connect(self.toggle_theme)

        # Help Menu
        help_menu = self.addMenu("Help")
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about_dialog)

    def show_about_dialog(self):
        QMessageBox.about(self, "About Digital Simulator", 
            "Digital Simulator Tool\n\n"
            "A simple digital circuit simulator built with PyQt6.\n"
            "Created in 2025 by Rick A. Crist.\n\n"
            "This tool allows you to create and simulate digital circuits using basic components like AND gates.\n")

    def toggle_theme(self):
        global is_dark_mode
        is_dark_mode = not is_dark_mode

        if is_dark_mode:
            self.apply_dark_theme()
        else:
            self.apply_light_theme()

    def apply_dark_theme(self):
        app = QApplication.instance()
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        app.setPalette(dark_palette)
        self.setStyleSheet("""
            QMenuBar, QMenu, QMenuBar::item, QMenu::item {
                background: #000000;
                color: #fff;
            }
            QMenuBar::item:selected, QMenu::item:selected {
                background: #2a82da;
            }
        """)

        # Set canvas (scene/view) background to black
        main_window = self.parent()
        if hasattr(main_window, "scene"):
            main_window.scene.setBackgroundBrush(QBrush(Qt.GlobalColor.black))
            main_window.scene.update()

    def apply_light_theme(self):
        app = QApplication.instance()
        app.setPalette(QApplication.style().standardPalette())
        self.setStyleSheet("""
            QMenuBar, QMenu, QMenuBar::item, QMenu::item {
                background: #f0f0f0;
                color: #000;
            }
            QMenuBar::item:selected, QMenu::item:selected {
                background: #d0d0d0;
            }
        """)

        # Set canvas (scene/view) background to white
        main_window = self.parent()
        if hasattr(main_window, "scene"):
            main_window.scene.setBackgroundBrush(QBrush(Qt.GlobalColor.white))
            main_window.scene.update()

    def toggle_grid(self):
        config.is_grid_enabled = not config.is_grid_enabled

        # Update the view to refresh the grid
        main_window = self.parent()
        if hasattr(main_window, "view"):
            main_window.view.viewport().update()

    def new_file(self):
        main_window = self.parent()
        if hasattr(main_window, "scene"):
            main_window.scene.clear()
        else:
            QMessageBox.information(self, "New", "Scene clearing is not implemented.")

    def open_file(self):
        main_window = self.parent()
        if not hasattr(main_window, "scene"):
            QMessageBox.information(self, "Open", "Scene loading is not implemented.")
            return
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Diagram", "", "Diagram Files (*.json);;All Files (*)")
        if file_name:
            try:
                with open(file_name, "r", encoding="utf-8") as f:
                    items_data = json.load(f)
                main_window.scene.clear()
                for item_data in items_data:
                    item = self.deserialize_item(item_data)
                    if item:
                        main_window.scene.addItem(item)
            except Exception as e:
                QMessageBox.warning(self, "Open", f"Failed to open file:\n{e}")

    def save_file(self):
        main_window = self.parent()
        if not hasattr(main_window, "scene"):
            QMessageBox.information(self, "Save", "Scene saving is not implemented.")
            return
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Diagram", "", "Diagram Files (*.json);;All Files (*)")
        if file_name:
            try:
                items_data = [self.serialize_item(item) for item in main_window.scene.items()]
                # Remove None items (if any)
                items_data = [item for item in items_data if item is not None]
                with open(file_name, "w", encoding="utf-8") as f:
                    json.dump(items_data, f, indent=2)
            except Exception as e:
                QMessageBox.warning(self, "Save", f"Failed to save file:\n{e}")

    def serialize_item(self, item):
        if isinstance(item, AndGate):
            return item.to_dict()
        return None

    def deserialize_item(self, data):
        if not data:
            return None
        t = data.get("type", "")
        if t == "and_gate":
            return AndGate.from_dict(data)
        return None
    
    def print_diagram(self):
        global is_printing
        main_window = self.parent()
        if not hasattr(main_window, "view"):
            QMessageBox.information(self, "Print", "Nothing to print.")
            return

        was_dark_mode = is_dark_mode
        is_printing = True  # Set printing flag

        # --- Disable grid before printing ---
        grid_was_enabled = config.is_grid_enabled
        config.is_grid_enabled = False
        if hasattr(main_window, "view"):
            main_window.view.viewport().update()

        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec():
            painter = QPainter(printer)
            main_window.view.render(painter)
            painter.end()

        # Restore dark theme if it was previously enabled
        if was_dark_mode:
            self.apply_dark_theme()

        # --- Restore grid state after printing ---
        config.is_grid_enabled = grid_was_enabled
        if hasattr(main_window, "view"):
            main_window.view.viewport().update()

        is_printing = False  # Reset printing flag

    @staticmethod
    def is_dark_mode():
        return is_dark_mode