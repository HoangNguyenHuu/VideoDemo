import subprocess as sp
FFMPEG_BIN = "ffmpeg"
x = 2
y = 300
origin = 'anni001.mpg'
ouput = "out.mp4"
command = [ FFMPEG_BIN,
            '-i', origin,
            '-vf', 'trim=start_frame='+ str(x) +':end_frame='+str(y),
            '-an',ouput]
pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
