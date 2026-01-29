import pytest
from music21 import pitch, chord, stream, note, instrument, meter
import music
import random


class TestGetYamanScale:
    """Test the get_yaman_scale function."""
    
    def test_default_root_note(self):
        """Test Yaman scale with default root note D4."""
        scale = music.get_yaman_scale()
        assert len(scale) == 7, "Yaman scale should have 7 notes"
        assert scale[0].nameWithOctave == 'D4', "First note should be D4"
    
    def test_custom_root_note(self):
        """Test Yaman scale with custom root note."""
        scale = music.get_yaman_scale('C4')
        assert scale[0].nameWithOctave == 'C4', "First note should be C4"
        assert len(scale) == 7, "Scale should have 7 notes"
    
    def test_scale_intervals(self):
        """Test that the scale has correct intervals."""
        scale = music.get_yaman_scale('D4')
        # Expected notes: D4, E4, F#4, G#4, A4, B4, C#5
        expected_names = ['D', 'E', 'F#', 'G#', 'A', 'B', 'C#']
        actual_names = [p.name for p in scale]
        assert actual_names == expected_names, f"Expected {expected_names}, got {actual_names}"
    
    def test_microtone_on_augmented_fourth(self):
        """Test that A4 interval has microtone adjustment."""
        scale = music.get_yaman_scale('D4')
        # Fourth note (index 3) should be G# with microtone
        # Microtone is an object, so check if it's set
        assert scale[3].microtone is not None, "G# should have microtone"
        # The string representation should show the cents value
        assert "10" in str(scale[3].microtone), "Microtone should be +10 cents"


class TestChordProgression:
    """Test the chord progression dictionary."""
    
    def test_chord_progression_exists(self):
        """Test that chord_progression is defined."""
        assert hasattr(music, 'chord_progression')
        assert isinstance(music.chord_progression, dict)
    
    def test_chord_progression_keys(self):
        """Test that all required chord keys exist."""
        expected_keys = ['I', 'V', 'IV', 'iv']
        for key in expected_keys:
            assert key in music.chord_progression, f"Key {key} missing from chord_progression"
    
    def test_chord_types(self):
        """Test that all values in chord_progression are Chord objects."""
        for key, val in music.chord_progression.items():
            assert isinstance(val, chord.Chord), f"chord_progression[{key}] should be a Chord object"


class TestTablaMap:
    """Test the tabla_map dictionary."""
    
    def test_tabla_map_exists(self):
        """Test that tabla_map is defined."""
        assert hasattr(music, 'tabla_map')
        assert isinstance(music.tabla_map, dict)
    
    def test_tabla_map_values(self):
        """Test that all tabla strokes have MIDI note mappings."""
        for bol, midi_notes in music.tabla_map.items():
            assert isinstance(midi_notes, list), f"{bol} should map to a list"
            assert len(midi_notes) > 0, f"{bol} should have at least one MIDI note"
            for midi_val in midi_notes:
                assert isinstance(midi_val, int), f"MIDI values should be integers"


class TestCreateSitarDrone:
    """Test the create_sitar_drone function."""
    
    def test_creates_part(self):
        """Test that function returns a Part object."""
        drone = music.create_sitar_drone()
        assert isinstance(drone, stream.Part), "Should return a stream.Part"
    
    def test_has_sitar_instrument(self):
        """Test that the part has a Sitar instrument."""
        drone = music.create_sitar_drone()
        instruments = [el for el in drone.recurse() if isinstance(el, instrument.Sitar)]
        assert len(instruments) > 0, "Should have Sitar instrument"
    
    def test_has_drone_notes(self):
        """Test that drone has at least two notes."""
        drone = music.create_sitar_drone()
        notes = list(drone.recurse().notes)
        assert len(notes) >= 2, "Drone should have at least 2 notes"
    
    def test_drone_velocity(self):
        """Test that drone notes have low velocity (pianissimo)."""
        drone = music.create_sitar_drone()
        notes = list(drone.recurse().notes)
        for n in notes:
            assert n.volume.velocity <= 40, "Drone notes should be soft (low velocity)"


class TestGenerateAlaap:
    """Test the generate_alaap function."""
    
    def test_returns_part(self):
        """Test that function returns a Part object."""
        alaap = music.generate_alaap(duration_quarters=8)
        assert isinstance(alaap, stream.Part), "Should return a stream.Part"
    
    def test_has_sitar_instrument(self):
        """Test that the part has a Sitar instrument."""
        alaap = music.generate_alaap(duration_quarters=8)
        instruments = [el for el in alaap.recurse() if isinstance(el, instrument.Sitar)]
        assert len(instruments) > 0, "Should have Sitar instrument"
    
    def test_generates_notes(self):
        """Test that alaap generates notes."""
        alaap = music.generate_alaap(duration_quarters=8)
        notes = list(alaap.recurse().notes)
        assert len(notes) > 0, "Should generate at least some notes"
    
    def test_respects_duration(self):
        """Test that alaap respects the duration parameter."""
        alaap = music.generate_alaap(duration_quarters=16)
        total_duration = sum(n.quarterLength for n in alaap.recurse().notes)
        # Allow some tolerance
        assert total_duration >= 15, f"Duration should be close to 16, got {total_duration}"
    
    def test_randomness(self):
        """Test that two alaap generations are different (probabilistic)."""
        random.seed(42)
        alaap1 = music.generate_alaap(duration_quarters=8)
        random.seed(43)
        alaap2 = music.generate_alaap(duration_quarters=8)
        
        notes1 = [n.nameWithOctave for n in alaap1.recurse().notes]
        notes2 = [n.nameWithOctave for n in alaap2.recurse().notes]
        
        # They should be different sequences (probabilistic, but very likely)
        assert notes1 != notes2, "Different seeds should produce different sequences"


class TestGenerateFractureTexture:
    """Test the generate_fracture_texture function."""
    
    def test_returns_part(self):
        """Test that function returns a Part object."""
        fracture = music.generate_fracture_texture()
        assert isinstance(fracture, stream.Part), "Should return a stream.Part"
    
    def test_has_cello_instrument(self):
        """Test that the part has a Cello instrument."""
        fracture = music.generate_fracture_texture()
        instruments = [el for el in fracture.recurse() if isinstance(el, instrument.Violoncello)]
        assert len(instruments) > 0, "Should have Cello instrument"
    
    def test_generates_chords(self):
        """Test that fracture generates chords."""
        fracture = music.generate_fracture_texture()
        chords = list(fracture.recurse().getElementsByClass(chord.Chord))
        assert len(chords) > 0, "Should generate chords"
    
    def test_dynamic_crescendo(self):
        """Test that dynamics increase over time."""
        fracture = music.generate_fracture_texture()
        chords = list(fracture.recurse().getElementsByClass(chord.Chord))
        if len(chords) >= 2:
            first_velocity = chords[0].volume.velocity
            last_velocity = chords[-1].volume.velocity
            assert last_velocity >= first_velocity, "Velocity should increase (crescendo)"


class TestMakePowerChord:
    """Test the make_power_chord function."""
    
    def test_returns_chord(self):
        """Test that function returns a Chord object."""
        pc = music.make_power_chord('D3')
        assert isinstance(pc, chord.Chord), "Should return a Chord"
    
    def test_has_two_notes(self):
        """Test that power chord has two notes (root and fifth)."""
        pc = music.make_power_chord('D3')
        assert len(pc.pitches) == 2, "Power chord should have 2 notes"
    
    def test_perfect_fifth_interval(self):
        """Test that the interval is a perfect fifth."""
        pc = music.make_power_chord('D3')
        pitches = list(pc.pitches)
        # Calculate interval between first and second note
        interval_val = pitches[1].midi - pitches[0].midi
        assert interval_val == 7, "Interval should be a perfect fifth (7 semitones)"
    
    def test_duration_parameter(self):
        """Test that duration parameter is respected."""
        pc = music.make_power_chord('D3', duration=2.0)
        assert pc.quarterLength == 2.0, "Should respect duration parameter"


class TestGenerateRockRiff:
    """Test the generate_rock_riff function."""
    
    def test_returns_part(self):
        """Test that function returns a Part object."""
        riff = music.generate_rock_riff()
        assert isinstance(riff, stream.Part), "Should return a stream.Part"
    
    def test_has_guitar_instrument(self):
        """Test that the part has an ElectricGuitar instrument."""
        riff = music.generate_rock_riff()
        instruments = [el for el in riff.recurse() if isinstance(el, instrument.ElectricGuitar)]
        assert len(instruments) > 0, "Should have ElectricGuitar instrument"
    
    def test_generates_chords(self):
        """Test that riff generates chords."""
        riff = music.generate_rock_riff()
        chords = list(riff.recurse().getElementsByClass(chord.Chord))
        assert len(chords) > 0, "Should generate chords"
    
    def test_progression_length(self):
        """Test that riff has correct number of chords (4 bars * 4 iterations = 16)."""
        riff = music.generate_rock_riff()
        chords = list(riff.recurse().getElementsByClass(chord.Chord))
        assert len(chords) == 16, f"Should have 16 chords (4 iterations * 4 bars), got {len(chords)}"


class TestCreateKeherwaaCycle:
    """Test the create_keherwa_cycle function."""
    
    def test_returns_measure(self):
        """Test that function returns a Measure object."""
        keherwa = music.create_keherwa_cycle()
        assert isinstance(keherwa, stream.Measure), "Should return a Measure"
    
    def test_has_time_signature(self):
        """Test that measure has 4/4 time signature."""
        keherwa = music.create_keherwa_cycle()
        ts = keherwa.timeSignature
        assert ts is not None, "Should have a time signature"
        assert ts.numerator == 4 and ts.denominator == 4, "Should be 4/4 time"
    
    def test_generates_notes(self):
        """Test that keherwa generates notes."""
        keherwa = music.create_keherwa_cycle()
        notes = list(keherwa.recurse().notes)
        assert len(notes) > 0, "Should generate notes"
    
    def test_has_tuplets(self):
        """Test that notes have tuplet markers (swing feel)."""
        keherwa = music.create_keherwa_cycle()
        notes = list(keherwa.recurse().notes)
        # At least some notes should have tuplets
        tuplet_count = sum(1 for n in notes if n.duration.tuplets)
        assert tuplet_count > 0, "Should have notes with tuplets for swing feel"


class TestGenerateSynthesisMelody:
    """Test the generate_synthesis_melody function."""
    
    def test_returns_part(self):
        """Test that function returns a Part object."""
        synthesis = music.generate_synthesis_melody()
        assert isinstance(synthesis, stream.Part), "Should return a stream.Part"
    
    def test_has_sitar_instrument(self):
        """Test that the part has a Sitar instrument."""
        synthesis = music.generate_synthesis_melody()
        instruments = [el for el in synthesis.recurse() if isinstance(el, instrument.Sitar)]
        assert len(instruments) > 0, "Should have Sitar instrument"
    
    def test_generates_notes(self):
        """Test that synthesis generates notes."""
        synthesis = music.generate_synthesis_melody()
        notes = list(synthesis.recurse().notes)
        assert len(notes) > 0, "Should generate notes"
    
    def test_straight_eighths(self):
        """Test that all notes are eighth notes (0.5 quarter length)."""
        synthesis = music.generate_synthesis_melody()
        notes = list(synthesis.recurse().notes)
        for n in notes:
            assert n.quarterLength == 0.5, "All notes should be straight eighths (0.5 QL)"
    
    def test_expected_note_count(self):
        """Test that it generates expected number of notes (8 bars * 8 eighth notes)."""
        synthesis = music.generate_synthesis_melody()
        notes = list(synthesis.recurse().notes)
        assert len(notes) == 64, f"Should have 64 notes (8 bars * 8 eighths), got {len(notes)}"


class TestBuildSaharENau:
    """Test the build_sahar_e_nau function."""
    
    def test_returns_score(self):
        """Test that function returns a Score object."""
        score = music.build_sahar_e_nau()
        assert isinstance(score, stream.Score), "Should return a stream.Score"
    
    def test_has_metadata(self):
        """Test that score has metadata."""
        score = music.build_sahar_e_nau()
        assert score.metadata is not None, "Should have metadata"
        assert score.metadata.title is not None, "Should have a title"
        assert score.metadata.composer is not None, "Should have a composer"
    
    def test_has_parts(self):
        """Test that score has multiple parts."""
        score = music.build_sahar_e_nau()
        parts = list(score.getElementsByClass(stream.Part))
        assert len(parts) > 0, "Should have at least one part"
    
    def test_has_tempo_markings(self):
        """Test that score has tempo markings."""
        score = music.build_sahar_e_nau()
        from music21 import tempo
        tempo_marks = list(score.recurse().getElementsByClass(tempo.MetronomeMark))
        assert len(tempo_marks) >= 1, "Should have at least one tempo marking"
    
    def test_metric_modulation(self):
        """Test that score has tempo changes (metric modulation)."""
        score = music.build_sahar_e_nau()
        from music21 import tempo
        tempo_marks = list(score.recurse().getElementsByClass(tempo.MetronomeMark))
        if len(tempo_marks) >= 2:
            assert tempo_marks[0].number != tempo_marks[1].number, "Should have different tempos"
    
    def test_has_notes(self):
        """Test that score has notes across all parts."""
        score = music.build_sahar_e_nau()
        notes = list(score.recurse().notes)
        assert len(notes) > 0, "Score should have notes"
    
    def test_score_exportable_to_midi(self):
        """Test that score can be exported to MIDI format."""
        import tempfile
        import os
        score = music.build_sahar_e_nau()
        
        # Create a temporary file for MIDI export
        with tempfile.NamedTemporaryFile(suffix='.mid', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Organize into measures before MIDI export (required by music21)
            score_with_measures = score.makeMeasures()
            
            # Attempt to write MIDI file
            score_with_measures.write('midi', fp=tmp_path)
            
            # Verify file was created and has content
            assert os.path.exists(tmp_path), "MIDI file should be created"
            assert os.path.getsize(tmp_path) > 0, "MIDI file should have content"
        finally:
            # Clean up
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def test_score_exportable_to_musicxml(self):
        """Test that score can be exported to MusicXML format."""
        import tempfile
        import os
        score = music.build_sahar_e_nau()
        
        # Create a temporary file for MusicXML export
        with tempfile.NamedTemporaryFile(suffix='.xml', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Organize into measures before export (recommended for proper notation)
            score_with_measures = score.makeMeasures()
            
            # Attempt to write MusicXML file
            score_with_measures.write('musicxml', fp=tmp_path)
            
            # Verify file was created and has content
            assert os.path.exists(tmp_path), "MusicXML file should be created"
            assert os.path.getsize(tmp_path) > 0, "MusicXML file should have content"
        finally:
            # Clean up
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


class TestIntegration:
    """Integration tests for the complete workflow."""
    
    def test_full_composition_pipeline(self):
        """Test that the full composition can be built without errors."""
        # This is an integration test that exercises the complete pipeline
        score = music.build_sahar_e_nau()
        
        # Verify basic structure
        assert isinstance(score, stream.Score)
        assert len(list(score.getElementsByClass(stream.Part))) > 0
        assert len(list(score.recurse().notes)) > 0
        
        # Verify metadata
        assert score.metadata.title is not None
        assert score.metadata.composer is not None
    
    def test_yaman_scale_in_context(self):
        """Test that Yaman scale integrates properly with other functions."""
        scale = music.get_yaman_scale('D4')
        scale_names = [p.nameWithOctave for p in scale]
        
        # Use scale in alaap generation
        alaap = music.generate_alaap(duration_quarters=8)
        alaap_notes = [n.name for n in alaap.recurse().notes]
        
        # All alaap notes should come from the Yaman scale
        scale_note_names = [p.name for p in scale]
        for note_name in alaap_notes:
            assert note_name in scale_note_names, f"Note {note_name} not in Yaman scale"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
