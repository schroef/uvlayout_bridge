# Changelog
All notable changes to this project will be documented in this file.


## [v0.7.5] - 2024-07-27
# Added
- UVchannel map preview toggle, when switching uv channel. the preview actively changes and also set index of active UVmap 

## [v0.7.41] - 2024-07-25
# Fixed
- missing check for OSX app path set

## [v0.7.4] - 2024-07-25
# Fixed
- Automation Optimize, didnt do anything code fixed
- Show warning when exporting and custom path doesnt exist or is wrong

# Changed
- Code cleanup
- Panel design is using split_property ala 2.8 Design
- Dialog operator now uses duplicate of panel by using wm.call_panel > easier and no double code
- Automation is either pack or optimize, running both commands wasnt doing anything since optimize also packs uvs

## [v0.7.3] - 2024-07-24
# Fixed
- Export error if app path is not set, Panel shows red error with set app path option

## [v0.7.2] - 2024-07-23
# Fixed
- Changed parameter for OBJ importer and exporter.

# Added
- check for different Blender versions, they use different operators and parameters
- Show alert for when custom path does not exist, path turns red

# Changed
- info custom path is added to tooltip
- Removed Local check, seems to be working now without issues perhaps due to new viewlayer system

## [v0.7.1] - 2021-11-10
# Changed
- get path and files moved to its own function, same code was used 6 times

## [v0.7.0] - 2021-11-10
# Added
- Export custom path now in export options panel > easier accesible

# Changed
- Better check if we cancel or send file back to Blender > returns cancel or done report in bottom

## [v0.7.0] - 2021-11-06
# Added
- Forced reimport > when commands fails
- Optimize options > auto drops geometry, flattens, optimizes, packs, saves and returns to Blender
- Function to send tmp, edit & obj files to UVlayout. This allows user to easily open them, the ui from UVlayout is very outdated and tedious to work with.

# Changed
- If not mods are in mesh gray out menu option
- If 1 UV channel in mesh hide UV layout sub panel
- Moved panel to Tool catergory > save vertical menu from being to crowed

## [v0.6.9] - 2021-11-06
# Fixed
- Autosave & close kept running when automation was off


## [v0.6.8] - 2021-11-04
# Fixed
- Concate error in export operator > addon_prefs, "uvlb_winPath" caused error 
- OBJ importer > global_clight_size taken out in new OBJ importer
- bl293 'apply_as" has changed
- Check local bool was not working properly. Added warning text, it has issues now and doen not transfering work done in UVlayout
- Missing options for Windows multiple options were not working and added in export

# Changed
- Added split_property > new 280 layout method
- Panel uses now sub-panel introduced in 2.80

## [v0.6.7] - 20-03-20
## Changed
- custom properties saved to addon prefs instead of in scene
  Mentioned by Brechts https://developer.blender.org/T74954#895043
  https://docs.blender.org/api/current/bpy.types.AddonPreferences.html
  Im Skipping this because i want this to be per scene
- Changed string path to DIR_PATH

## [v0.6.6] - 20-03-19
## Fixed
- Warning error Panel class

## [0.6.5] - 2019-02-26
### Fixed
- Error caused by items inside collection (bl 2.80)
- Non Mesh types where added when "selection only" was off

## [0.6.4] - 2019-01-12
### Changed
- Popup menu doesnt have 2 buttons at the bottom, makes it more clear what export is
- Label was replace due to new WM menu
- Export button has more logical label

### Fixed
- Apply modifier for bl 2.80

### Added
- Undo for export operation in case of error or malfunction

## [0.6.3] - 2019-01-12
### Fixed
- Issue with swapped keymap code

### Added
- Missing "skip localview" in popup menu
- Support for bl 2.80, see bl2.80_deb branch

## [0.6.2] - 2018-09-22
### Changed
- Added "skip localview check", can give errors so skip is added

## [0.6.1] - 2018-09-22
### Fixed
- Set config read/writing, errors occurred reading and writing file
- Keymap name errors

## [0.6] - 2017-12-16
### Fixed
- Set config file, errors occurred with custom path.
- WM call menu, now resizes when automation is checked.

## [0.5] - 2017-12-15
### Added
- OSX support for load options
- Extra load options (Weld UVs, Clean, Detach Flipped UVs)
- Checker for export from local view (is not supported)
- Automation, automatic packing and automatic save and return
- Hotkeys for popup menu (for clean workflow)
- Hotkeys to add-on panel for quick acces
- Quick Export shortcut (quick exports according to last settings)
- Add-on preferences saving options. On restart all settings will be loaded
- Custom export folder. Useful for when errors occur and file needs to be saved, quick access to files.

## [0.4] - 2017-12-07
### Added
- Create backup when ‘Apply Modifier’ is added.
- Option to export all visible objects, hidden and layers OFF won’t be exported.

## [0.3] - 2017-12-05
### Added
- Apply modifier option

## [0.2]
### Added
- Functionality with better selection of objects
- Selection only option
- Checker for selection only
- OSX support

## [0.1]
### Added
- Initial start plugin by Titus

## Notes
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[v0.7.5]:https://github.com/schroef/uvlayout_bridge/releases/tag/v0.7.5
[v0.7.41]:https://github.com/schroef/uvlayout_bridge/releases/tag/v0.7.41
[v0.7.4]:https://github.com/schroef/uvlayout_bridge/releases/tag/v0.7.4
[v0.7.3]:https://github.com/schroef/uvlayout_bridge/releases/tag/v0.7.3
[v0.7.2]:https://github.com/schroef/uvlayout_bridge/releases/tag/v0.7.2
[v0.7.1]:https://github.com/schroef/uvlayout_bridge/releases/tag/v0.7.1
[v0.6.5]:https://github.com/schroef/uvlayout_bridge/releases/tag/v0.6.5_2.80
[0.6.4]:https://github.com/schroef/uvlayout_bridge/releases/tag/v0.6.4
[0.6.3]:https://github.com/schroef/uvlayout_bridge/releases/tag/v0.6.3
[0.6.2]:https://github.com/schroef/uvlayout_bridge/releases/tag/v0.6.2
[0.6.1]:https://github.com/schroef/uvlayout_bridge/releases/tag/v0.6.1
[0.6]:https://github.com/schroef/uvlayout_bridge/releases/tag/v0.6
