import json, requests, sys, bpy, mathutils

SERVER_URL = "https://api.slin.dev/grab/v1/"

def get_user_cosmetics(user_name):
    user_url = f"{SERVER_URL}list?type=user_name&search_term={user_name}"
    user_list = requests.get(user_url).json()
    if len(user_list) == 0:
        return None
    user_color_primary = None
    user_color_secondary = None
    user_items = None

    for user in user_list:
        if "active_customizations" not in user:
            user["active_customizations"] = {
                "items": {}
            }
        if "items" not in user["active_customizations"]:
            user["active_customizations"]["items"] = {}

    user_color_primary = user_list[0]["active_customizations"]["player_color_primary"]["color"]
    user_color_secondary = user_list[0]["active_customizations"]["player_color_secondary"]["color"]
    user_items = user_list[0]["active_customizations"]["items"]

    for user in user_list:
        if user["user_name"] == user_name:
            user_color_primary = user["active_customizations"]["player_color_primary"]["color"]
            user_color_secondary = user["active_customizations"]["player_color_secondary"]["color"]
            user_items = user["active_customizations"]["items"]
            break
    
    return [user_color_primary, user_color_secondary, user_items]
    
def get_shop():
    shop_url = f"{SERVER_URL}get_shop_items?version=1"
    shop = requests.get(shop_url).json()
    return shop

def generate(userName):
    shop = get_shop()
    cosmetics = get_user_cosmetics(userName)

    primary = cosmetics[0]
    secondary = cosmetics[1]
    items = cosmetics[2]

    glasses = None
    hat = None
    head = None
    neck = None

    if "head/glasses" in items:
        glasses = items["head/glasses"]
    if "head/hat" in items:
        hat = items["head/hat"]
    if "head" in items:
        head = items["head"]
    if "body/neck" in items:
        neck = items["body/neck"]

    if glasses:
        glasses = {
            "file": shop[glasses]["file"]+".obj",
            "materials": shop[glasses]["materials_v2"]
        }
    if hat:
        hat = {
            "file": shop[hat]["file"]+".obj",
            "materials": shop[hat]["materials_v2"]
        }
    if head:
        head = {
            "file": shop[head]["file"]+".obj",
            "materials": shop[head]["materials_v2"]
        }
    else:
        head = {
            "file": "cosmetics/head/head/head.obj",
            "materials": ["default_primary_color", "default_secondary_color", "default_secondary_color_visor"]
        }
    if neck:
        neck = {
            "file": shop[neck]["file"]+".obj",
            "materials": shop[neck]["materials_v2"]
        }
    
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    bpy.ops.import_scene.obj(filepath="cosmetics/body/body.obj")
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[-1]
    bpy.ops.object.join()
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    # move down 1
    bpy.context.object.location[2] -= 0.3
    for i, material in enumerate(["default_primary_color", "default_secondary_color"]):
        if material != "default":
                if ("type" in material and material["type"] == "default_primary_color") or material == "default_primary_color" or material == "default_neon" or ("type" in material and material["type"] == "default_neon"):
                    bpy.context.active_object.data.materials[i].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (primary[0], primary[1], primary[2], 1)
                    bpy.context.active_object.data.materials[i].diffuse_color = (primary[0], primary[1], primary[2], 1)
                if ("type" in material and material["type"] == "default_secondary_color") or material == "default_secondary_color":
                    bpy.context.active_object.data.materials[i].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (secondary[0], secondary[1], secondary[2], 1)
                    bpy.context.active_object.data.materials[i].diffuse_color = (secondary[0], secondary[1], secondary[2], 1)
                if "type" in material and material["type"] == "default_color" and "diffuseColor" in material:
                    bpy.context.active_object.data.materials[i].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (material["diffuseColor"][0], material["diffuseColor"][1], material["diffuseColor"][2], 1)
                    bpy.context.active_object.data.materials[i].diffuse_color = (material["diffuseColor"][0], material["diffuseColor"][1], material["diffuseColor"][2], 1)
                if ("type" in material and material["type"] == "default_secondary_color_visor") or material == "default_secondary_color_visor":
                    bpy.context.active_object.data.materials[i].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (primary[0], primary[1], primary[2], 1)
                    bpy.context.active_object.data.materials[i].diffuse_color = (primary[0], primary[1], primary[2], 1)
    bpy.ops.object.select_all(action='DESELECT')

    if glasses:
        bpy.ops.import_scene.obj(filepath=glasses["file"])
        bpy.context.view_layer.objects.active = bpy.context.selected_objects[-1]
        bpy.ops.object.join()
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        for i, material in enumerate(glasses["materials"]):
            if material != "default":
                if ("type" in material and material["type"] == "default_primary_color") or material == "default_primary_color" or material == "default_neon" or ("type" in material and material["type"] == "default_neon"):
                    bpy.context.active_object.data.materials[i].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (primary[0], primary[1], primary[2], 1)
                    bpy.context.active_object.data.materials[i].diffuse_color = (primary[0], primary[1], primary[2], 1)
                if ("type" in material and material["type"] == "default_secondary_color") or material == "default_secondary_color":
                    bpy.context.active_object.data.materials[i].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (secondary[0], secondary[1], secondary[2], 1)
                    bpy.context.active_object.data.materials[i].diffuse_color = (secondary[0], secondary[1], secondary[2], 1)
                if "type" in material and material["type"] == "default_color" and "diffuseColor" in material:
                    bpy.context.active_object.data.materials[i].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (material["diffuseColor"][0], material["diffuseColor"][1], material["diffuseColor"][2], 1)
                    bpy.context.active_object.data.materials[i].diffuse_color = (material["diffuseColor"][0], material["diffuseColor"][1], material["diffuseColor"][2], 1)
                if ("type" in material and material["type"] == "default_secondary_color_visor") or material == "default_secondary_color_visor":
                    bpy.context.active_object.data.materials[i].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (primary[0], primary[1], primary[2], 1)
                    bpy.context.active_object.data.materials[i].diffuse_color = (primary[0], primary[1], primary[2], 1)
    bpy.ops.object.select_all(action='DESELECT')

    if hat:
        bpy.ops.import_scene.obj(filepath=hat["file"])
        bpy.context.view_layer.objects.active = bpy.context.selected_objects[-1]
        bpy.ops.object.join()
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        for i, material in enumerate(hat["materials"]):
            if material != "default":
                if ("type" in material and material["type"] == "default_primary_color") or material == "default_primary_color" or material == "default_neon" or ("type" in material and material["type"] == "default_neon"):
                    bpy.context.active_object.data.materials[i].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (primary[0], primary[1], primary[2], 1)
                    bpy.context.active_object.data.materials[i].diffuse_color = (primary[0], primary[1], primary[2], 1)
                if ("type" in material and material["type"] == "default_secondary_color") or material == "default_secondary_color":
                    bpy.context.active_object.data.materials[i].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (secondary[0], secondary[1], secondary[2], 1)
                    bpy.context.active_object.data.materials[i].diffuse_color = (secondary[0], secondary[1], secondary[2], 1)
                if "type" in material and material["type"] == "default_color" and "diffuseColor" in material:
                    bpy.context.active_object.data.materials[i].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (material["diffuseColor"][0], material["diffuseColor"][1], material["diffuseColor"][2], 1)
                    bpy.context.active_object.data.materials[i].diffuse_color = (material["diffuseColor"][0], material["diffuseColor"][1], material["diffuseColor"][2], 1)
                if ("type" in material and material["type"] == "default_secondary_color_visor") or material == "default_secondary_color_visor":
                    bpy.context.active_object.data.materials[i].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (primary[0], primary[1], primary[2], 1)
                    bpy.context.active_object.data.materials[i].diffuse_color = (primary[0], primary[1], primary[2], 1)
    bpy.ops.object.select_all(action='DESELECT')

    if head:
        bpy.ops.import_scene.obj(filepath=head["file"])
        bpy.context.view_layer.objects.active = bpy.context.selected_objects[-1]
        bpy.ops.object.join()
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        for i, material in enumerate(head["materials"]):
            if material != "default":
                if ("type" in material and material["type"] == "default_primary_color") or material == "default_primary_color" or material == "default_neon" or ("type" in material and material["type"] == "default_neon"):
                    bpy.context.active_object.data.materials[i].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (primary[0], primary[1], primary[2], 1)
                    bpy.context.active_object.data.materials[i].diffuse_color = (primary[0], primary[1], primary[2], 1)
                if ("type" in material and material["type"] == "default_secondary_color") or material == "default_secondary_color":
                    bpy.context.active_object.data.materials[i].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (secondary[0], secondary[1], secondary[2], 1)
                    bpy.context.active_object.data.materials[i].diffuse_color = (secondary[0], secondary[1], secondary[2], 1)
                if "type" in material and material["type"] == "default_color" and "diffuseColor" in material:
                    bpy.context.active_object.data.materials[i].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (material["diffuseColor"][0], material["diffuseColor"][1], material["diffuseColor"][2], 1)
                    bpy.context.active_object.data.materials[i].diffuse_color = (material["diffuseColor"][0], material["diffuseColor"][1], material["diffuseColor"][2], 1)
                if ("type" in material and material["type"] == "default_secondary_color_visor") or material == "default_secondary_color_visor":
                    bpy.context.active_object.data.materials[i].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (primary[0], primary[1], primary[2], 1)
                    bpy.context.active_object.data.materials[i].diffuse_color = (primary[0], primary[1], primary[2], 1)
    bpy.ops.object.select_all(action='DESELECT')

    # if neck:
    #     bpy.ops.import_scene.obj(filepath=neck["file"])
    #     bpy.context.view_layer.objects.active = bpy.context.selected_objects[-1]
    #     bpy.ops.object.join()
    #     bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    #     for i, material in enumerate(neck["materials"]):
    #         if material != "default":
    #             if ("type" in material and material["type"] == "default_primary_color") or material == "default_primary_color" or material == "default_neon" or ("type" in material and material["type"] == "default_neon"):
    #                 bpy.context.active_object.data.materials[i].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (primary[0], primary[1], primary[2], 1)
    #                 bpy.context.active_object.data.materials[i].diffuse_color = (primary[0], primary[1], primary[2], 1)
    #             if ("type" in material and material["type"] == "default_secondary_color") or material == "default_secondary_color":
    #                 bpy.context.active_object.data.materials[i].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (secondary[0], secondary[1], secondary[2], 1)
    #                 bpy.context.active_object.data.materials[i].diffuse_color = (secondary[0], secondary[1], secondary[2], 1)
    #             if "type" in material and material["type"] == "default_color" and "diffuseColor" in material:
    #                 bpy.context.active_object.data.materials[i].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (material["diffuseColor"][0], material["diffuseColor"][1], material["diffuseColor"][2], 1)
    #                 bpy.context.active_object.data.materials[i].diffuse_color = (material["diffuseColor"][0], material["diffuseColor"][1], material["diffuseColor"][2], 1)
    #             if "type" in material and material["type"] == "default_secondary_color_visor":
    #                 bpy.context.active_object.data.materials[i].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (primary[0], primary[1], primary[2], 1)
    #                 bpy.context.active_object.data.materials[i].diffuse_color = (primary[0], primary[1], primary[2], 1)
    # bpy.ops.object.select_all(action='DESELECT')

    # bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 2, 0), rotation=(1.570796, 0, 3.14159))
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0.62, 1.87, 0.19), rotation=(1.403244, 0, 2.816959))
    bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(1, 3, 0), rotation=(1.570796, 0, 3.14159))
    bpy.context.scene.camera = bpy.data.objects["Camera"]
    bpy.context.scene.render.resolution_x = 512
    bpy.context.scene.render.resolution_y = 512
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    bpy.context.scene.render.film_transparent = True
    bpy.ops.render.render(write_still=True)

    bpy.data.images['Render Result'].save_render(f'img/{userName}.png')
    # bpy.ops.wm.save_as_mainfile(filepath=f"{userName}.blend")

for name in [
    "Nash_Human",
    "fruitbythefist",
    "tltt",
    "nixmars",
    "envi0us",
    "iceyboxes",
    "the.nothing",
    "vrvinny",
    "yoshibigbum"
]:
    print(name)
    try:
        generate(name)
    except Exception:
        print("error")
        pass