An AI video upscaling & restoration experiment.

The purpose of this code is to learn how a simple neuro model,
running on a single consumer grade RTX 3080 card, can restore
HEVC-compressed and downscaled Overwatch videos
back to their original 1920x1080 clean picture;
also to experiment on the assumption that a narrow-trained model
can make it's job way better than a general-purpose upscaler.
Videos are processed frame-by-frame.

The "Iggy" script creates traning dataset from a bunch
of source-quality FHD videos. Requires ffmpeg installed
in the system to work.

The "Pop" script is the training and prediction code itself.
