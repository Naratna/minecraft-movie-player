import os
import shutil
import json

def make(containing_folder: str, resourcepack_subfolder: str = None):
    
    mcfunction, nbt, ogg = _get_file_lists(containing_folder)

    if len(mcfunction):
        datapack_name = _get_datapack_name(containing_folder)
        _make_datapack_folder_structure(containing_folder, datapack_name)
        _create_datapack_files(containing_folder, datapack_name)
        _move_functions(containing_folder, datapack_name, mcfunction)
        _move_structures(containing_folder, datapack_name, nbt)
    if len(ogg):
        resourcepack_subfolder = _get_resourcepack_subfolder(containing_folder, ogg[0]) if resourcepack_subfolder is None else resourcepack_subfolder
        _make_resourcepack_folder_structure(containing_folder, resourcepack_subfolder)
        _create_resourcepack_files(containing_folder)
        _move_sounds(containing_folder, resourcepack_subfolder, ogg)
        

def _get_file_lists(containing_folder: str):
    files = [f for f in os.listdir(containing_folder) if os.path.isfile(os.path.join(containing_folder, f))]
    
    mcfunction, nbt, ogg = [], [], []
    for f in files:
        extension = os.path.splitext(f)[1][1:]

        if extension == "mcfunction":
            mcfunction.append(f)
        elif extension == "nbt":
            nbt.append(f)
        elif extension == "ogg":
            ogg.append(f)

    return mcfunction, nbt, ogg

def _get_datapack_name(containing_folder: str):
    path = os.path.join(containing_folder, "main_video.mcfunction")
    if not os.path.exists(path):
        return None
    main_video = open(path, "r")
    datapack_name = main_video.readline()[1:-1]
    main_video.close()
    return datapack_name

def _get_resourcepack_subfolder(containing_folder: str, sound_name: str):
    sound_name = "/" + os.path.splitext(sound_name)[0]
    path = os.path.join(containing_folder, "sounds.json")
    if not os.path.exists(path):
        return None
    sounds_file = open(path, "r")
    sounds_json = json.load(sounds_file)
    sounds_file.close()
    
    for sound in sounds_json.items():
        name = sound[1]["sounds"][0]["name"]
        if sound_name in name:
            return name[:-len(sound_name)]
    return None

def _make_datapack_folder_structure(containing_folder: str, datapack_name: str):
    join = os.path.join
    datapack_folder = join(containing_folder, datapack_name)
    if os.path.exists(datapack_folder):
        shutil.rmtree(datapack_folder)
    os.mkdir(datapack_folder)
    os.mkdir(join(datapack_folder, "data"))
    os.mkdir(join(datapack_folder, "data", "minecraft"))
    os.mkdir(join(datapack_folder, "data", "minecraft", "tags"))
    os.mkdir(join(datapack_folder, "data", "minecraft", "tags", "functions"))
    os.mkdir(join(datapack_folder, "data", datapack_name))
    os.mkdir(join(datapack_folder, "data", datapack_name, "functions"))
    os.mkdir(join(datapack_folder, "data", datapack_name, "structures"))

def _make_resourcepack_folder_structure(containing_folder: str, resourcepack_name:str):
    join = os.path.join
    resourcepack_folder = join(containing_folder, "resources")
    if os.path.exists(resourcepack_folder):
        shutil.rmtree(resourcepack_folder)
    os.mkdir(resourcepack_folder)
    os.mkdir(join(resourcepack_folder, "assets"))
    os.mkdir(join(resourcepack_folder, "assets", "minecraft"))
    os.mkdir(join(resourcepack_folder, "assets", "minecraft", "sounds"))
    os.mkdir(join(resourcepack_folder, "assets", "minecraft", "sounds", resourcepack_name))

def _create_datapack_files(containing_folder, datapack_name):
    join = os.path.join
    datapack_folder = join(containing_folder, datapack_name)
    pack_mcmeta = {
        "pack": {
            "pack_format": 6,
            "description": f"{datapack_name} generated using Minecraft Movie Player"
        }
    }
    pack_file = open(join(datapack_folder, "pack.mcmeta"), "w+")
    json.dump(pack_mcmeta,pack_file, indent=2)
    pack_file.close()

    tick_json = {
        "values":[
            f"{datapack_name}:main_video"
        ]
    }

    if os.path.exists(join(containing_folder, "main_audio.mcfunction")):
        tick_json["values"].append(f"{datapack_name}:main_audio")

    tick_file = open(join(datapack_folder, "data", "minecraft", "tags", "functions", "tick.json"), "w+")
    json.dump(tick_json, tick_file, indent=2)
    tick_file.close()

def _create_resourcepack_files(containing_folder):
    join = os.path.join
    resourcepack_folder = join(containing_folder, "resources")

    pack_mcmeta = {
        "pack": {
            "pack_format": 6,
            "description": "Generated using Minecraft Movie Player"
        }
    }
    pack_file = open(join(resourcepack_folder, "pack.mcmeta"), "w+")
    json.dump(pack_mcmeta,pack_file, indent=2)
    pack_file.close()

def _move_functions(containing_folder: str, datapack_name: str, mcfunction: list):
    for f in mcfunction:
        shutil.move(os.path.join(containing_folder, f), os.path.join(containing_folder, datapack_name, "data", datapack_name, "functions"))

def _move_structures(containing_folder: str, datapack_name: str, nbt: list):
    for f in nbt:
        shutil.move(os.path.join(containing_folder, f), os.path.join(containing_folder, datapack_name, "data", datapack_name, "structures"))

def _move_sounds(containing_folder: str, resourcepack_subfolder: str, ogg: list):
    for f in ogg:
        shutil.move(os.path.join(containing_folder, f), os.path.join(containing_folder, "resources", "assets", "minecraft", "sounds", resourcepack_subfolder))
    shutil.move(os.path.join(containing_folder, "sounds.json"), os.path.join(containing_folder, "resources", "assets", "minecraft"))

def main():
    import argparse

if __name__ == "__main__":
    main()