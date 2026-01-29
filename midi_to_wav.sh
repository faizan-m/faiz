#!/bin/bash
# Convert MIDI files to WAV using FluidSynth
# Usage: ./midi_to_wav.sh [input.mid] [output.wav]
#   Or:  ./midi_to_wav.sh [directory]  (converts all .mid files in directory)

set -e

# Default soundfont location (Debian/Ubuntu)
SOUNDFONT="/usr/share/sounds/sf2/FluidR3_GM.sf2"

# Check if fluidsynth is installed
if ! command -v fluidsynth &> /dev/null; then
    echo "❌ Error: fluidsynth is not installed"
    echo "Install with: sudo apt-get install fluidsynth fluid-soundfont-gm"
    exit 1
fi

# Check if soundfont exists
if [ ! -f "$SOUNDFONT" ]; then
    echo "⚠️  Warning: Default soundfont not found at $SOUNDFONT"
    echo "Searching for alternative soundfonts..."
    SOUNDFONT=$(find /usr/share/sounds -name "*.sf2" 2>/dev/null | head -n 1)
    if [ -z "$SOUNDFONT" ]; then
        echo "❌ No soundfont found. Install with: sudo apt-get install fluid-soundfont-gm"
        exit 1
    fi
    echo "✓ Using: $SOUNDFONT"
fi

convert_midi() {
    local input="$1"
    local output="$2"
    
    echo "🎵 Converting: $input"
    echo "   → $output"
    
    # FluidSynth command:
    # -ni: non-interactive, no shell
    # -g: gain (volume)
    # -F: output file
    # -r: sample rate
    fluidsynth -ni \
        -g 1.0 \
        -F "$output" \
        -r 44100 \
        "$SOUNDFONT" \
        "$input" \
        > /dev/null 2>&1
    
    if [ -f "$output" ]; then
        size=$(du -h "$output" | cut -f1)
        echo "   ✓ Created: $output ($size)"
    else
        echo "   ❌ Failed to create: $output"
        return 1
    fi
}

# Main logic
if [ $# -eq 0 ]; then
    echo "Usage:"
    echo "  $0 input.mid output.wav          # Convert single file"
    echo "  $0 directory/                     # Convert all .mid files in directory"
    exit 1
fi

if [ $# -eq 2 ]; then
    # Single file conversion
    INPUT="$1"
    OUTPUT="$2"
    
    if [ ! -f "$INPUT" ]; then
        echo "❌ Error: Input file not found: $INPUT"
        exit 1
    fi
    
    convert_midi "$INPUT" "$OUTPUT"
    
elif [ $# -eq 1 ]; then
    # Directory conversion
    DIR="$1"
    
    if [ ! -d "$DIR" ]; then
        echo "❌ Error: Directory not found: $DIR"
        exit 1
    fi
    
    # Find all .mid files
    shopt -s nullglob
    midi_files=("$DIR"/*.mid)
    
    if [ ${#midi_files[@]} -eq 0 ]; then
        echo "❌ No .mid files found in: $DIR"
        exit 1
    fi
    
    echo "Found ${#midi_files[@]} MIDI file(s)"
    echo "Using soundfont: $SOUNDFONT"
    echo ""
    
    success_count=0
    fail_count=0
    
    for midi_file in "${midi_files[@]}"; do
        base_name=$(basename "$midi_file" .mid)
        wav_file="$DIR/${base_name}.wav"
        
        if convert_midi "$midi_file" "$wav_file"; then
            ((success_count++))
        else
            ((fail_count++))
        fi
        echo ""
    done
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "✓ Converted: $success_count"
    if [ $fail_count -gt 0 ]; then
        echo "❌ Failed: $fail_count"
    fi
    echo "📁 Output directory: $DIR"
fi
