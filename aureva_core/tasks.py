# Core Aureva tasks in Celery. These processes take a long time and can now be run without disrupting the server.
from celery import shared_task
import shlex
import subprocess

@shared_task
def generate_waveform(file):
    # Takes an audio file path as input and returns raw bytes of a transparent PNG file containing
    # a waveform graph of the audio file, using ffmpeg and then gnuplot.
    # This is for user pages.

    # Takes an audio file and outputs raw binary data, with two bytes for each sample.
    # Sampling rate is lowered to 8000 Hz to speed things up.
    text = 'ffmpeg -i {0} -ac 1 -filter:a aresample=8000 -map 0:a -c:a pcm_s16le -f data -'.format(file)
    args = shlex.split(text)
    ffmpeg_proc = subprocess.Popen(args, stdout=subprocess.PIPE)

    # Takes the raw output from the ffmpeg call and generates a graph of sorts of the waveform.
    # Parameters are in the file util/waveform.gnuplot and may be edited as one wishes.
    gnuplot_proc = subprocess.Popen(('gnuplot', 'util/waveform.gnuplot'), stdin=ffmpeg_proc.stdout,
                                    stdout=subprocess.PIPE)
    ffmpeg_proc.stdout.close()

    # Raw bytes of the png image
    output = gnuplot_proc.communicate()[0]

    return output