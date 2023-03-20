import mido
from mido import MidiFile, MidiTrack, Message
from music21 import converter
from pydub import AudioSegment
import fluidsynth

abc_star_spangled_banner = '''
X:126
T:The Star-Spangled Banner
Z:Jack Campin  *  May 2000  *  http://www.campin.me.uk/ * christian collins sound font * http://www.schristiancollins.com/generaluser.php
M:3/4
L:1/8
Q:110
K:D
  A>F | D2 F2 A2 | d4 f>e | d2 F2 ^G2 | A4 A2 | f3 e/ d2 | c4 Bc | d2 d2
 A2 | F2 D2 :| f>f | f2 g2 a2 | a4 g>f | e2 f2 g2 | g4 g2 | f3 e/ d2 | c
4 B>c | d2 F2 ^G2 | A4 A2 | d2 d2 dc | B2 B2 B2 | e2 gf ed | d2 c2
A>A | d3 e/ fg | a4 d>e | f3 g/ e2 | d6 ||
'''


def note_to_midi(note):
  note_map = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
  note_base = note[0]
  accidental = ''
  octave = note[-1]

  if len(note) == 3:
    accidental = note[1]

  midi_note = note_map[note_base]

  if accidental == '#':
    midi_note += 1
  elif accidental == 'b':
    midi_note -= 1

  midi_note += (int(octave) + 1) * 12
  return midi_note


# Parse the ABC notation
parsed_abc = converter.parse(abc_star_spangled_banner, format='abc')

# Extract notes and durations
notes_durations = [(n.pitch.nameWithOctave, n.duration.quarterLength)
                   for n in parsed_abc.flat.notes]

# Create a MIDI file using Mido
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(Message('program_change', program=0, time=0))

ticks_per_beat = 480
for note, duration in notes_durations:
  track.append(Message('note_on', note=note_to_midi(note), velocity=64,
                       time=0))
  track.append(
    Message('note_off',
            note=note_to_midi(note),
            velocity=64,
            time=int(duration * ticks_per_beat)))

mid.save('star_spangled_banner.mid')

# Path to your SoundFont file (replace with your own)
soundfont = "/gs/gs.sf2"

# Convert MIDI to WAV using FluidSynth
fluidsynth.midi_to_audio('star_spangled_banner.mid',
                         'star_spangled_banner.wav',
                         soundfont_path=soundfont)

# Convert WAV to MP3 using pydub
wav_audio = AudioSegment.from_wav('star_spangled_banner.wav')
wav_audio.export('star_spangled_banner.mp3', format='mp3')
