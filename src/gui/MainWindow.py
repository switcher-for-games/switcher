#  Switcher, a tool for managing graphics and keymap profiles in games.
#  Copyright (C) 2020 Sam McCormack
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.
import asyncio
from typing import List

from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QMainWindow, QDialog

from gui.MainGUI import MainGUI
from gui.ManagePluginsDialog import ManagePluginsDialog
from gui.PluginWidget import PluginWidget
from utils import resources


class MainWindow(MainGUI, QMainWindow):
    """
    The main window of the application.
    """

    def __init__(self, application):
        MainGUI.__init__(self)
        QMainWindow.__init__(self)

        self.plugin_widgets: List[PluginWidget] = []

        self.application = application
        self.plugin_handler = application.plugin_handler

        self.plugin_handler.initialise()
        self.setup_ui()

    def setup_ui(self) -> None:
        uic.loadUi(resources.get_layout(), self)
        self.btn_plugins.clicked.connect(self.manage_plugins)

        plugins = self.plugin_handler.plugins

        cols = max(2, round(len(plugins) / 3))
        row, col = 0, 0

        for p in plugins:
            if col == cols:
                row += 1
                col = 0

            col += 1
            w = PluginWidget(p, self)
            self.grid.addWidget(w, row, col)

            self.plugin_widgets.append(w)
            asyncio.ensure_future(w.coro_initialise())

    def manage_plugins(self) -> None:
        dialog = ManagePluginsDialog(
            self, self.plugin_handler.get_installed_plugin_urls()
        )

        if dialog.exec() == QDialog.Accepted and (changes := dialog.get_changes()):
            self.plugin_handler.apply_changes(changes)
            self.application.restart()

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        # img = Image.open("background.png")
        # img = img.filter(ImageFilter.GaussianBlur(radius=10))
        # img.save("blur.png")

        # backgrnd = QPixmap("blur.png")
        # backgrnd = backgrnd.scaled(self.size(), Qt.KeepAspectRatioByExpanding)
        # palette = QPalette()
        # palette.setBrush(QPalette.Background, QBrush(backgrnd))
        # self.setPalette(palette)

        pass

    def resize_plugin_widgets(self):
        window_height = self.height()
        count = max(5, len(self.plugin_widgets))

        widget_height = window_height / count

        cap = 250
        if widget_height > cap:
            widget_height = cap

        for w in self.plugin_widgets:
            _width, _height = w.exact_size

            aspect_ratio = _width / _height
            widget_width = widget_height * aspect_ratio

            w.setFixedHeight(widget_height)
            w.setFixedWidth(widget_width)

            w.exact_size = (widget_width, widget_height)
            asyncio.ensure_future(w.coro_initialise())

            self.btn_plugins.setFixedWidth(widget_width)
