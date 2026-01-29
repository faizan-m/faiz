import random
from music21 import *

# ==========================================
# SECTION 3: THEORETICAL MODELING
# ==========================================

def get_yaman_scale(root_note='D4'):
    """
    Returns a list of pitches for Raag Yaman based on the root.
    Formula: R (Maj 2nd), G (Maj 3rd), M# (Aug 4th), P (Perf 5th), D (Maj 6th), N (Maj 7th).
    """
    tonic = pitch.Pitch(root_note)
    # Intervals from Tonic: Maj2, Maj3, Aug4, Perf5, Maj6, Maj7
    # Note: 'A4' represents Augmented 4th (Tivra Ma) 
    intervals = ['M2', 'M3', 'A4', 'P5', 'M6', 'M7']
    
    yaman_pitches = [tonic]
    for int_str in intervals:
        p = tonic.transpose(int_str)
        
        # Section 7: Microtonality Implementation
        # Sharpen the Tivra Ma (A4) by 10 cents to add "yearning" 
        if int_str == 'A4':
            p.microtone = 10 
            
        yaman_pitches.append(p)
        
    return yaman_pitches # 

# Define the Revolutionary Progression (The "Dha Conflict") 
# This introduces G Natural and Bb, alien to Yaman.
chord_progression = {
    'I': chord.Chord(['D3', 'F#3', 'A3']),    # D Major
    'V': chord.Chord(['A2', 'C#3', 'E3']),    # A Major
    'IV': chord.Chord(['G2', 'B2', 'D3']),     # G Major (Standard)
    'iv': chord.Chord(['G2', 'Bb2', 'D3']),    # G Minor (The "Hope" Chord/Minor IV) 
}

# ==========================================
# SECTION 5: INSTRUMENTATION & PERCUSSION MAP
# ==========================================

# Mapped based on the table in "Section 5.3: The 'Sahar-e-Nau' Percussion Map" 
tabla_map = {
    'Ge': [36],         # Resonant Bass (Kick)
    'Na': [37],         # Sharp Rim (Side Stick)
    'Tin': [45],        # Soft Resonant (Low Tom)
    'Dha': [36, 37],    # Bass + Rim (Combo)
    'Dhin': [36, 45],   # Bass + Soft (Combo)
    'Ka': [44],         # Flat Slap (Pedal Hi-Hat)
    'Ke': [44]
}

def create_sitar_drone():
    """
    Creates the Shadow Drone Part (Simulating Tarab strings).
    """
    sitar_drone = stream.Part()
    sitar_drone.insert(0, instrument.Sitar())
    
    # Logic: Add long-held D3 and A3 notes at low velocity (pp)
    drone_root = note.Note('D3')
    drone_root.volume.velocity = 30 # Pianissimo 
    drone_root.quarterLength = 100  # Long duration
    
    drone_fifth = note.Note('A3')
    drone_fifth.volume.velocity = 30
    drone_fifth.quarterLength = 100

    sitar_drone.insert(0, drone_root)
    sitar_drone.insert(0, drone_fifth)
    return sitar_drone

# ==========================================
# SECTION 6: MOVEMENT CONSTRUCTION
# ==========================================

# --- Movement I: The Golden Cage (Alaap) ---
def generate_alaap(duration_quarters=32):
    """
    Generates a free-form Alaap in Raag Yaman using weighted probabilities.
    """
    alaap_stream = stream.Part()
    alaap_stream.insert(0, instrument.Sitar())
    
    # Get Yaman pitches in D4 register
    yaman_scale = get_yaman_scale('D4')
    # Extract pitch names for the random choice
    scale_names = [p.nameWithOctave for p in yaman_scale]
    
    # Weights favor the Vaadi (Third - F#) and Samvaadi (Seventh - C#) 
    # Rough mapping to scale indices: Sa, Re, Ga(Vaadi), Ma#, Pa, Dha, Ni(Samvaadi)
    weights = [0.1, 0.1, 0.3, 0.1, 0.1, 0.1, 0.2] 
    
    current_offset = 0.0
    
    while current_offset < duration_quarters:
        # Choose a pitch based on weights
        p_str = random.choices(scale_names, weights=weights, k=1)[0]
        n = note.Note(p_str)
        
        # Vary durations to simulate "rubato" (free time)
        dur = random.choice([0.5, 1.0, 1.5, 2.0]) 
        n.quarterLength = dur
        
        alaap_stream.insert(current_offset, n)
        current_offset += dur
        
    return alaap_stream

# --- Movement II: The Fracture (Tritone Clash) ---
def generate_fracture_texture():
    """
    Creates the dissonance between Yaman's Tivra Ma (G#) and the Rock's Shuddha Ma (G).
    """
    fracture_stream = stream.Part()
    fracture_stream.insert(0, instrument.Violoncello()) # Using Cello for the texture
    
    # Loop for 8 bars (approx 32 quarter lengths)
    for i in range(16):
        # The Clash: G vs G#
        n1 = note.Note('G3')   # Shuddha Ma (Revolution)
        n2 = note.Note('G#3')  # Tivra Ma (Tradition)
        
        n1.quarterLength = 1.0
        n2.quarterLength = 1.0
        
        # Sul Ponticello articulation for "gritty" sound 
        sp = articulations.StrongAccent() 
        n1.articulations.append(sp)
        n2.articulations.append(sp)
        
        # Dynamic Build: Crescendo from p to f 
        velocity = 60 + (i * 3) # capped at ~108
        n1.volume.velocity = velocity
        n2.volume.velocity = velocity
        
        # Append as a chord or alternating notes to create "beating"
        clash_chord = chord.Chord([n1, n2])
        clash_chord.quarterLength = 2.0
        fracture_stream.append(clash_chord)
        
    return fracture_stream

# --- Movement III: The March (Rock Anthem) ---
def make_power_chord(root_name, duration=4.0):
    """
    Creates a Power Chord (Root + 5th).
    """
    r = note.Note(root_name)
    fifth = r.transpose('P5') # Transpose up a Perfect Fifth
    c = chord.Chord([r, fifth])
    c.quarterLength = duration
    return c

def generate_rock_riff():
    """
    Generates the Rhythm Guitar part enforcing the Minor IV progression.
    """
    riff_stream = stream.Part()
    riff_stream.insert(0, instrument.ElectricGuitar())
    
    # Create 4 iterations of the 4-bar progression
    for _ in range(4):
        # Bar 1: D Major (Power)
        riff_stream.append(make_power_chord('D3', 4.0)) 
        
        # Bar 2: A Major (Power)
        riff_stream.append(make_power_chord('A2', 4.0))
        
        # Bar 3: G Major (Power)
        riff_stream.append(make_power_chord('G2', 4.0))
        
        # Bar 4: G Minor (Full Triad for emotional impact) 
        # Includes Bb (Minor 3rd) to signal the "wound"
        gm_chord = chord.Chord(['G2', 'Bb2', 'D3']) 
        gm_chord.quarterLength = 4.0
        riff_stream.append(gm_chord)
        
    return riff_stream

def create_keherwa_cycle():
    """
    Creates one bar of Keherwa Theka (8 beats) with a swung feel.
    Pattern: Dha - Ge - Na - Tin | Na - Ka - Dhin - Na
    """
    m = stream.Measure()
    m.timeSignature = meter.TimeSignature('4/4')
    
    # Rhythm Pattern: (Bol, QuarterLength)
    # Using triplets: Beat is divided into 3 parts. 
    # 'Swing' feel: First note = 2/3 beat, Second note = 1/3 beat.
    # Total QL for a pair must be 1.0
    
    long_beat = 2/3.0
    short_beat = 1/3.0
    
    pattern_bols = [
        ('Dha', long_beat), ('Ge', short_beat),   # Beat 1
        ('Na', long_beat), ('Tin', short_beat),   # Beat 2
        ('Na', long_beat), ('Ka', short_beat),    # Beat 3
        ('Dhin', long_beat), ('Na', short_beat)   # Beat 4
    ]
    
    for bol, q_len in pattern_bols:
        midi_vals = tabla_map[bol]
        
        if len(midi_vals) > 1:
            # Combo stroke (Chord)
            n = chord.Chord(midi_vals)
        else:
            # Single stroke
            n = note.Note(midi_vals[0])
            
        n.quarterLength = q_len
        
        # Explicitly define tuplet to ensure correct notation/playback 
        t = duration.Tuplet(3, 2)
        n.duration.tuplets = (t,)
        m.append(n)
        
    return m

# --- Movement IV: Synthesis ---
def generate_synthesis_melody():
    """
    Generates a Sitar melody that adapts to the Rock Grid.
    """
    synthesis_part = stream.Part()
    synthesis_part.insert(0, instrument.Sitar())
    
    yaman_scale = get_yaman_scale('D4')
    safe_note_names = [p.nameWithOctave for p in yaman_scale]

    # Locked to the 4/4 grid (no rubato, straight 8ths) 
    for _ in range(8 * 8): # 8 bars of 8th notes
        n = note.Note(random.choice(safe_note_names))
        n.quarterLength = 0.5 # Straight 8ths match the rock drums
        synthesis_part.append(n)
        
    return synthesis_part

# ==========================================
# MAIN ASSEMBLY: THE CONDUCTOR
# ==========================================

def build_sahar_e_nau():
    """
    Assembles the Score > Part > Measure hierarchy.
    """
    # Initialize Score and Metadata 
    score = stream.Score()
    score.metadata = metadata.Metadata()
    score.metadata.title = "Sahar-e-Nau: Symphony of the Awakening"
    score.metadata.composer = "Faiz Fusion Project"
    
    # 1. Generate Parts
    print("Generating Movement I: Alaap...")
    sitar_alaap = generate_alaap(duration_quarters=32)
    sitar_drone = create_sitar_drone()
    
    print("Generating Movement II: Fracture...")
    fracture = generate_fracture_texture()
    
    print("Generating Movement III: Rock Anthem...")
    guitar_riff = generate_rock_riff()
    
    # Generate Drums: Create a Part and repeat the Keherwa cycle
    drums_part = stream.Part()
    drums_part.insert(0, instrument.UnpitchedPercussion()) # Placeholder 
    keherwa_bar = create_keherwa_cycle()
    # Repeat the bar for the duration of the rock section (approx 16 bars)
    for _ in range(16):
        # We deepcopy the measure to avoid reference issues
        import copy
        drums_part.append(copy.deepcopy(keherwa_bar))

    print("Generating Movement IV: Synthesis...")
    sitar_synthesis = generate_synthesis_melody()

    # 2. Add Parts to Score with offsets 
    # To simplify, we will treat 'score' as a container of simultaneous parts, 
    # but we will append measures sequentially within the parts or use insert with offsets.
    # Here we construct the full timeline part by part.

    # -- Constructing the Master Sitar Part --
    master_sitar = stream.Part()
    master_sitar.id = 'Sitar'
    master_sitar.insert(0, instrument.Sitar())
    
    # Mov I (0-32 QL)
    for element in sitar_alaap.recurse().notes:
        master_sitar.insert(element.offset, element)
    
    # Mov IV (Synthesis) - entering later
    # Calculate offset based on previous sections (Mov I + II + III)
    # Mov I (32) + Mov II (32) + Mov III (64) = 128 QL start
    synthesis_start_offset = 32 + 32 + 64
    for element in sitar_synthesis.recurse().notes:
        master_sitar.insert(synthesis_start_offset + element.offset, element)

    # -- Constructing the Texture/Cello Part --
    master_cello = stream.Part()
    master_cello.id = 'Cello'
    master_cello.insert(0, instrument.Violoncello())
    # Enter at Mov II (Offset 32)
    for element in fracture.recurse().notes:
        master_cello.insert(32 + element.offset, element)

    # -- Constructing the Guitar Part --
    master_guitar = stream.Part()
    master_guitar.id = 'Guitar'
    master_guitar.insert(0, instrument.ElectricGuitar())
    # Enter at Mov III (Offset 64)
    for element in guitar_riff.recurse().notes:
        master_guitar.insert(64 + element.offset, element)

    # -- Constructing the Drum Part --
    master_drums = stream.Part()
    master_drums.id = 'Drums'
    master_drums.insert(0, instrument.UnpitchedPercussion())
    # Enter at Mov III (Offset 64) with metric modulation
    current_drum_offset = 64
    for measure in drums_part:
        master_drums.insert(current_drum_offset, measure)
        current_drum_offset += 4.0

    # 3. Metric Modulation (Tempo) 
    # Initial Tempo (Ghazal)
    score.insert(0, tempo.MetronomeMark(number=72))
    
    # Modulation at Rock Section (Mov III, Offset 64)
    # 72 * 1.5 = 108 BPM
    score.insert(64, tempo.MetronomeMark(number=108))

    # Add all parts to score
    score.insert(0, master_sitar)
    score.insert(0, master_cello)
    score.insert(0, master_guitar)
    score.insert(0, master_drums)
    # Note: Drone is omitted here for brevity but follows similar logic
    
    return score