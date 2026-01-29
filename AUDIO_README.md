# Sahar-e-Nau Audio Generation

This project generates a fusion composition combining Indian classical music (Raag Yaman) with rock music.

## Quick Start

### 1. Export MIDI Files
```bash
jupyter notebook export_sahar_e_nau.ipynb
# Or run cells 1-6 in the notebook
```

### 2. Convert MIDI to Audio
```bash
# Install FluidSynth (if not in devcontainer)
sudo apt-get install fluidsynth fluid-soundfont-gm

# Convert all MIDI files
./midi_to_wav.sh .

# Or convert single file
./midi_to_wav.sh sahar_e_nau_full_score.mid output.wav
```

## Files Generated

### MIDI Files
- `sahar_e_nau_full_score.mid` - Complete orchestration
- `sahar_e_nau_sitar.mid` - Sitar part (Movements I & IV)
- `sahar_e_nau_cello.mid` - Cello part (Movement II)
- `sahar_e_nau_guitar.mid` - Electric guitar part (Movement III)
- `sahar_e_nau_drums.mid` - Drums part (Movement III)

### WAV Files (after conversion)
Same filenames with `.wav` extension

## Composition Structure

**Duration:** ~6:40 minutes

1. **Movement I: The Golden Cage (Alaap)** - 1:47
   - Sitar solo in free time exploring Raag Yaman
   - Tempo: 72 BPM

2. **Movement II: The Fracture** - 1:47  
   - Cello creating dissonance between G and G# (tritone clash)
   - Tempo: 72 BPM

3. **Movement III: The March (Rock Anthem)** - 1:11
   - Electric guitar power chords with Keherwa drums
   - Tempo: 108 BPM (metric modulation)

4. **Movement IV: Synthesis** - 0:36
   - Sitar melody locked to rock rhythm grid
   - Tempo: 108 BPM

## Tools & Dependencies

- Python 3.11+
- music21
- FluidSynth (for audio conversion)
- pytest (for tests)

## Testing

```bash
# Run all tests
pytest test_music.py -v

# Run specific test
pytest test_music.py::TestIntegration::test_drums_part_has_content -v
```
