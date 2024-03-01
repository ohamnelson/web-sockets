import socket
import struct
import pyaudio
import threading

host_ip = '10.10.10.159'
port = 9611

# Create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host_ip, port))

# Initialize PyAudio
p = pyaudio.PyAudio()

# Define the chunk size for audio processing
CHUNK = 4096

# Configure the audio stream for playback
stream_play = p.open(format=pyaudio.paInt16,
                     channels=1,
                     rate=22050,
                     output=True,
                     frames_per_buffer=CHUNK)

stream_read = p.open(format=pyaudio.paInt16,
                     channels=1,
                     rate=22050,
                     input=True,
                     frames_per_buffer=CHUNK)

def receive():
    while True:
        try:
            # Receive the packed message containing the length and audio data
            message = client_socket.recv(8)

            # Unpack the message to get the length of the audio data
            data_len = struct.unpack("Q", message)[0]

            # Receive the audio data
            audio_data = client_socket.recv(data_len)

            # Play the received audio data
            stream_play.write(audio_data)

        except Exception as e:
            # Handle any exceptions and print an error message
            print(f"Error: {str(e)}")
            break

def write():
    while True:
        try:
            # Read audio data from the microphone
            if stream_read.is_active():
                data = stream_read.read(CHUNK, exception_on_overflow=False)

            # Pack the length of the data and the data itself using struct
            message = struct.pack("Q", len(data)) + data

            # Send the packed message to the server
            client_socket.sendall(message)
        except Exception as e:
            # Handle any exceptions and print an error message
            print(f"Error: {str(e)}")
            break

t1_receive = threading.Thread(target=receive)
t1_receive.start()

t2_write = threading.Thread(target=write)
t2_write.start()
