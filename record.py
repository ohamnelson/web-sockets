import pyaudio
import wave

def record_and_save_audio(file_path, duration=20, sample_rate=44100):
    # Set up the recording parameters
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1  # Mono recording

    p = pyaudio.PyAudio()

    stream = p.open(format=format,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk)

    print(f"Recording {duration} seconds of audio...")

    frames = []

    for i in range(0, int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Recording complete. Saving to file...")

    # Save the recorded audio data to a WAV file
    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved to {file_path}")

    stream.stop_stream()
    stream.close()
    p.terminate()


# Example usage
file_path = 'recorded_audio.wav'
record_and_save_audio(file_path, duration=5)
