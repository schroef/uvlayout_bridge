'''
##   Todo   ########
#
#   V Get arguments working on OSX
#   - Get localview export working (not supported)
#   - Fix custom path and preload, with old scene opened wrong paths are used.
#     It uses the path from file for export and path for import fro ini. Add extra update for path on EXport
#   - Try scene without getConfig this is not needed as enum already loads settings
#	- Added d2.80 support
#	- updated user_preferences to preferences
#   - Add warning when appPath is not set
#   - Auto save shows CANCELLED but does work
####################

####################
## v.0.6.3
## 29-12-18
## Changed
## - Added skip local view, some scene cause errors
##
## 12-01-19
## Fixed
## - Small UI change
## - Hotkey issue
##
## Added
## - Missing skip local to popup menu
##
## Changed
## - Popup menu doesnt have 2 buttons at the bottom, makes it more clear what export is
## - Label was replace due to new WM menu
## - Export button has more logical label

## v.0.6.4
## 12-01-19
## Changed
## - Popup menu doesnt have 2 buttons at the bottom, makes it more clear what export is
## - Label was replace due to new WM menu
## - Export button has more logical label
##
## Fixed
## - Apply modifier for bl 2.80
##
## Added
## - Undo for export operation in case of error or malfunction

## v.0.6.5
## 26-02-19
## Fixed
## - Error caused by items inside collection
## - Non Mesh types where added when "selection only" was off

## v.0.6.6
## 20-03-19
## Fixed
## - Warning error Panel class

## v.0.6.7
## 20-03-20
## Changed
## - custom properties saved to addon prefs instead of in scene
##   Mentioned by Brechts https://developer.blender.org/T74954#895043
##   https://docs.blender.org/api/current/bpy.types.AddonPreferences.html
##   Im Skipping this because i want this to be per scene
## - Changed string path to DIR_PATH

## v.0.6.8
## 2021-11-04
# Fixed
- Concate error in export operator > addon_prefs, "uvlb_winPath" caused error 
- OBJ importer > global_clight_size taken out in new OBJ importer
- bl293 'apply_as" has changed
- Check local bool was not working properly. Added warning text, it has issues now and doen not transfering work done in UVlayout
- Missing options for Windows multiple options were not working and added in export

# Changed
- Added split_property > new 280 layout method
- Panel uses now sub-panel introduced in 2.80

## v.0.6.9
## 2021-11-06
# Fixed
- Autosave & close kept running when automation was off

## v.0.7.0
## 2021-11-06
# Added
- Forced reimport > when commands fails
- Optimize options > auto drops geometry, flattens, optimizes, packs, saves and returns to Blender
- Function to send tmp, edit & obj files to UVlayout. This allows user to easily open them, the ui from UVlayout is very outdated and tedious to work with.

# Changed
- If not mods are in mesh gray out menu option
- If 1 UV channel in mesh hide UV layout sub panel
- Moved panel to Tool catergory > save vertical menu from being to crowed

## v.0.7.0
## 2021-11-10
# Added
- Export custom path now in export options panel > easier accesible

# Changed
- Better check if we cancel or send file back to Blender > returns cancel or done report in bottom

## v.0.7.1 - 2021-11-10

# Changed
- get path and files moved to its own function, same code was used 6 times

## v.0.7.2 - 2024-07-23

# Fixed
- Changed parameter for OBJ importer and exporter.

## [v0.7.3] - 2024-07-24

# Fixed
- Export error if app path is not set, Panel shows red error with set app path option

## [v0.7.4] - 2024-07-25
# Fixed
- Automation Optimize, didnt do anything code fixed
- Show warning when exporting and custom path doesnt exist or is wrong
- missing check for OSX app path

# Changed
- Code cleanup
- Panel design is using split_property ala 2.8 Design
- Dialog operator now uses duplicate of panel by using wm.call_panel > easier and no double code
- Automation is either pack or optimize, running both commands wasnt doing anything since optimize also packs uvs

## [v0.7.41] - 2024-07-25
# Fixed
- missing check for OSX app path set

## [v0.7.5] - 2024-07-25
# Added
- uv channel poreview when switch number. this switches uvmap index so we actually can see preview easier

####################
## TODO
- Seams need to be updated after new import > 0.6.8 still shows old seams
- Fix automate, keeps running when checked off	cmd file keeps being created when automate is checked off
- Add check for UVchannels, if there 1 then gray out menu or hide it
- Add check for modifier options, if no mod on model, gray out option
- Add function which adds manual update fo when the sending didnt go well > there is alway an out file still there
- Add options to load tmp and edit files which you can save from UVlayout, does work with blender. Send them to UVlayout
- Save custom file in dot file next to blend file, now ini file is still per app
- Add better check when UVlayout is canceled, currently it states that all is done
- Autopack sometimes closes without saving on OSX
- When switching UV Channel, make it switch in the panel so we see preview
####################
'''

bl_info = {
    "name": "Headus UVLayout Bridge",
    "description": "Headus UVLayout Bridge - A bridge between Blender and Headus UVlayout for quick UVs unwrapping",
    "location": "3D VIEW > Properties > Headus UVlayout Panel",
    "author": "Rombout Versluijs // Titus Lavrov",
    "version": (0, 7, 5),
    "blender": (2, 80, 0),
    "wiki_url": "https://github.com/schroef/uvlayout_bridge",
    "tracker_url": "https://github.com/schroef/uvlayout_bridge/issues",
    "category": "UV"
}

import bpy
import collections
import os
import rna_keymap_ui
#import sys
import os.path
import subprocess
import tempfile
import time
import configparser


from sys import platform
from configparser import SafeConfigParser
from bpy.props import StringProperty, EnumProperty, BoolProperty, IntProperty
from bpy.types import Operator, AddonPreferences, Panel
from bpy_extras.io_utils import (ImportHelper, ExportHelper)
from . config.registers import get_hotkey_entry_item

    #---Check OS---
#    bpy.types.Scene.osSys = EnumProperty(
#            items = (('0', "WIN", ''),('1', "OSX", '')),
#            name = "OS check",
#            description="Check what OS is used",
#            default = '0')
    #--SYS check Enummenus --#
scn = bpy.types.Scene
if platform == "darwin":
    scn.osSys = '1'
if platform == "win32":
    scn.osSys = '0'
print("OS used: %s" % platform)



# return addon preferences
def get_addon_prefs(context):
    return context.preferences.addons[__name__].preferences

def app_path_set(context):
    addon_prefs = get_addon_prefs(context)
    if platform == "win32":
        return addon_prefs.uvlb_winPath != 'Please set Application Path'
    if platform == "darwin":
        return addon_prefs.versionUVL != 'Please choose version'

def customPath_exists(context):
    scn = context.scene
    return os.path.exists(scn.uvlb_customPath)

# def object_color_type_items(self,context)

#     return colors

def toggle_texture_preview(self,context):
    context = bpy.context
    scn = context.scene
    VIEW3D_PT_shading = bpy.types.VIEW3D_PT_shading
    shading = VIEW3D_PT_shading.get_shading(context)
    if scn.uvlb_uvPreview ==  True:
        if shading.color_type != 'TEXTURE':
            scn.object_color_types = shading.color_type
            shading.color_type = 'TEXTURE'
    else:
        shading.color_type = scn.object_color_types
    #toggle actrive UVMAP index
    ob = context.active_object
    scn=context.scene
    ob.data.uv_layers.active_index = scn.uvlb_uv_channel-1

def update_uvchannel_index(self,context):
    '''channels uv channel index so we see preview in 3dv when switching'''
    # switch uv map index
    ob = context.active_object
    scn=context.scene
    ob.data.uv_layers.active_index = scn.uvlb_uv_channel-1

    # set overlay preview
    context.scene.uvlb_uvPreview = True
    toggle_texture_preview(context, context)

# WIP make it toggle both ways, so if we change index in UVMAPS panel also update int prop
# b3d example GGET/SET
# https://b3d.interplanety.org/en/dynamically-setting-the-max-and-min-values-%E2%80%8B%E2%80%8Bfor-a-custorm-property-in-the-blender-python-api/
def get_uvchannels(self):
    uv_channels = bpy.context.active_object.data.uv_layers
    # # print(self.get('uvlb_uv_channel'))
    # if self.get('uvlb_uv_channel',1) > len(uv_channels)-1:
    #     print("1")
    #     return self.get('uvlb_uv_channel')
    # elif uv_channels.active_index+1 < self.get('uvlb_uv_channel'):
    #     print("2")
    #     return uv_channels.active_index +1
    # elif self.get('uvlb_uv_channel',1) < uv_channels.active_index+1:
    #     print("3")
    #     return self.get('uvlb_uv_channel')
    # else:
    #     return 1
    return self.get('uvlb_uv_channel', 1)

def set_uvchannels(self, value):
    uv_channels = bpy.context.active_object.data.uv_layers
    if uv_channels:
        if value > len(uv_channels):
            value = len(uv_channels)
        if value < len(uv_channels):
            value = 1
    else:
        value = 1
    self['uvlb_uv_channel'] = value


# def get_uvchannels_index(self,context):
#     '''Get uv channels active_index'''
#     if context.scene and context.active_object:
#         ob = context.active_object
#         if ob.data.uv_layers != None:
#             return ob.data.uv_layers.active_index + 1


#-- LOAD / SET CONFIG FILE  --#
configFol = "config"
version = "Please choose version"

def setConfig(self, context):
    '''Save Custom Path in config file when property is updated
        :param context: context
    '''
    preferences = context.preferences
    addon_prefs = get_addon_prefs(context)

    version = getattr(addon_prefs, "versionUVL", "")
    customPath = getattr(context.scene, "uvlb_customPath", "")
    pathEnable = getattr(context.scene, "uvlb_pathEnable", False)
    winPath = getattr(addon_prefs, "uvlb_winPath", "")
    config = configparser.ConfigParser()
    configPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), configFol + "/config.ini")
    print("UVlayout-Bridge: %s // %s // %s" % (customPath, pathEnable, winPath))
    config.read(configPath)
    if not config.has_section("main"):
        config.add_section('main')
    config.set('main', 'version', str(version))
    config.set('main', 'customPath', str(customPath))
    config.set('main', 'pathEnable', str(pathEnable))
    config.set('main', 'winPath', str(winPath))
    with open(configPath, 'w') as configfile:
        config.write(configfile)


def getVersionUVL():
    '''get UVlayout version from configuration file
        :return: versionUVL
        :rtype: bool
    '''

    version = "Please choose version"
    config = SafeConfigParser()

    for path in bpy.utils.script_paths():
        ConfigFile = os.path.join(path,"addons","uvlayout_bridge/",configFol + "/config.ini")
        if os.path.exists(ConfigFile):
            config.read(ConfigFile)
            try:
                version = config.get('main', 'version')
            except:
                version = "Please choose version"
    return version

def getCustomPath():
    '''get Custom Path version from configuration file

        :return: customPath
        :rtype: string
    '''

    customPath = "Please set path"
    pathEnable = False
    winPath = "Please set Application Path"

    config = SafeConfigParser()
    for path in bpy.utils.script_paths():
        ConfigFile = os.path.join(path,"addons","uvlayout_bridge/",configFol + "/config.ini")
        if os.path.exists(ConfigFile):
            config.read(ConfigFile)
            try:
                customPath = config.get('main', 'customPath')
                pathEnable = config.getboolean('main', 'pathEnable')
                winPath = config.get('main', 'winPath')
            except:
                customPath = "Please set path"
                pathEnable = False
                winPath = "Please set Application Path"

    return (customPath, pathEnable, winPath)


def updateIcon(self, context):
    scn = bpy.types.Scene
    # print("### Icons Updated ###")
    # print(self.uvlb_mode)
    if (self.uvlb_mode == '0'):
        setattr(scn, "iconMode", 'EDITMODE_HLT')
    else:
        setattr(scn, "iconMode", 'MOD_SUBSURF')
    if (self.uvlb_uv_mode == '0'):
        setattr(scn, "iconUVMode", 'TEXTURE')
    else:
        setattr(scn, "iconUVMode", 'GROUP_UVS')


# Props
scn = bpy.types.Scene

#-- GET CUSTOM PATH / OSX & WIN --#
scn.uvlb_customPath = StringProperty(
    name="Custom Path",
    description = "Choose custom export  path instead of temp directory. Is saved per scene",
    subtype = 'DIR_PATH',
    default = getCustomPath()[0],
    update = setConfig)

scn.uvlb_pathEnable = BoolProperty(
    name="Custom Path",
    description = "Choose custom path instead of temp",
    default = getCustomPath()[1],
    update = setConfig)



#-- BRIDGE ADDON OPTIONS --#
#---UV Channel selector---
scn.uvlb_uv_channel = IntProperty(
    name = "Map",
    description = "Select a UV channel for editing in export. Shows UV channel when setting number for easy preview",
    default = 1,
    get=get_uvchannels, 
    set=set_uvchannels,
    # get=lambda self: get_uvchannels(self),
    # set=lambda self, value: set_uvchannels(self, value),
    # min = 1,
    # max = get_uvchannels,
    update = update_uvchannel_index)

scn.object_color_types = EnumProperty(
    items = (('MATERIAL', 'MATERIAL',''),
           ('OBJECT','OBJECT',''),
           ('VERTEX','VERTEX',''),
           ('SINGLE','SINGLE',''),
           ('RANDOM','RANDOM',''),
           ('TEXTURE','TEXTURE','')),
    name = "Color Type",
    description = "Overlayer object Color Type in 3dView",
    default = 'MATERIAL')

scn.uvlb_uvPreview = BoolProperty(
    name="UV Preview",
    description = "Preview UV channel in 3dView, enables texture preview.",
    default = False,
    update = toggle_texture_preview)

scn.spaceName = BoolProperty(
    name="Spaces in Name",
    default=False)

scn.selOnly = BoolProperty(
    name="Selection Only",
    description = "Export selected object(s) only. Otherwise all visible object are exported.",
    default=True)

scn.viewOnly = BoolProperty(
    name="Selection Only",
    default=False)

scn.appMod = BoolProperty(
    name="Apply Modifier",
    description="Applies subsurf modifer, also in Blender will this be applied. You can choose to make backup.",
    default=False)

scn.cloneOb = BoolProperty(
    name="Create Backup",
    description="Creates copy of the model before modifiers are applied.",
    default=False)

scn.useKeyMap = BoolProperty(
    name="Use short popup",
    description="Use Alt + Shit + U to open the popup window",
    default=True)

#--Icons Enummenus --#
scn.iconMode = EnumProperty(
    items = (('EDITMODE_HLT', "EDITMODE_HLT", ''),
           ('MOD_SUBSURF', "MOD_SUBSURF", '')),
    name = "Mode",
    description = "POLY or SUBD",
    default = 'EDITMODE_HLT')
scn.iconMode = EnumProperty(
    items = (('EDITMODE_HLT', "EDITMODE_HLT", ''),
           ('MOD_SUBSURF', "MOD_SUBSURF", '')),
    name = "Mode",
    description = "POLY or SUBD",
    default = 'EDITMODE_HLT')

scn.iconUVMode = EnumProperty(
    items = (('TEXTURE', "TEXTURE", ''),('GROUP_UVS', "GROUP_UVS", '')),
    name = "UVMode",
    description = "Edit or New",
    default = 'TEXTURE')

#-- UVlayout OPTIONS --#
scn.uvlb_mode = EnumProperty(
    items = (('0', "Poly", ''),
           ('1', "SUBD", '')),
    name = "Mode",
    description = "If the mesh being loaded is the control cage for a subdivision surface, then make sure that SUBD is selected. The subdivided surface will then be used in the flattening calculations, rather than the control cage itself, producing more accurate results. If the mesh isn't a subdivision surface, then select Poly. Mind that objects with low poly count can look different in UVlayout. The mesh isnt changed it only looks different in 3d view.",
    default = '0',
    update=updateIcon)

scn.uvlb_uv_mode = EnumProperty(
    items = (('0', "New", ''),('1', "Edit", '')),
    name = "UV Mode",
    description = "If your mesh already has UVs and you want to reflatten them to reduce distortion, select Edit. Otherwise, select New to delete any existing UVs and start with a clean slate.",
    default = '0',
    update=updateIcon)

scn.uvlb_uv_weld = BoolProperty(
    name="Weld UV's",
    description = "If the loaded mesh has seams (green edges) between adjacent polys, reload with this option ticked. It'll weld all co-incident UVs together, but could break the OBJ Update tool and point correspondences between morph targets.",
    default=False)

scn.uvlb_uv_clean = BoolProperty(
    name="Clean",
    description = "If the loaded mesh has non-manifold edges (i.e. an edge is shared by more than two faces) then ticking this option will fix the problem geometry as its loaded. The clean will also remove duplicate faces. A summary of the changes made will be displayed once the file has been loaded.",
    default=False)

scn.uvlb_uv_detach = BoolProperty(
    name="Detach Flipped UVs",
    description = "Tick this option if you want flipped polys in UV space to be detached into separate shells.",
    default=False)

scn.uvlb_uv_geom = BoolProperty(
    name="Weld Geom Vertexes",
    description = "If there are geometry seams (blue edges) between seemingly continuous surfaces, then reload with this ticked to weld those up. Currently this triangulates the mesh also, so its recommended you only do this if you really have to.",
    default=False)

scn.uvlb_autoComm = BoolProperty(
    name="Automation:",
    description = "Use a couple commands to automate workflow. Can be a bit buggy!",
    default=False)

scn.uvlb_autoPack = BoolProperty(
    name="Packing",
    description = "Packs model or all models automatically.",
    default=False)

scn.uvlb_autoOptimize = BoolProperty(
    name="Optimize",
    description = "Drop all geometry, flatten, optimize, pack and save it ",
    default=False)

scn.uvlb_autoSave = BoolProperty(
    name="Auto Return",
    description = "Automatically sends the model back to Blender when all actions are done. Dont interupt this action, takes a small bit of time.",
    default=False)

scn.uvlb_help = BoolProperty(
    name="Help",
    description = "Hover over each button or menu for short detailed description of functions.",
    default=False)

scn.uvlb_autoCOMS = EnumProperty(
#    items = (('1', "Drop", ''),('2', "Flatten", ''),('3', "Optimize", ''),('4', "Drop-Flatten-Optimize", ''),('5', "Pack", ''),('6', "Drop-Flatten-Optimize-Pack", '')),
    items = (('0', "Choose", 'Choose'),('1', "Pack", 'Packs all UVs'),('2', "Optimize", 'Flatten, optimizes and packs')),
    name = "Commands",
    description = "Some of the options you can check under \"Pack\", will cause an error. Some commands are buggy and will crash the window. You need to redo the export from Blender and try again :(",
    default = '0')
    # default = '0')

# scn.checkLocal = BoolProperty(
#     name = "Skip Local",
#     default = False,
#     description="If issue with localview arrises skip it. NOT RECOMMENDED! You can loose work because, sometimes causes work done not to transfer over.")

scn.forced_reimport = BoolProperty(
    name = "Forced Reimport",
    default = False,
    description="Forces reimport of the out file from UVlayout. Sometimes import mismatches timing of UVlayout causing to not import proper output file.")


def is_local(context):
    #for ob in bpy.context.scene.objects:
    for ob in bpy.context.scene.collection.objects:
        #bpy.context.view_layer.objects.active = bpy.data.objects[ob.name]
        ## 2.80
        view = context.space_data
        is_local_view = (view.local_view is not None)
        # print("ob: %s - %s" % (ob.name, is_local_view))
        #if ob.layers_local_view[0]:
        ## 2.80
        if is_local_view:
            return True
        else:
            pass

def CheckSelection():
    objSelected = False
    if bpy.context.selected_objects != []:
        objSelected = True
    return objSelected

def get_path_files():
    preferences = bpy.context.preferences
    addon_prefs = get_addon_prefs(bpy.context)
    scn = bpy.context.scene


    #---Variables---
    if platform == "win32":
        UVLayoutPath = addon_prefs.uvlb_winPath
    else:
        UVLayoutPath = ''

    if scn.uvlb_pathEnable:
        path = scn.uvlb_customPath
    else:
        path = "" + tempfile.gettempdir()

#    path = "" + tempfile.gettempdir()
    # print("path %s" % path)
    path = '/'.join(path.split('\\'))

    if platform == "win32":
        path = path+'/'
    file_Name = path + "Blender2UVLayout_TMP.obj"
    file_outName = path + "Blender2UVLayout_TMP.out"
    file_setName = path +"Blender2UVLayout_TMP.set"
    file_cmdName = path + "Blender2UVLayout_TMP.cmd"
    file_commands = "subd"
    uvl_exit_str = "exit"

    pathFiles = scn, addon_prefs, UVLayoutPath, file_Name,file_outName, file_setName, file_cmdName, uvl_exit_str, uvlObjs, Objs
    return pathFiles

global expObjs, expMeshes, uvlObjs, Objs
expObjs = []
expMeshes = []
uvlObjs = []
Objs = []

def import_to_blender(file_Name,file_outName, file_setName, file_cmdName, uvl_exit_str, uvlObjs, Objs):
    # print("Import path: %s - File:%s" % (file_Name))
    # print("isosfile file_name: %s" % os.path.isfile(file_outName))
    # print("isosfile file_name == true: %s" % os.path.isfile(file_outName) == True)
    if os.path.isfile(file_outName) == True:
    #time.sleep(1)
        if bpy.app.version[0] < 3:
            bpy.ops.import_scene.obj(filepath = file_outName,
                                axis_forward = 'Y',
                                axis_up = 'Z',
                                filter_glob = "*.obj;*.mtl",
                                use_edges = False,
                                use_smooth_groups = False,
                                use_split_objects = True,
                                use_split_groups = True,
                                use_groups_as_vgroups = True,
                                use_image_search = False,
                                split_mode = 'ON',
                                )

        #bl 4.0
        if bpy.app.version[0] == 4 and bpy.app.version[1] >= 0:
            bpy.ops.wm.obj_import(filepath = file_outName,
                                forward_axis = 'Y',
                                up_axis = 'Z',
                                filter_glob = "*.obj;*.mtl",
                                use_split_objects = True,
                                use_split_groups = True,
                                import_vertex_groups  = True,
                                )

        # print("IMPORT OBJ")
        #---Close UVLAYOUT ---
        f = open(file_cmdName, "w+")
        f.write(''.join([uvl_exit_str]))
        f.close()

        # print("Transfer UVs and CleanUP")
        #---Transfer UVs and CleanUP---
        for ob in bpy.context.selected_objects:
            uvlObjs.append(ob)

        bpy.ops.object.select_all(action='DESELECT')

        # print("JOIN UVS")
        for ob in uvlObjs:
            try:
                # print(ob.name)
                #---Get source object name
                refName=ob.name.split('__UVL')
                #---Select source object---
                ## 2.80
                bpy.data.objects[refName[0]].select_set(state=True)
                #---Select UVL object
                ## 2.80
                bpy.context.view_layer.objects.active = bpy.data.objects[ob.name]
                #---Transfer UVs from UVL object to Source object
                bpy.ops.object.join_uvs()
                bpy.ops.object.select_all(action='DESELECT')
            except Exception as error:
                print("[DEBUG ]UVleayout Error: %s" % error)


        bpy.ops.object.select_all(action='DESELECT')

        # print("REMOVE IMPORTED MESH")
        for ob in uvlObjs:
            # print("remove ob UVL: %s" % ob.name)
            # print("remove ob data UVL: %s" %  ob.data.name)
            #bpy.data.meshes.remove(ob.data,True)
            ## 2.80
            bpy.data.meshes.remove(ob.data, do_unlink=True)

        bpy.ops.object.select_all(action='DESELECT')

        # print("SET MODES MESH OBJECT")
        for ob in Objs:
            #---Make new seams
            ## 2.80
            ob.select_set(state=True)
            ## 2.80
            bpy.context.view_layer.objects.active = ob
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            # Added clear seams bl293
            bpy.ops.mesh.mark_seam(clear=True)
            bpy.ops.uv.seams_from_islands()
            bpy.ops.object.editmode_toggle()

        return True
    else:
        return False

#-- Headus uvLayout Export/Import --#
def UVL_IO():
    scn, addon_prefs, UVLayoutPath, file_Name,file_outName, file_setName, file_cmdName, uvl_exit_str, uvlObjs, Objs = get_path_files()

    # reset forced reimport
    scn.forced_reimport = False

    expObjs = []
    expMeshes = []
    uvlObjs = []
    Objs = []

    #--Check visible objects
    #def layers_intersect(a, b, name_a="layers", name_b=None):
    #def layers_intersect(a, b, name_a="collections", name_b=None):
    #	return any(l0 and l1 for l0, l1 in zip(getattr(a, name_a), getattr(b, name_b or name_a)))
    ## 2.80
    def find_collection(context, obj):
        collections = obj.users_collection
        if len(collections) > 0:
            return collections[0]
        return context.scene.collection

    def gather_objects(scene):
        objexcl = set()

        def no_export(obj):
            return (not obj.hide_viewport) and (not obj.hide_select) and obj.visible_get() #and find_collection(bpy.context, obj)

        def is_selected(obj):
            #return obj.select
            return obj.select_get()

        def add_obj(obj):
            if obj.type == 'MESH':
                if obj not in objexcl:
                    scn.viewOnly = True
                    if scn.selOnly:
                        scn.viewOnly = False
                        if (is_selected(obj)):
                            objexcl.discard(obj)
                        print ("Objects sel only: %s" % obj)
                    else:
                        objexcl.add(obj)
                    print ("Objects include: %s" % obj)
                    return

        for obj in scene.objects:
        #for obj in scene.collection.objects:
            if obj.type == 'MESH':
                if (not no_export(obj)):
                    objexcl.discard(obj)
                    continue
                add_obj(obj)

        return objexcl

    objexcl = gather_objects(bpy.context.scene)
    for ob in objexcl:
        #--Select object only visible and set selection
        ## 2.80
        bpy.data.objects[ob.name].select_set(state=True)
        print ("Objects exclude: %s" % ob.name)
        scn.selOnly = True

    #--Get selected objects---
    for ob in bpy.context.selected_objects:
        if ob.type == 'MESH':
            #---If space in name replace by underscore
            params = [" "] #list of search parameters
            # [ o for o in bpy.context.scene.objects if o.active ]
            if any(x for x in params if x in ob.name): #search for params items in object name
                ob.name = ob.name.replace(" ","_")
                scn.spaceName = True

            if ob.type == 'MESH':
                ## 2.80
                if len(ob.data.uv_layers) < bpy.context.scene.uvlb_uv_channel:
                    for n in range(bpy.context.scene.uvlb_uv_channel):
                        ## 2.80
                        ob.data.uv_layers.new()
            ## 2.80
            ob.data.uv_layers.active_index = (bpy.context.scene.uvlb_uv_channel - 1)
            Objs.append(ob)

    #---Lists buildUP---
    #---Create and prepare objects for export---
    for ob in Objs:
        for mod in ob.modifiers:
            if scn.appMod:
                if scn.cloneOb:
                    newObj = ob.copy()
                    newObj.data = ob.data.copy()
                    newObj.name = ob.name + "_Backup"
                    newObj.animation_data_clear()
                    #scn.objects.link(newObj)
                    ## 2.80
                    scn.collection.objects.link(newObj)
                if mod.type == 'SUBSURF':
                    print ("Obj Name: %s - Mod Applied: %s" % (ob.name, mod.type))
                    # print(bpy.app.version[1])
                    if bpy.app.version[0] >= 3 or (bpy.app.version[0] >= 2 and bpy.app.version[1] >= 90):
                        bpy.ops.object.modifier_apply(modifier="Subsurf")
                    else:
                        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subdivision")

        newObj = ob.copy()
        newObj.data = ob.data.copy()
        newObj.animation_data_clear()
        newObj.name = ob.name + "__UVL"
        #bpy.context.scene.objects.link(newObj)
        ## 2.80
        bpy.context.scene.collection.objects.link(newObj)
        expObjs.append(newObj)
        expMeshes.append(newObj.data)

    #---Texture channels cleanup exept uvlb_uv_channel
    for ob in expMeshes:
        active_index = (bpy.context.scene.uvlb_uv_channel - 1)
        ## 2.80
        texName=ob.uv_layers[active_index].name
        ## 2.80
        uv_layers = ob.uv_layers
        ObjTexs=[]
        for t in uv_layers:
            ObjTexs.append(t.name)
        for u in ObjTexs:
            if u != texName:
                uv_layers.remove(uv_layers[u])

    #---Select objects for EXPORT
    bpy.ops.object.select_all(action='DESELECT')
    for ob in expObjs:
        ## 2.80
        bpy.data.objects[ob.name].select_set(state=True)


    # print(bpy.app.version)
    #---EXPORT---
    print("Export File:%s" % (file_Name))
    if bpy.app.version[0] < 3:
        bpy.ops.export_scene.obj(filepath=file_Name,
                                check_existing = True,
                                axis_forward = 'Y',
                                axis_up = 'Z',
                                filter_glob = "*.obj;*.mtl",
                                use_selection = scn.selOnly,
                                use_animation = False,
                                use_mesh_modifiers = scn.appMod,
#                                use_mesh_modifiers_render = False,
                                use_edges = False,
                                use_smooth_groups = False,
                                use_smooth_groups_bitflags = False,
                                use_normals = True,
                                use_uvs = True,
                                use_materials = True,
                                use_triangles = False,
                                use_nurbs = False,
                                use_vertex_groups = False,
                                use_blen_objects = False,
                                group_by_object = True,
                                group_by_material = False,
                                keep_vertex_order = True,
                                global_scale = 1,
                                path_mode = 'AUTO')
    
    # bl 4.0
    # https://docs.blender.org/api/current/bpy.ops.wm.html#bpy.ops.wm.obj_export
    if bpy.app.version[0] == 4 and bpy.app.version[1] >= 0:
        bpy.ops.wm.obj_export(filepath=file_Name,
                                check_existing = True,
                                forward_axis = 'Y',
                                up_axis = 'Z',
                                filter_glob = "*.obj;*.mtl",
                                export_animation = False,
                                apply_modifiers = scn.appMod,
                                export_selected_objects = scn.selOnly,
                                export_uv = True,
                                export_normals = True,
                                export_colors = True,
                                export_materials = True,
                                export_triangulated_mesh = False,
                                export_curves_as_nurbs = False,
                                export_object_groups = True,
                                export_material_groups = False,
                                export_vertex_groups = False,
                                export_smooth_groups = False,
                                smooth_group_bitflags = False,
                                global_scale = 1,
                                path_mode = 'AUTO')

    #--Reset Sel only
    if scn.viewOnly:
        scn.selOnly = False
    #---OBJs Clean up and deselect before import
    for ob in expMeshes:
        #bpy.data.meshes.remove(ob,True)
        ## 2.80
        bpy.data.meshes.remove(ob, do_unlink=True)

    bpy.ops.object.select_all(action='DESELECT')


#
    #-Set uvLayout mode
    if (bpy.context.scene.uvlb_mode == '0'):
        uvlb_mode = 'Poly,'
    if (bpy.context.scene.uvlb_mode == '1'):
        uvlb_mode = 'SUBD,'
    #-Set UVs mode
    if (bpy.context.scene.uvlb_uv_mode == '0'):
        uvlb_uv_mode = 'New,'
    if (bpy.context.scene.uvlb_uv_mode == '1'):
        uvlb_uv_mode = 'Edit,'
    #-Set Weld UVs
    if scn.uvlb_uv_weld:
        uvlb_uv_weld = 'Weld,'
    if not scn.uvlb_uv_weld:
        uvlb_uv_weld = ''
    #-Set Clean
    if scn.uvlb_uv_clean:
        uvlb_uv_clean = 'Clean,'
    if not scn.uvlb_uv_clean:
        uvlb_uv_clean = ''
    #-Set Detach UVs
    if scn.uvlb_uv_detach:
        uvlb_uv_deach = 'Detach flipped,'
    if not scn.uvlb_uv_detach:
        uvlb_uv_deach = ''
    #-Set Weld GEOM Vertexes
    if scn.uvlb_uv_geom:
        uvlb_uv_geom = 'Geom vertexes'
    if not scn.uvlb_uv_geom:
        uvlb_uv_geom = ''

    #-- OS CHECK--
    if platform == "darwin":
        versionUVL = getattr(addon_prefs, "versionUVL")
        dropSet = 0
        if os.path.isfile(file_setName) == False:
            if dropSet == 0:
#                loadAction = 'run UVLayout|Pack|Pack All' + '\n' +'run UVLayout|Plugin|Save'
#                loadAction = "drop \ n auto obj \n auto dxf "
                loadAction = uvlb_mode + uvlb_uv_mode + uvlb_uv_weld + uvlb_uv_clean + uvlb_uv_deach + uvlb_uv_geom

                f = open(file_setName, "w+")
    #            print("Commands Sent: %s - %s" % (uvlb_mode, uvlb_uv_mode))
                f.write(''.join([loadAction]))
                f.close()
                dropSet = 1
#                time.sleep(2)

        uvlayoutpath = []
        appOpen = '/Applications/headus-UVLayout-'+versionUVL+'.app/Contents/MacOS/uvlayout-maya'

        uvlayoutpath.append(appOpen)
        uvlayoutpath.append(file_Name)
        # print("UVLayoutPath %s" % uvlayoutpath)
        # print("Modes:" + uvlb_mode + uvlb_uv_mode + uvlb_uv_weld + uvlb_uv_clean + uvlb_uv_deach + uvlb_uv_geom)
        uvlayout_proc = subprocess.Popen(uvlayoutpath)


    elif platform == "win32":
        # print("UVLayoutPath %s" % UVLayoutPath)
        # print("Modes:" + uvlb_mode + uvlb_uv_mode + uvlb_uv_weld + uvlb_uv_clean + uvlb_uv_deach + uvlb_uv_geom)
        # uvlayout_proc = subprocess.Popen(args=[UVLayoutPath + 'uvlayout.exe', ' -debug -plugin,' + uvlb_mode + uvlb_uv_mode + uvlb_uv_weld + uvlb_uv_clean + uvlb_uv_deach + uvlb_uv_geom, file_Name])
        # https://stackoverflow.com/questions/60290732/subprocess-with-a-variable-that-contains-a-whitespace-path
        # cmd = f'"{tar_exe}" -tf "{image_file}"'
        # cmd = f'{UVLayoutPath}uvlayout.exe -log -plugin, {uvlb_mode}{uvlb_uv_mode}{uvlb_uv_weld}{uvlb_uv_clean}{uvlb_uv_deach}{uvlb_uv_geom}{file_Name}'
        # print(cmd)

        # versionUVL = getattr(addon_prefs, "versionUVL")
        # uvlayout_proc = subprocess.Popen(args=[cmd], shell=True)
        # uvlayoutpath =  'C:/program files \9x86\)/headus UVlayout v2'+versionUVL+'/uvlayout.exe'
        # uvlayout_proc = subprocess.Popen(args=[UVLayoutPath, '-plugin,' + uvlb_mode + uvlb_uv_mode + uvlb_uv_weld + uvlb_uv_clean + uvlb_uv_deach + uvlb_uv_geom, file_Name])

        uvlayout_proc = subprocess.Popen(args=[UVLayoutPath + 'uvlayout.exe', '-plugin,' + uvlb_mode + uvlb_uv_mode + uvlb_uv_weld + uvlb_uv_clean + uvlb_uv_deach + uvlb_uv_geom, file_Name])

    dropCom = 0

    result = False
    #---IMPORT---
    while not os.path.isfile(file_outName) and uvlayout_proc.poll() != 0:

        #-- SEND AUTOMATION COMMANDS ---
        if (os.path.isfile(file_cmdName) == False) and scn.uvlb_autoComm:
            if dropCom == 0:
                time.sleep(0)
                print("Commands Send")
                comm = ''
                # Not used fo now
                if scn.uvlb_autoCOMS == '1':
                    comm = 'run UVLayout|Pack|Pack All'
                if scn.uvlb_autoCOMS == '2':
                    comm = 'auto'
                # if scn.uvlb_autoCOMS == '1':
                #     comm = 'drop \n run UVLayout|Pack|Pack All'
                # if scn.uvlb_autoCOMS == '2':
                #     comm = 'drop \n auto obj \ run UVLayout|Pack|Pack All'
                # if scn.uvlb_autoCOMS == '3':
                #     comm = 'drop \n auto dxf \ run UVLayout|Pack|Pack All'
                # if scn.uvlb_autoCOMS == '4':
                #     comm = 'drop \n auto obj \n auto dxf '
                # if scn.uvlb_autoCOMS == '5':
                #     comm = 'run UVLayout|Pack|Pack All'
                # if scn.uvlb_autoCOMS == '6':
                #     comm = 'drop \n auto obj \n auto dxf \n run UVLayout|Pack|Pack All'

                # if scn.uvlb_autoPack:
                #     comm = 'run UVLayout|Pack|Pack All'
                
                # if scn.uvlb_autoOptimize:
                #     comm = 'auto'
                    # 2024-07-24d
                    # NOTE some settings in packing will cause error if set
                    # comm = 'run UVLayout|Auto|Pack\Pack All'
                    # comm = 'Auto obj'
                    # comm = 'Auto obj'
#                comm = 'drop \ n auto obj'
#                comm = "drop \ n auto obj \n auto eps \n auto dxf"
#                comm = "drop \ n auto dxf"

#                comm = 'run UVLayout|Pack|Pack All' + '\n' +'run UVLayout|Plugin|Save'
#                comm = "Poly"
#                comm = "drop \ n auto obj \n "
                f = open(file_cmdName, "w+")
    #            print("Commands Sent: %s - %s" % (uvlb_mode, uvlb_uv_mode))
                print("Command: %s" % comm)
                f.write(''.join([comm]))
                f.close()
                dropCom = 1

        #-- AUTO SAVE ACTION
        if (os.path.isfile(file_cmdName) == False) and scn.uvlb_autoSave and scn.uvlb_autoComm:
            comm = ''
            time.sleep(2)
#                if scn.uvlb_autoDRPS:
            if dropCom == 0 or dropCom == 1:
                comm = 'run UVLayout|Plugin|Save'
                print("Command: %s" % comm)
                f = open(file_cmdName, "w+")
                f.write(''.join([comm]))
                f.close()
                dropCom = 2
#            time.sleep(1)
        # close command file
#        time.sleep(3)

        #-- IMPORT OBJ BACK TO BLENDER --
        result = import_to_blender(file_Name,file_outName, file_setName, file_cmdName, uvl_exit_str, uvlObjs, Objs)

    while os.path.isfile(file_outName):
        time.sleep(1)
        # reset forced reimport
        # print(os.path.isfile(file_outName))
        # print(file_outName)
        if os.path.isfile(file_outName):
            # print(os.path.isfile(file_outName))
            # print(file_outName)
            # print("TMP output exists - Headus perhaps still open")
            scn.forced_reimport = True
        else:
            scn.forced_reimport = False
            # print(os.path.isfile(file_outName))
            # print(file_outName)
            # print("TMP output removed - Headus closed")
    else:
        scn.forced_reimport = False
    
    print("## ALL DONE ##")
    return result

class FILE_SN_choose_path(bpy.types.Operator, ImportHelper):
    """Choose path custom export location """
    bl_idname = "open.path_loc"
    bl_label = "Choose path export location"

    #    filename_ext = "*.scn.thea; *.mat.thea"
    filter_glob: StringProperty(
        default="DIR_PATH",
        #            default="*.png;*.jpeg;*.jpg;*.tiff")#,
        options={'HIDDEN'}, )

    def execute(self, context):
        scn = context.scene
        if scn != None:
            setattr(scn, "uvlb_customPath", self.filepath)
            return {'FINISHED'}


helper_tabs_items = [("EXECUTE", "Modifiers", "")]

#-- START EXPORT  --#
class UVLB_OT_Export(Operator):
    """Unwrap models using Headus UVlayout, this Bridge provides a easy workflow."""
    bl_idname = "uvlb.export"
    bl_name = "UVlayout Bridge"
    bl_label = "UVlayout Bridge"
    bl_options = {'REGISTER','UNDO'}

    tab: EnumProperty(name = "Tab", default = "EXECUTE", items = helper_tabs_items)

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = get_addon_prefs(context)

        scn = bpy.context.scene
        scn.spaceName = False

        ## Check if object is editmode
        if bpy.context.active_object != None:
            if bpy.context.active_object.mode == 'EDIT':
                bpy.ops.object.editmode_toggle()

        # Seems to be working now
        # if not scn.checkLocal:
        #     if is_local(context):
        #         self.report({'ERROR'}, "Localview Not Supported")
        #         return {'FINISHED'}
        #-- OSX check if application is chosen correct
        if platform == "darwin":
            versionUVL = getattr(addon_prefs, "versionUVL")
            if os.path.isfile('/Applications/headus-UVLayout-'+versionUVL+'.app/Contents/MacOS/uvlayout-plugin') == False:
                info = "Wrong UVlayout version in addon settings"
                self.report({'ERROR'}, info)
                return {'CANCELLED'}

        if scn.selOnly:
            if (CheckSelection() == False):
                self.report({'ERROR'}, "Nothing selected")
                return {'CANCELLED'}

        if scn.uvlb_pathEnable and not os.path.exists(scn.uvlb_customPath):
            self.report({'ERROR'}, "Custom Path can't be found or doesnt exist. Please check path")
            return {'CANCELLED'}

        #-- Run export eaction
        result = UVL_IO()

        #-- If files had space they are removed warning
        if scn.spaceName:
            self.report({'ERROR'}, "Some objects needed space removing")
            return {'FINISHED'}
        
        if result: self.report ({'INFO'}, 'UVLayout bridge - Import Done!')
        if not result: self.report ({'ERROR'}, 'UVLayout bridge - Cancelled')

        return {'FINISHED'}



def UVL_forced_reimport(context):
    scn, addon_prefs, UVLayoutPath, file_Name,file_outName, file_setName, file_cmdName, uvl_exit_str, uvlObjs, Objs = get_path_files()

    #-- IMPORT OBJ BACK TO BLENDER --
    import_to_blender(file_Name,file_outName, file_setName, file_cmdName, uvl_exit_str, uvlObjs, Objs)


#-- FORCE IMPOROT OUT FILE  --#
class UVLB_OT_Forced_Reimport(Operator):
    """Sometimes import mismatches timing of UVlayout causing to not import proper output file. Forces reimport of the out file from UVlayout. """
    bl_idname = "uvlb.forced_reimport"
    bl_name = "Forced Reimport"
    bl_label = "Forced Reimport"
    bl_options = {'REGISTER','UNDO'}

    @classmethod
    def poll(cls, context):
        scn, addon_prefs, UVLayoutPath, file_Name,file_outName, file_setName, file_cmdName, uvl_exit_str, uvlObjs, Objs = get_path_files()

        # file_outName = path + "Blender2UVLayout_TMP.out"
        return os.path.isfile(file_outName) or scn.forced_reimport

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = get_addon_prefs(context)

        scn = bpy.context.scene
        scn.spaceName = False

        #-- Run export eaction
        UVL_forced_reimport(context)

        self.report ({'INFO'}, 'Forced reimport succesful')
        return {'FINISHED'}


class UVLB_OT_Send_TempEdit_File(bpy.types.Operator, ExportHelper):
    """Function to send tmp, edit & obj files to UVlayout. This allows user to easily open them, the ui from UVlayout is very outdated and tedious to work with."""
    bl_idname = "uvlb.send_tmpedit"
    bl_label = "Send to UVL"

    filter_glob: StringProperty(
        # default="DIR_PATH",
        default="*.uvl;*.obj;*.ply;",
        options={'HIDDEN'}, )
    
    # filename_ext = "*.uvl;*.obj;*.ply;"
    filename_ext: EnumProperty(
        name="Example Enum",
        description="Choose between two items",
        items=(
            ('.uvl', "*.uvl", "UVlayout data file"),
            ('.obj', ".obj", "OBJ file"),
            ('.ply', ".ply", "PLY file"),
        ),
        default='.uvl',
    )
    filename = 'test.uvl'


    def execute(self, context):
        scn,addon_prefs, UVLayoutPath, file_Name,file_outName, file_setName, file_cmdName, uvl_exit_str, uvlObjs, Objs = get_path_files()
        # preferences = bpy.context.preferences
        # addon_prefs = get_addon_prefs(context)
        # scn = bpy.context.scene
        filename = self.filename
        # reset forced reimport
        scn.forced_reimport = False

        #-Set uvLayout mode
        if (bpy.context.scene.uvlb_mode == '0'):
            uvlb_mode = 'Poly,'
        if (bpy.context.scene.uvlb_mode == '1'):
            uvlb_mode = 'SUBD,'
        #-Set UVs mode
        if (bpy.context.scene.uvlb_uv_mode == '0'):
            uvlb_uv_mode = 'New,'
        if (bpy.context.scene.uvlb_uv_mode == '1'):
            uvlb_uv_mode = 'Edit,'
        #-Set Weld UVs
        if scn.uvlb_uv_weld:
            uvlb_uv_weld = 'Weld,'
        if not scn.uvlb_uv_weld:
            uvlb_uv_weld = ''
        #-Set Clean
        if scn.uvlb_uv_clean:
            uvlb_uv_clean = 'Clean,'
        if not scn.uvlb_uv_clean:
            uvlb_uv_clean = ''
        #-Set Detach UVs
        if scn.uvlb_uv_detach:
            uvlb_uv_deach = 'Detach flipped,'
        if not scn.uvlb_uv_detach:
            uvlb_uv_deach = ''
        #-Set Weld GEOM Vertexes
        if scn.uvlb_uv_geom:
            uvlb_uv_geom = 'Geom vertexes'
        if not scn.uvlb_uv_geom:
            uvlb_uv_geom = ''

        #-- OS CHECK--
        if platform == "darwin":
            versionUVL = getattr(addon_prefs, "versionUVL")
            dropSet = 0
            if os.path.isfile(file_setName) == False:
                if dropSet == 0:
                    loadAction = uvlb_mode + uvlb_uv_mode + uvlb_uv_weld + uvlb_uv_clean + uvlb_uv_deach + uvlb_uv_geom

                    f = open(file_setName, "w+")
                    f.write(''.join([loadAction]))
                    f.close()
                    dropSet = 1

            uvlayoutpath = []
            appOpen = '/Applications/headus-UVLayout-'+versionUVL+'.app/Contents/MacOS/uvlayout-maya'

            uvlayoutpath.append(appOpen)
            uvlayoutpath.append(self.filepath)
            # print("Modes:" + uvlb_mode + uvlb_uv_mode + uvlb_uv_weld + uvlb_uv_clean + uvlb_uv_deach + uvlb_uv_geom)
            subprocess.Popen(uvlayoutpath)
        
        if platform == "win32":
            subprocess.Popen(args=[UVLayoutPath + 'uvlayout.exe', '-plugin,' + uvlb_mode + uvlb_uv_mode + uvlb_uv_weld + uvlb_uv_clean + uvlb_uv_deach + uvlb_uv_geom, self.filepath])
        
        return {'FINISHED'}


#-- BRIDGE PANEL TOOL TAB __#
class UVLBRIDGE(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"


class VIEW3D_PT_panel_uvlbridge(UVLBRIDGE, Panel):
    """Creates a Unfold3d bridge Panel"""
    bl_label = "Headus UVlayout Bridge"
    bl_idname = "VIEW3D_PT_panel_uvlbridge"
    bl_context = "objectmode"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        # Only allow in Object mode and for a selected mesh.
        return (context.object is not None and context.object.type == "MESH")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        scn = bpy.context.scene
        obj = bpy.context.object
        addon_prefs = get_addon_prefs(context)

        if platform == "win32" and (addon_prefs.uvlb_winPath == 'Please set Application Path'):
            layout.alert = addon_prefs.uvlb_winPath == 'Please set Application Path'
            layout.label(text = "Application Path Headus UVLayout v2.")
            layout.prop(addon_prefs, "uvlb_winPath", text="")
        
        if platform == "darwin" and (addon_prefs.versionUVL == 'Please choose version'):
            layout.alert = addon_prefs.versionUVL == 'Please choose version'
            layout.label(text = "Application Path Headus UVLayout v2.")
            layout.prop(addon_prefs, "uvlb_winPath", text="")


#-- UVLAYOUT LOAD OPTIONS --#
class VIEW3D_PT_load_options(UVLBRIDGE, Panel):
    bl_label = "Load Options"
    bl_parent_id = "VIEW3D_PT_panel_uvlbridge"

    @classmethod
    def poll(cls, context):
        # print(app_path_set(context))
        return app_path_set(context)
    
    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        if scn.uvlb_pathEnable:
            layout.enabled = customPath_exists(context)
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        obj = bpy.context.object

        settingsBox = layout 
        column = settingsBox.column()

        column.row().prop(scn, "uvlb_mode", icon = getattr(scn,"iconMode",2))
        column.row().prop(scn, "uvlb_uv_mode", icon = getattr(scn,"iconUVMode",2))

        column.row().prop(scn, "uvlb_uv_weld")
        column.row().prop(scn, "uvlb_uv_detach")
        if (getattr(scn, "uvlb_uv_mode",) == '0'):
            column.row().prop(scn, "uvlb_uv_clean")
            # uvlbOptions.prop(scn, "uvlb_uv_geom") #Destroys linking import- triangulates the mesh



#-- QUICK COMMANDS --#
class VIEW3D_PT_automation(UVLBRIDGE, Panel):
    bl_label = " Automation"
    bl_parent_id = "VIEW3D_PT_panel_uvlbridge"

    @classmethod
    def poll(cls, context):
    	return app_path_set(context)

    def draw_header(self, context):
        layout = self.layout
        scn = bpy.context.scene
        layout.prop(scn, "uvlb_autoComm", text="")

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        if scn.uvlb_pathEnable:
            layout.enabled = customPath_exists(context)
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        obj = bpy.context.object

        settingsBox = layout
        column = settingsBox.column()

        if scn.uvlb_autoComm:
            column.row().prop(scn, "uvlb_autoCOMS")
            autosave = column.row()
            autosave.enabled = scn.uvlb_autoCOMS != '0'
            autosave.prop(scn, "uvlb_autoSave")


#-- UVMAPS --#
class VIEW3D_PT_uvchannel(UVLBRIDGE, Panel):
    bl_label = "UV Channel"
    bl_parent_id = "VIEW3D_PT_panel_uvlbridge"

    @classmethod
    def poll(cls, context):
        scn = bpy.context.scene
        return check_uv_channels(scn) and app_path_set(context)

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        if scn.uvlb_pathEnable:
            layout.enabled = customPath_exists(context)
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        obj = bpy.context.object

        # uvMapBox = layout
        # uvMapChannel = uvMapBox.split(factor=0.3)
        col = layout.column(align=True)
        uvMapChannel = col.row(align=True)
        if scn.uvlb_uvPreview:
            icon_uv = 'HIDE_OFF'
        else:
            icon_uv = 'HIDE_ON'
        uvMapChannel.prop(scn, "uvlb_uv_channel", icon="GROUP_UVS")
        uvMapChannel.prop(scn, "uvlb_uvPreview", text='', icon=icon_uv)

def check_for_mods(scn):
    #--Get selected objects---
    for ob in bpy.context.selected_objects:
        if ob.type == 'MESH':
            for mod in ob.modifiers:
                if mod.type == 'SUBSURF':
                    return True
    return False

def check_uv_channels(scn):
    #--Get selected objects---
    for ob in bpy.context.selected_objects:
        if ob.type == 'MESH':
            if len(ob.data.uv_layers) > 1:
                return True
    return False

#-- OBJ EXPORT options --#
class VIEW3D_PT_export_options(UVLBRIDGE, Panel):
    bl_label = "OBJ Eport Options"
    bl_parent_id = "VIEW3D_PT_panel_uvlbridge"	

    @classmethod
    def poll(cls, context):
    	return app_path_set(context)

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        if scn.uvlb_pathEnable:
            layout.enabled = customPath_exists(context)
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        obj = bpy.context.object

        column = layout.column()
        column.row().prop(scn,"selOnly")
        sub = column.row()
        sub.active = check_for_mods(scn) 
        sub.enabled = check_for_mods(scn) 
        sub.prop(scn,"appMod")
        if scn.appMod:
            column.row().prop(scn,"cloneOb")
            column.row().label(text="Subsurf will be applied, backup?", icon='INFO')

        column.row().prop(scn,"uvlb_pathEnable")
        if scn.uvlb_pathEnable:
            layout = self.layout
            layout.enabled = True
            column = layout.column()
            row = column.row()
            row.alert = not os.path.exists(scn.uvlb_customPath)
            row.prop(scn,"uvlb_customPath")


def uvl_panel_operator(self,context):
    if app_path_set(context):
        layout = self.layout
        #-- START EXPORT --
        layout.scale_y = 1.25
        
        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("uvlb.export", text = "Unwrap in UVlayout", icon_value=custom_icons["uvl"].icon_id)
        row.operator("uvlb.send_tmpedit", text = "", icon='FILE_TICK') # TEMP RECOVER_LAST LOOP_BACK
        
        scn,addon_prefs, UVLayoutPath, file_Name,file_outName, file_setName, file_cmdName, uvl_exit_str, uvlObjs, Objs = get_path_files()
        
        if os.path.exists(file_outName):
        # if os.path.isfile(file_outName):
            row = col.row(align=True)
            row.operator("uvlb.forced_reimport", icon='RECOVER_LAST') # RECOVER_LAST LOOP_BACK

#-- ADDON PREFS --#
class Blender2UVLayoutAddonPreferences(AddonPreferences):
    """ Preference Settings Addin Panel"""
    bl_idname = __name__

    uvlb_winPath : StringProperty(
        name="Path",
        description = "Choose custom path to Headus UVlayout application",
        default = getCustomPath()[2],
        subtype = 'DIR_PATH',
        update = setConfig)


    #-- ENUM MENUS --#
    versionUVL : EnumProperty(
        items = (("Please choose version", "Please choose version", ""),("demo", "UVlayout Demo", "UVlayout Demo"),("student", "UVlayout Student", ""),("hobbist", "UVlayout Hobbist", ""),("pro", "UVlayout Pro", "")),
        name = "UVlayout Version",
        description = "Set UVlayout Version, needed for startin correct application",
        default = getVersionUVL(),
        update = setConfig)


    def draw(self, context):
        layout = self.layout
        scene = context.scene

        if platform == "win32":
            box=layout.box()
            split = box.split()
            col = split.column()
            col.alert = (self.uvlb_winPath == 'Please set Application Path')
            col.label(text = "Application Path Headus UVLayout v2.")
            col.prop(self, "uvlb_winPath", text="")
            col.separator()
        if platform == "darwin":
            box=layout.box()
            split = box.split()
            col = split.column()
            col.alert = (self.versionUVL == 'Please choose version')
            col.label(text = "Headus UVlayout Version:")
            col.prop(self,"versionUVL", text="")
            col.label(text = "* No application path settings needed on OSX")
#            col.separator()

        col.separator()
        #-- CUSTOM EXPORT PATH --
        expBut = layout.box()

        column = expBut.column()
        column.row().label(text = "Custom export path:")
        if scene.uvlb_pathEnable:
            row = column.row()
            row.alert = not os.path.exists(scene.uvlb_customPath)
            row.prop(scene,"uvlb_customPath", text="")

        column = expBut.column()
        column.row().prop(scene,"uvlb_pathEnable", text="")

        box=layout.box()
        split = box.split()
        col = split.column()
        col.label(text = "Hotkeys:")
        col.label(text = "Do NOT remove hotkeys, disable them instead!")

        col.separator()
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user

        km = kc.keymaps['3D View']
        kmi = get_hotkey_entry_item(km, 'uvlb.export', 'EXECUTE', 'tab')
        if kmi:
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
            col.label(text = "Quick export using last settings")

        else:
            col.label(text = "Shift + V = quick export using last settings")
            col.label(text = "restore hotkeys from interface tab")

        col.separator()
        km = kc.keymaps['3D View']
        kmi = get_hotkey_entry_item(km, 'uvlayout.bridge', 'EXECUTE', 'tab')
        if kmi:
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
            col.label(text = "Opens the popup window")
        else:
            col.label(text = "Alt + Shift + V = opens the popup window")
            col.label(text = "restore hotkeys from interface tab")
        col.separator()



class OBJECT_OT_b2uvl_addon_prefs(Operator):
    bl_idname = "object.b2uvl_addon_prefs"
    bl_label = "Addon Preferences"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        if platform == "win32":
            preferences = context.preferences
            addon_prefs = get_addon_prefs(context)

            info = ("Path: %s" % (addon_prefs, "uvlb_winPath"))

        self.report({'INFO'}, info)
        print(info)

        return {'FINISHED'}

def icon_Load():
    # importing icons
    import bpy.utils.previews
    global custom_icons
    custom_icons = bpy.utils.previews.new()

    # path to the folder where the icon is
    # the path is calculated relative to this py file inside the addon folder
    my_icons_dir = os.path.join(os.path.dirname(__file__), configFol)

    # load a preview thumbnail of a file and store in the previews collection
    custom_icons.load("uvl", os.path.join(my_icons_dir, "uvl.png"), 'IMAGE')
    custom_icons.load("help", os.path.join(my_icons_dir, "help.png"), 'IMAGE')

# global variable to store icons in
custom_icons = None


addon_keymaps = []

#Classes for register and unregister
classes = (
    FILE_SN_choose_path,
    UVLB_OT_Export,
    UVLB_OT_Forced_Reimport,
    UVLB_OT_Send_TempEdit_File,
    VIEW3D_PT_panel_uvlbridge,
    VIEW3D_PT_load_options,
    VIEW3D_PT_automation,
    VIEW3D_PT_uvchannel,
    VIEW3D_PT_export_options,
    Blender2UVLayoutAddonPreferences,
    OBJECT_OT_b2uvl_addon_prefs,
    )


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # add operator to bottom panel > work around for sub panel usage
    bpy.types.VIEW3D_PT_panel_uvlbridge.append(uvl_panel_operator)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    km = kc.keymaps.new(name = "3D View", space_type = "VIEW_3D")

    # Removed dialog operator, this is cleaner and eaier. No duplciate code
    kmi = km.keymap_items.new('wm.call_panel', 'V', 'PRESS',alt = True,shift=True)
    kmi.properties.name = 'VIEW3D_PT_panel_uvlbridge'
    
    kmi = km.keymap_items.new("uvlb.export", "V", "PRESS", shift = True)
    kmi.properties.tab = "EXECUTE"

    addon_keymaps.append((km, kmi))
    icon_Load()




def unregister():
    global custom_icons
    bpy.utils.previews.remove(custom_icons)

    bpy.types.VIEW3D_PT_panel_uvlbridge.remove(uvl_panel_operator)

    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()

