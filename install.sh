#!/usr/bin/env sh

sudo cp pyimafe.py /bin/pyimafe

sudo chmod 755 /bin/pyimafe

sudo mkdir /usr/share/pixmaps/imafe/

sudo cp resources/*.png /usr/share/pixmaps/imafe/

sudo cp pyimafe.desktop /usr/share/applications/