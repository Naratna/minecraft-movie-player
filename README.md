
# minecraft-movie-player

A command line program that generates a datapack that plays videos in vanilla Minecraft

The goal of this program is to take a video file and convert its frames into structure block files so that it can be played inside a Minecraft world through the use of a datapack and a resourcepack

## Getting started

**Prerequisites**

 - [Python >= 3.8](https://www.python.org/downloads/) 
 - [ffmpeg](https://ffmpeg.org/download.html) or [libav](https://libav.org/download/)
 - Minecraft java edition 1.6 (May work on earlier versions but is untested)

Make sure both python and ffmpeg/libav are present in your system's PATH environment variable

**Installation**
the installation can be done through [pip](https://pypi.org/project/pip/)

    $ python -m pip install minecraft-movie-player

**Basic usage**
The program can be called from a command line with

    $ mc-movie

or, alternatively, with

    $ python -m minecraft_movie_player

The easiest way to generate the necessary files is through the sub command `all` provided by the cli, like so:
 
    $ mc-movie all OUTPUT_FOLDER -v VIDEO
   
OUTPUT_FOLDER should be replaced with the path to a (preferably empty) folder where all the generated files will be saved.
VIDEO should be replaced with the path to the video that is to be played inside Minecraft

Once the program begins, it can take from a few minutes to a few hours for it to finish, depending on the length of the video as well as the performance of your processor.

Throughout this process, hundreds (or even thousands) of files will be dumped inside the output folder, try not to mess with any of them and don't worry about the mess, by the end all that will be left in there is a single folder and a zip file.

If the process in interrupted, it can be resumed later simply by providing the path to the output folder that was being used, provided the files within it are still intact.

    $ mc-movie all SAME_OUTPUT_FOLDER

**Getting the video inside Minecraft**

Once the program is done, go inside the output folder, where you will find a folder named `player` and a zip file named `resources.zip`. Go into Minecraft, select the world of your choice, click the button `Edit` on the bottom left and then the button `Open world folder`. Copy `resources.zip` to this folder, then head inside the folder named `datapacks` and copy the folder `player` to it.

After all that is done, open your Minecraft world and pick the location for the screen's bottom left corner, stand there, open the chat (default key is `t`), then send

    /function player:setup_video

and

    /function player:setup_audio

Finally, when you wish to start the video, send

    /function player:restart
   
That's it! If everything went accordingly, your video should be playing inside vanilla Minecraft.
Additionally, the following commands should be available to pause/play the video:

    /funtcion player:pause
    /function player:play

## More advanced usage

**the `all` subcommand**
As explained above, this command easily generates all the required files without much hassle.

Required positional arguments:
- `path_to_output_folder`: The path to the folder where all the generated files will be dumped. Additionally, a `progress.txt` file will be created inside the folder, it helps the program pick up where it left off in case it is interrupted. If the file is present, all provided optional arguments will be ignored in favor of the values present inside `progress.txt`. If the file is not present, the argument `-v`/`--video` becomes obligatory.

Optional arguments:
- `-v` or `--video`: The path to the video that is to be used as a base for generating all the required files. The video's frames will be converted into structure block (nbt) files. The audio will be split into 60 seconds-long segments and saved as vorbis encoded .ogg files. If the video contains more than one audio track, the one marked as default within the file will be used. If the video has no sound, all of the steps pertaining to audio playback will be skipped.

The `all` subcommand described above is merely a shortcut for a set of more complicated commands that are used to generate all of the individual parts of the datapack and resource pack. These commands can be used if more advanced options are required or if only one of the many parts needs to be generated, instead of all of them.

## How it works

The most important part of the program is that which analyses an image pixel by pixel and finds which Minecraft block is the closest in color. In order to so, the program requires a list of of Minecraft blocks and their average RGB value, this list is known as a palette. The larger the palette, the better the image

**How to create a palette**

The script is able to analyze a folder containing Minecraft texture images (obtained by extracting .minecraft/versions/[version number]/[version number].jar with any tool such as WinRAR or 7Zip) in order to find their average colors and put them on a file, the palette. However, average color is not all the information the program needs, it also has to know which block IDs go with which colors, and in some cases some NBT data indicating the direction a block is facing.

This information is stored in a file formatted with tab separated values called the index, which tells the script the filenames of different Minecraft blocks, their block IDs and, optionally, the NBT data required to make the block face the right direction.

For example, the following is the file containing the texture for dirt:

![images/dirt.png](images/dirt.png)

The name of this image is dirt.png.

This block is simple enough, as its filename is the same as its block ID and looks the same on all sides. Its corresponding entry on the index would look something like this:

    dirt.png dirt

However, it is not so simple for other blocks. Consider the following image:

![oak_log_top.png](images/oak_log_top.png)

The name of this image is oak_log_top.png, however its block ID is simply oak_log. Moreover, this block is placed upright by default, meaning we need to add information about its orientation to be able to see the top when standing in front of it. More precisely, the script wants the information required to make its blocks face north.

So, what do we do? We go into Minecraft an place down an oak log facing north with the help of the debug menu (f3), like so:

![oak_1.png](images/oak_1.png)

Then, we point at the block and look at the right of the debug menu, there, we will find its block ID, as well as information regarding its orientation

![oak_2.png](images/oak_2.png)

The first highlighted line, minecraft:oak_log, is the block ID, the second, axis: z, is the information we need about the orientation, meaning the index would now look like this:

  

    dirt.png dirt
    
    oak_log_top.png oak_log {axis:z}

Keep in mind that two entries may share the same block ID, so long as they point at different images, for instance, the following entries are fine:

  

    dirt.png dirt
    
    oak_log_top.png oak_log {axis:z}
    
    oak_log.png oak_log {axis:y}

  

If we were to add, say, furnaces into the mix, the index would now look like this:

  

    dirt.png dirt
    
    oak_log_top.png oak_log {axis:z}
    
    oak_log.png oak_log {axis:y}
    
    furnace_front.png furnace {facing:north}
    
    furnace_side.png furnace {facing:east}
    
    furnace_back.png furnace {facing:south}

  

Once the index is filled to your own satisfaction, it can be fed into the script to generate the palette

This project comes with its own index and palette, however, they may be incomplete or outdated, so it is encouraged to make a pull request if you have indexed any new blocks.

It is recommended that you don't use any blocks that aren't full blocks, can't stand on their own, would cause light updates (transparent blocks or light emitting blocks), can not be seen at a distance, or would behave in destructive ways (water, lava, TNT)

Feel free to use these blocks at your own risk, but I will be declining any pull requests containing them.
