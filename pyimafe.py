#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Ferhat Geçdoğan All Rights Reserved.
# Distributed under the terms of the MIT License.
#

# PyImafe
#   Python3 implementation of Imafe image viewer (executable)
#
#   github.com/ferhatgec/imafe
#

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk, GdkPixbuf
import sys


class Imafe:
    image = 0
    title = 'PyImafe'

    def __init__(self):
        window = Gtk.Window()
        header_bar = Gtk.HeaderBar()
        box = Gtk.Box()

        header_bar.set_title(self.title)
        header_bar.set_show_close_button(True)

        window.set_size_request(600, 400)
        window.connect_after('destroy', self.destroy)

        box.set_spacing(5)

        box.set_orientation(Gtk.Orientation.VERTICAL)

        window.set_titlebar(header_bar)

        window.add(box)

        self.image = Gtk.Image()

        box.pack_start(self.image, True, True, 0)

        button = Gtk.Button(label='Open')

        header_bar.pack_start(button)

        button.connect_after('clicked', self.on_open_clicked)

        window.show_all()

    def destroy(window, self):
        Gtk.main_quit()

    def on_open_clicked(self, button):
        dialog = Gtk.FileChooserDialog(title='Open Image',
                                       parent=button.get_toplevel(),
                                       action=Gtk.FileChooserAction.OPEN)

        dialog.add_button(Gtk.STOCK_CANCEL, 0)
        dialog.add_button(Gtk.STOCK_OPEN, 1)
        dialog.set_default_response(1)

        filefilter = Gtk.FileFilter()
        filefilter.add_pixbuf_formats()

        dialog.set_filter(filefilter)

        if dialog.run() == 1:
            self.image.set_from_file(dialog.get_filename())
            dialog.destroy()


def main():
    app = Imafe()
    Gtk.main()


sys.exit(main())
