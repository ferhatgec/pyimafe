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
from os import path, getcwd

import sys

center: float = 0.5
resources_path = '/usr/share/pixmaps/imafe/{file}.png'

class Imafe:
    image = Gtk.Image()
    title = 'PyImafe'
    argument = ''

    header_bar = Gtk.HeaderBar()
    grid = Gtk.Grid()

    image_label = Gtk.Label()

    filename = Gtk.Entry()
    resolution = Gtk.Entry()

    # TODO: Implement Tyfe library in Python (github.com/ferhatgec/tyfe)
    # for file-type information.
    type = Gtk.Entry()

    switcher = Gtk.StackSwitcher()
    image_stack = Gtk.Stack()

    info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

    width = ''
    height = ''

    def __init__(self):
        window = Gtk.Window()
        box = Gtk.Box()

        self.header_bar.set_title(self.title)
        self.header_bar.set_show_close_button(True)

        window.set_size_request(700, 400)
        window.connect_after('destroy', self.destroy)

        self.initialize()

        self.image_stack.set_vexpand(True)
        self.image_stack.set_hexpand(True)

        self.switcher.halign = Gtk.Align.CENTER;
        self.switcher.set_stack(self.image_stack)

        box.set_spacing(5)
        self.info_box.set_spacing(5)

        box.set_orientation(Gtk.Orientation.VERTICAL)

        window.add(self.grid)

        self.grid.attach(self.switcher, 0, 0, 1, 1)
        self.grid.attach(self.image_stack, 0, 1, 1, 1)

        self.image_stack.add_titled(box, 'Image', 'Image')
        self.image_stack.add_titled(self.info_box, 'Info', 'Info')

        window.set_titlebar(self.header_bar)

        self.info_box.pack_start(self.filename, False, True, 0)
        self.info_box.pack_start(self.resolution, False, True, 1)
        self.info_box.pack_start(self.type, False, True, 2)

        if len(sys.argv) > 1:
            self.argument = (getcwd() + '/' + sys.argv[1])

            self.open_image()

        window.add(box)

        box.pack_start(self.image, True, True, 0)

        button = Gtk.Button(label='Open')

        self.header_bar.pack_start(button)

        button.connect_after('clicked', self.on_open_clicked)

        window.show_all()

    def destroy(window, self):
        Gtk.main_quit()

    def initialize(self):
        self.filename = self.set_info(self.filename)
        self.resolution = self.set_info(self.resolution)
        self.type = self.set_info(self.type)

        self.filename.set_text('...')
        self.resolution.set_text('...')
        self.type.set_text('...')

        if path.exists(resources_path.format(file='imafe_main')):
            __path = resources_path.format(file='imafe_main')

            self.image.set_from_file(__path)

    def open_image(self):
        self.image.set_from_file(self.argument)

        self.set(self.argument)

    def set_info(self, entry: Gtk.Entry) -> Gtk.Entry:
        entry.set_can_focus(False)
        entry.set_editable(False)

        entry.set_halign(Gtk.Align.FILL)
        entry.set_valign(Gtk.Align.CENTER)

        entry.set_alignment(xalign=center)

        entry.margin = 20

        return entry

    def match(self, file: str) -> str:
        return {
            '.png': 'PNG-Image',

            '.jpeg': 'JPEG-Image',
            '.jpg': 'JPEG-Image',

            '.gif': 'GIF-Image'
        }.get(file, 'Regular (?)')

    def get_type_of_file(self, file: str) -> str:
        file = path.splitext(file)[1]

        return self.match(file)

    def set(self, file: str):
        self.image.set_from_file(file)

        self.width = str(self.image.get_allocation().width)
        self.height = str(self.image.get_allocation().height)

        self.header_bar.set_title(file)

        self.filename.set_text('Path: '
                               + file)

        self.resolution.set_text('Resolution w x h: '
                                 + self.width
                                 + ' x '
                                 + self.height)

        self.type.set_text('Type: '
                           + self.get_type_of_file(file))

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
            dialog_filename = dialog.get_filename()

            self.set(dialog_filename)

            dialog.destroy()


def main():
    app = Imafe()

    Gtk.main()


sys.exit(main())
