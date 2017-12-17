## Headus UVlayout Bridge

>A bridge between Blender and Headus UVlayout for quick UVs unwrapping

Headus UVlayout Bridge is a [Blender](https://www.blender.org) add-on for exporting objects from Blender to Headus UVlayout for either quick uvwrapping. Its has multiple options and automation possibilities.

![Header Image](https://github.com/schroef/uvlayout_bridge/blob/master/wiki/images/suzanne-gui-header-image.jpg)

This addon requires [Headus UVlayout](https://www.uvlayout.com/) to be installed on the system.



## Installation Process

1. Download the latest [release](https://github.com/schroef/uvlayout_bridge/releases/) or clone the repository into a directory of your convenience.
2. If you downloaded the zip file.
3. Open Blender.
4. Go to File -> User Preferences -> Addons.
5. At the bottom of the window, chose *Install From File*.
6. Select the file `uvlayout_bridge_VERSION.zip` from your download location..
7. Activate the checkbox for the plugin that you will now find in the list.
8. Choose setting according to system:<br>-Choose the Headus UVlayout application path if your on Windows.<br>-Choose the Headus UVlayout version if your OSX user.
8. From startup the panel is located in the TOOLS panel.

# System Requirements

| **OS** | **Blender** | **UVlayout** |
| ------------- | ------------- | ------------- |
| OSX | Blender 2.78 | All Versions |
| Windows | Blender 2.78 | All Versions |
| Linux | Not Tested | Not Tested |


# Changelog

| **Version** | **Date** | **Change log** |
| ------------- | ------------- | ------------- |
| 0.6.1 | 16.12.2017 | • Updated set config read/writing, errors occurred reading and writing file<br>• Updated Keymaps, name errors
| 0.6 | 16.12.2017 | • Updated set config file, errors occurred with custom path. <br>• Updated WM call menu, now resizes when automation is checked.
| 0.5 | 15.12.2017 | • Added OSX support for load options <br>• Added extra load options (Weld UVs, Clean, Detach Flipped UVs)<br>• Added checker for export from local view (is not supported)<br>• Added Automation, automatic packing and automatic save and return<br>• Added hotkeys for popup menu (for clean workflow)<br>• Added hotkeys to add-on panel for quick acces<br>• Added Quick Export shortcut (quick exports according to last settings)<br>• Added add-on preferences saving options. On restart all settings will be loaded<br>• Added custom export folder. Useful for when errors occur and file needs to be saved, quick access to files.
| 0.4 | 07.12.2017 | • Added create backup when ‘Apply Modifier’ is added. <br>• Added option to export all visible objects, hidden and layers OFF won’t be exported.
| 0.3 | 05.12.2017 | • Added Apply modifier option
| 0.1 | 15.12.2017 | • First official release by Titus Lavrov

<!--
- Fill in data
    -
    -
-->

# Offical Blender Artist Thread
This is the [BlenderArtist thread](https://blenderartists.org/forum/showthread.php?441849-Add-on-Blender-lt-gt-UVLayout-bridge) where initial start from Titus Lavrov started. This version is a Fork of that source and has been optimized for OSX.

Copyright (C) 2017
