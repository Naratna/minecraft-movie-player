
from . import controller, __version__
import argparse
import os

def wrap(function):
    def validate(value):
        try:
            return function(value)
        except ValueError as err:
            raise argparse.ArgumentTypeError(str(err))
    return validate

fold = wrap(controller.fold)
fil = wrap(controller.fil)
nfil = lambda val: val if val is None else fil(val)
palette = wrap(controller.palette)
vid = wrap(controller.vid)
nvid = lambda val: val if val is None else vid(val)
filename = wrap(controller.filename)
nfilename = lambda val: val if val is None else filename(val)
datapack = wrap(controller.datapack)
mint = lambda minimum, nullable=False: wrap(controller.mint(minimum, nullable))
mfloat = lambda minimum, nullable=False: wrap(controller.mfloat(minimum, nullable))

def _get_parsers():
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--version", dest="version", action="store_true", default=False, help="display the version number")

    parsers = parser.add_subparsers(help="commands", dest="command")


    video_parser = parsers.add_parser("video", help="convert video to structure files")
    video_parser.add_argument("path_to_video", type=vid, help="The path to the video file that will be converted to structure files")
    video_parser.add_argument("path_to_output_folder", type=fold, help="The path to the folder in which the frames will be written")
    video_parser.add_argument("-p", "--palette", default=os.path.join(os.path.dirname(__file__), "palette.txt"), type=palette, dest="path_to_palette",help="The path to the block palette file to be used when convertnig")
    video_parser.add_argument("-n", "--name-prefix", default="video_", type=filename, dest="name_prefix", help="Specifies the name that will be prefixed to every generated frame")
    video_parser.add_argument("-t", "--ticks-per-frame", default="2", type=mint(0), dest="ticks_per_frame",help="How many game ticks between every frame. Can be any integer from 1 to 20. Default is 2. 20 = 1 fps, 2 = 10 fps, 1 = 20 fps, etc...")
    video_parser.add_argument("-x", "--width", default=None, type=mint(0, True), dest="width", help="The width of the output frames, measured in blocks")
    video_parser.add_argument("-y", "--height", default=None, type=mint(0, True), dest="height", help="The height of the output frames, measured in blocks")
    video_parser.add_argument("-m", "--adjust-mode", default="fit", type=str, dest="adjust_mode", choices=["fit", "fill"], help="If 'fit' is selected, black bars will be added to make the image fit the specified with and height. If set to 'fill', the image will be cropped in order to fit the width and height specified. Only used if both with and height are specified")
    video_parser.add_argument("-u","--unoptimized", action="store_true", dest="unoptimized", help="By default, every frame contains only the blocks that differ from the previous frame in an attempt to save resources. Using this option will disable this feature")
    video_parser.add_argument("-s", "--subprocesses", default=None, type=mint(0, True), dest="subprocesses", help="The amount of subprocesses that should be used when generating the frames. Defaults to the amount of cores on your PC")

    resourcepak_parser = parsers.add_parser("resourcepack", help="Generate sound files and sounds.json")
    resourcepack_parsers = resourcepak_parser.add_subparsers(help="subcommands", dest="subcommand")

    resourcepack_audio_parser = resourcepack_parsers.add_parser("audio", help="Splits the audio track from a video or audio file into several vorbis encoded audio files so that it can be used by the player")
    resourcepack_audio_parser.add_argument("path_to_audio", type=fil, help="The path to the audio file that will be split and converted")
    resourcepack_audio_parser.add_argument("path_to_output_folder", type=fold, help="The path to the folder in which the audio files will be written")
    resourcepack_audio_parser.add_argument("-s", "--split-size", default="60", type=mfloat(0), dest="split_size", help="The duration in seconds of every generated audio file")
    resourcepack_audio_parser.add_argument("-p", "--name-prefix", default="audio_", type=filename, dest="name_prefix", help="Specifies the name that will be prefixed to every generated frame")
    
    resourcepack_json_parser = resourcepack_parsers.add_parser("json", help="Generates the sounds.json file required to create thr resourcepack")
    resourcepack_json_parser.add_argument("output_folder", type=fold, help="The path to the folder in which the sounds.json file will be written")
    resourcepack_json_parser.add_argument("amount_of_sound_files", type=mint(0), help="The amount of sound files that should be added to sonds.json")
    resourcepack_json_parser.add_argument("-p", "--name-prefix", type=filename, default="audio_", dest="name_prefix", help="The name that was prefixed to every sound file")
    resourcepack_json_parser.add_argument("-f","--subfolder-name", type=filename, default="player", dest="subfolder_name", help="The name of the resourcepack subfolder where the audio files should be moved to")
    resourcepack_json_parser.add_argument("-m", "--merge", action="store_true", default=False, dest="merge", help="If present, the contents of the generated sounds.json will be merged with those of any existent sounds.json file in the destination folder")

    functions_parser = parsers.add_parser("functions", help="generates movie player functions")
    functions_parsers = functions_parser.add_subparsers(help="subcommands", dest="subcommand")

    #(output_folder: str, datapack_name:str, filename_prefix:str, first_index: int, final_index: int, max_commands: int = 25, ticks_per_frame: int = 2)
    video_functions_parser = functions_parsers.add_parser("video", help="Generate the functions required for video playbak")
    video_functions_parser.add_argument("output_folder", type=fold, help="The path to the folder in which the video functions will be written")
    video_functions_parser.add_argument("amount_of_frames", type=mint(0), help="The amount of frames that were generated previously")
    video_functions_parser.add_argument("-d","--datapack-name", type=datapack, default="player", dest="datapack_name", help="The name you wish to give to your datapack, should remain consistent across all functions and be less than 13 alphabetic lowercase characters")
    video_functions_parser.add_argument("-p","--name-prefix", type=filename, default="video_", dest="name_prefix", help="the name prefix of the frames that should have been generated beforehand")
    video_functions_parser.add_argument("-m","--max-commands", type=mint(0), default=25, dest="max_commands", help="The maximum amount of commands per generated function file, too many commands in a single function may impact performance. The less commands per function file, the more files will be generated")
    video_functions_parser.add_argument("-t", "--ticks-per-frame", type=mint(0), default=2, dest="ticks_per_frame", help="How many game ticks between every frame. If the number is different that the one used to generate the frames, the video will be sped up or slowed down")

    #(output_folder: str, datapack_name: str, sound_name_prefix: str, sound_duration: float, first_index: int, final_index: int, max_commands: int = 25)
    audio_functions_parser = functions_parsers.add_parser("audio", help="Generate the functions required for audio playbak")
    audio_functions_parser.add_argument("output_folder", type=fold, help="The path to the folder in which the audio functions will be written")
    audio_functions_parser.add_argument("amount_of_sound_files", type=mint(0), help="The amount of previously generated sound files")
    audio_functions_parser.add_argument("-n","--datapack-name", type=datapack, default="player", dest="datapack_name", help="The name you wish to give to your datapack, should remain consistent across all functions and be less than 13 alphabetic lowercase characters")
    audio_functions_parser.add_argument("-p","--name-prefix", type=filename, default="player.audio_", dest="name_prefix", help="The name prefix of the audio files that should have been generated beforehand")
    audio_functions_parser.add_argument("-d","--sound-duration", type=mfloat(0), default=60, dest="sound_duration", help="The duration in seconds of the previously generated sound files")
    audio_functions_parser.add_argument("-m","--max-commands", type=mint(0), default=25, dest="max_commands", help="The maximum amount of commands per generated function file, too many commands in a single function may impact performance. The less commands per function file, the more files will be generated")

    #(output_folder: str, datapack_name: str, control_audio: bool = False)
    playback_control_functions_parser = functions_parsers.add_parser("playback-control", help="Generate the functions required for controlling the video and audio playback")
    playback_control_functions_parser.add_argument("output_folder", type=fold, help="The path to the folder in which the playback control functions will be written")
    playback_control_functions_parser.add_argument("-d","--datapack-name", type=filename, default="player", dest="datapack_name", help="The name you wish to give to your datapack, should remain consistent across all functions and be less than 13 alphabetic lowercase characters")
    playback_control_functions_parser.add_argument("-a","--control-audio", action="store_true", default=False, dest="control_audio", help="If present, the functions will be able to control the audio playback aswell, if the datapack uses no audio, enabling this option will break the playback control")

    
    maker_parser = parsers.add_parser("make", help="Puts together all the generated files, creating a datapack folder and resourcepack folder")
    maker_parser.add_argument("containing_folder", type=fold, help="The path to the folder containing all the generated files")
    maker_parser.add_argument("-f", "--audio-subfolder", type=nfilename, default=None, dest="subfolder_name", help="Specify in case the script has trouble detecting it automatically")
    maker_parser.add_argument("-d", "-datapack-name", type=nfilename, default=None, dest="datapack_name", help="Specify in case the script has trouble detecting it automatically")


    index_parser = parsers.add_parser("index", help="Helps generate a template for the index file")
    index_parser.add_argument("path_to_block_folder", type=fold, help="The path to the folder containing all the block textures that are to be used")
    index_parser.add_argument("destination_file", type=str, help="The path where the file that will be generated")
    index_parser.add_argument("-f", "--filename-is-id", action="store_true", default=False, dest="filename_is_id", help="Uses the filenames of the images as block IDs in the generated file")



    palette_parser = parsers.add_parser("palette", help="Generates a palette file based on the specified block textures")
    palette_parser.add_argument("path_to_block_folder", type=fold, help="The path to the folder containing all the block textures that are to be used")
    palette_parser.add_argument("destination_file", type=str, help="The path where the file that will be generated")
    palette_parser.add_argument("-i", "--index", type=nfil, default=None, dest="path_to_index", help="The path to the block index file. If not specified, all the blocks within the block folder will be used and their filenames will be taken as their IDs")



    all_parser = parsers.add_parser("all", help="Generates all the necessary files in one command")
    all_parser.add_argument("path_to_output_folder", type=fold, help="The path to the folder where all the generated files will be witten")
    all_parser.add_argument("-v", "--video", type=nvid, default=None, dest="path_to_video", help="The path to the video that will be converted")
    all_parser.add_argument("-d", "--datapack-name", type=datapack, default="player", dest="datapack_name", help="The name that will be assigned to the generated datapack")
    all_parser.add_argument("-p", "--palette", default=os.path.join(os.path.dirname(__file__), "palette.txt"), type=palette, dest="path_to_palette",help="The path to the block palette file to be used when convertnig")
    all_parser.add_argument("-t", "--ticks-per-frame", default="2", type=mint(0), dest="ticks_per_frame",help="How many game ticks between every frame. Can be any integer from 1 to 20. Default is 2. 20 = 1 fps, 2 = 10 fps, 1 = 20 fps, etc...")
    all_parser.add_argument("-x", "--width", default=None, type=mint(0, True), dest="width", help="The width of the output frames, measured in blocks")
    all_parser.add_argument("-y", "--height", default=None, type=mint(0, True), dest="height", help="The height of the output frames, measured in blocks")
    all_parser.add_argument("-m", "--adjust-mode", default="fit", type=str, dest="adjust_mode", choices=["fit", "fill"], help="If 'fit' is selected, black bars will be added to make the image fit the specified with and height. If set to 'fill', the image will be cropped in order to fit the width and height specified. Only used if both with and height are specified")
    

    return parser, resourcepak_parser, functions_parser, all_parser

def main():

    parser, resourcepak_parser, functions_parser, all_parser = _get_parsers()

    args = parser.parse_args()

    if args.version:
        print(f"minecraft-movie-player {__version__}")

    elif args.command is None:
        parser.print_usage()

    elif args.command == "video":
        #(path_to_video: str, path_to_output_folder: str, path_to_palette: str, name_prefix: str, ticks_per_frame: str, width: int, height: int, unoptimized: bool)
        controller.video(args.path_to_video, args.path_to_output_folder, args.path_to_palette, args.name_prefix, args.ticks_per_frame, args.width, args.height, args.adjust_mode, args.unoptimized, args.subprocesses)

    elif args.command == "resourcepack":
        if args.subcommand is None:
            resourcepak_parser.print_usage()
        elif args.subcommand == "audio":
            controller.resourcepack_audio(args.path_to_audio, args.path_to_output_folder, args.split_size, args.name_prefix)
        elif args.subcommand == "json":
            controller.resourcepack_json(args.output_folder, args.amount_of_sound_files, args.name_prefix, args.subfolder_name, args.merge)

    elif args.command == "functions":
        if args.subcommand is None:
            functions_parser.print_usage()
        elif args.subcommand == "video":
            controller.functions_video(args.output_folder, args.amount_of_frames, args.datapack_name, args.name_prefix, args.max_commands, args.ticks_per_frame)
        elif args.subcommand == "audio":
            controller.functions_audio(args.output_folder, args.amount_of_sound_files, args.datapack_name, args.name_prefix, args.sound_duration, args.max_commands)
        elif args.subcommand == "playback-control":
            controller.functions_playback_control(args.output_folder, args.datapack_name, args.control_audio)

    elif args.command == "make":
        controller.make(args.containing_folder, args.subfolder_name, args.datapack_name)

    elif args.command == "index":
        controller.index(args.path_to_block_folder, args.destination_file, args.filename_is_id)

    elif args.command == "palette":
        controller.get_palette(args.path_to_block_folder, args.destination_file, args.path_to_index)

    elif args.command == "all":
        from os.path import isfile, join
        if args.path_to_video is None and not isfile(join(args.path_to_output_folder, "progress.txt")):
            all_parser.error("No progress.txt file was found at destination folder, please specify a video using -v/--video")
        controller.generate_all(args.path_to_video, args.path_to_output_folder, args.datapack_name, args.path_to_palette, args.ticks_per_frame, args.width, args.height, args.adjust_mode)

if __name__ == "__main__":
    main()