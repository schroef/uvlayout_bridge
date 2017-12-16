# BLender2UVlayout Bridge - Quick UVunwrapping using Headus UVlayout

Headus UVlayout Bridge is a [Blender](https://www.blender.org) add-on for quick exporting objects from Blender to UVlayout for quick and fats UVunwrapping.
This addon requires [Headus UVlayout](https://www.uvlayout.com/) installed on the OS (OSX - Windows).

![Header Image](https://raw.githubusercontent.com/wiki/schroef/uvlayout_bridge/wiki/image/suzanne-header-image.jpg)


# Installation Process


## Changelog

### Version 0.5
- Added OSX support for load options
- Added extra load options (Weld UVs, Clean, Detach Flipped UVs)
- Added checker for export from local view (is not supported)
- Added Automation, automatic packing and automatic save and return
- Added hotkeys for popup menu (for clean workflow)
- Added hotkeys to add-on panel for quick acces
- Added Quick Export shortcut (quick exports according to last settings)
- Added add-on preferences saving options. On restart all settings will be loaded
- Added custom export folder. Useful for when errors occur and file needs to be saved, quick access to files.

### Version 0.4
- Added create backup when ‘Apply Modifier’ is added.
- Added option to export all visible objects, hidden and layers OFF won’t be exported.

### Version 0.3
- Added Apply modifier option

### Version 0.1
First official release. By Titus Lavrov

- Fill in data
    -
    -

## License
UVlayout Bridge

Copyright (C) 2017  Rombout Versluijs

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
version 2 as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

This Blender plugin is based on the research paper "Recovery of Intrinsic
and Extrinsic Camera Parameters Using Perspective Views of Rectangles" by
T. N. Tan, G. D. Sullivan and K. D. Baker, Department of Computer Science,
The University of Reading, Berkshire RG6 6AY, UK,
from the Proceedings of the British Machine Vision Conference, published by
the BMVA Press.
