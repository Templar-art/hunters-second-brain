"""Get Down (Put em up) - Ryan James, flythrough reel cut on Hunter's cinematic flow:
intro 0-12 (chant), 'Get down' hit at 12.25, build 12-23, drop at 23.0, two bars of the drop,
then a half-beat overlap at 28.98 (just before the next vocal line) into the song's own ending at 181.56
(vocal gap, same groove phase: chroma 0.86 / onset 0.92) through its real stop at 189.45. 36.9 s."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reel_cut import main
SONG = "/Users/10xhunter/Downloads/ryan james - Get Down (Put em up) _THIS SONG DONATES TO MAKE SCHOOLS HEALTHIER_.mp3"
main(SONG, "output/getdown-reel/GetDown_reel.wav", [[0, 28.98], [181.56, 189.45]], [[0.37, 1.0]], tail_fade=0.3)
