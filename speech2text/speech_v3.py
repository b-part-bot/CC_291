import subprocess
subprocess.call('rm temp.wav',shell=True)
#converting mp3 to wav
subprocess.call('ffmpeg -i {} -acodec pcm_s16le -ar 16000 -ac 1 temp.wav'.format('dialog1.mp3'),shell=True)
#removing previous present files
subprocess.call('rm parts/*', shell=True)
#segmenting our .wav in parts of 5 seconds for processing 
subprocess.call('ffmpeg -i temp.wav -f segment -segment_time 5 -c copy parts/out%09d.wav',shell=True)
