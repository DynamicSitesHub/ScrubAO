from qgis.PyQt.QtWidgets import QAction
from .ao_scrub_gui import AOScrubDialog

class AOScrubToolPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_menu = "&AO Scrub Tool"
        self.action = None
        self.dialog = None

    def initGui(self):
        self.action = QAction("AO Scrub Tool", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu(self.plugin_menu, self.action)

    def unload(self):
        if self.action:
            self.iface.removePluginMenu(self.plugin_menu, self.action)

    def run(self):
        if not self.dialog:
            self.dialog = AOScrubDialog(self.iface)
        self.dialog.show()
        self.dialog.raise_()
        self.dialog.activateWindow()
