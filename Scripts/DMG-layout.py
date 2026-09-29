#!/usr/bin/env python3
"""Write Finder presentation metadata on a mounted, writable disk image."""
import os
import sys
from ds_store import DSStore

volume = os.path.abspath(sys.argv[1])
with open(sys.argv[2], 'rb') as alias_file:
    background_alias = alias_file.read()
with DSStore.open(os.path.join(volume, '.DS_Store'), 'w+') as store:
    store['.']['vSrn'] = ('long', 1)
    store['.']['icvl'] = ('type', 'icnv')
    store['.']['vstl'] = ('type', 'icnv')
    store['.']['ICVO'] = ('bool', True)
    store['.']['bwsp'] = {
        'WindowBounds': '{{180, 160}, {600, 360}}',
        'ShowToolbar': False, 'ShowSidebar': False, 'ShowStatusBar': False,
        'ShowPathbar': False, 'ShowTabView': False, 'ContainerShowSidebar': False,
        'PreviewPaneVisibility': False,
    }
    store['.']['icvp'] = {
        'viewOptionsVersion': 1, 'backgroundType': 2,
        'backgroundColorRed': 1.0, 'backgroundColorGreen': 1.0, 'backgroundColorBlue': 1.0,
        'backgroundImageAlias': background_alias,
        'iconSize': 92.0, 'textSize': 13.0, 'arrangeBy': 'none',
        'gridSpacing': 100.0, 'gridOffsetX': 0.0, 'gridOffsetY': 0.0,
        'scrollPositionX': 0.0, 'scrollPositionY': 0.0,
        'labelOnBottom': True, 'showItemInfo': False, 'showIconPreview': False,
    }
    store['pika.app']['Iloc'] = (150, 170)
    store['Drag to Applications']['Iloc'] = (450, 170)
