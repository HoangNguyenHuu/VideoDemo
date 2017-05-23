import subprocess as sp
FFMPEG_BIN = "ffmpeg"
command = [ FFMPEG_BIN,
            '-i', 'anni001.mpg',
            '-vf', 'trim=start_frame=2:end_frame=30',
            '-an', 'hello.mp4']
pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)