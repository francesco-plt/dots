#!/usr/bin/env fish
# convert all .mp4 files in the current directory to .mov

# Iterate through all .mp4 files in the current directory
for file in (ls *.mp4)
    # Get the target filename by replacing .mp4 with .mov
    set target (echo $file | sed 's/\.mp4$/.mov/')

    # Check if the target file already exists
    if not test -f $target
        # If it doesn't exist, convert the .mp4 file to .mov
        ffmpeg -i $file -c:v h264 -c:a aac -strict -2 $target
        # and delete source file after conversion
        rm $file
    end
end

