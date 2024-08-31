import pyaudio
import wave
import tkinter as tk
from tkinter import messagebox

class VoiceRecorder:
    def __init__(self):
        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.is_recording = False

    def start_recording(self):
        # Start the audio stream and recording process
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=44100,
                                      input=True,
                                      frames_per_buffer=1024)
        self.frames = []
        self.is_recording = True
        self.record_audio()

    def record_audio(self):
        # Continue recording audio in chunks
        if self.is_recording:
            data = self.stream.read(1024)
            self.frames.append(data)
            self.root.after(1, self.record_audio)

    def stop_recording(self):
        # Stop the recording process
        if self.is_recording:
            self.is_recording = False
            self.stream.stop_stream()
            self.stream.close()

    def save_recording(self):
        # Save the recorded audio to a WAV file
        if self.frames:
            filename = "output.wav"
            wf = wave.open(filename, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            messagebox.showinfo("Success", f"Recording saved as {filename}")
        else:
            messagebox.showwarning("Warning", "No recording to save!")

    def create_ui(self):
        # Create the user interface using Tkinter
        self.root = tk.Tk()
        self.root.title("Voice Recorder")

        start_button = tk.Button(self.root, text="Start Recording", command=self.start_recording)
        start_button.pack(pady=10)

        stop_button = tk.Button(self.root, text="Stop Recording", command=self.stop_recording)
        stop_button.pack(pady=10)

        save_button = tk.Button(self.root, text="Save Recording", command=self.save_recording)
        save_button.pack(pady=10)

        self.root.mainloop()

    def __del__(self):
        # Clean up and terminate PyAudio
        self.audio.terminate()

if __name__ == "__main__":
    recorder = VoiceRecorder()
    recorder.create_ui()
