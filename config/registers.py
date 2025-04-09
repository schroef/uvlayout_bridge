import bpy
import rna_keymap_ui


def get_hotkey_entry_item(km, kmi_name, kmi_value, properties):

    for i, km_item in enumerate(km.keymap_items):
        # print("iFem key: %s - %s - %s" % (kmi_name, kmi_value, properties))
    #    print("item key: %s - %s" % (km.keymap_items.keys()[i], kmi_name))
            # print("item key: %s - %s" % (km.keymap_items.keys()[i], km.keymap_items.keys()[i].name))
        if km.keymap_items.keys()[i] == kmi_name:
            # print("properties %s" % properties)
            # print("item key: %s - %s" % (km.keymap_items.keys()[i], km.keymap_items[i].name))
            if properties == kmi_value:
                # print("item key: %s - %s" % (km.keymap_items.keys()[i], km.keymap_items[i].properties))
                # if km.keymap_items[i].properties.name == kmi_value:
                return km_item
            if properties == 'name':
                # print("item key: %s - %s" % (km.keymap_items.keys()[i], km.keymap_items[i].properties))
                if km.keymap_items[i].properties.name == kmi_value:
                    return km_item
            elif properties == 'tab':
                if km.keymap_items[i].properties.tab == kmi_value:
                    return km_item

            elif properties == 'none':
                return km_item
    return None
