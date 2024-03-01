import socket
import threading
import pyaudio
import struct

host_ip = '10.10.10.159'
port = 9611

# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host_ip, port))
server_socket.listen(5)

# Define the chunk size for audio processing
CHUNK = 4096

p = pyaudio.PyAudio()

# Configure the audio stream from the microphone
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=22050,
                output=True,
                frames_per_buffer=CHUNK)
clients = []

def handle(client_socket):
    while True:
        try:
            # Receive the packed message containing the length and audio data
            message = client_socket.recv(8)

            # Unpack the message to get the length of the audio data
            data_len = struct.unpack("Q", message)[0]

            # Break the loop if data_len is 0, indicating the client is disconnecting
            if data_len == 0:
                clients.remove(client_socket)
                client_socket.close()
                break

            broadcast(client_socket, data_len)

        except Exception as e:
            # Handle any exceptions and print an error message
            print(f"Error: {str(e)}")
            clients.remove(client_socket)
            client_socket.close()
            break

def broadcast(sender_socket, data_len):
    """This function sends messages to all the connected clients except the sender"""
    for client_socket in clients:
        # Check if the socket is still open before attempting to send
        if client_socket.fileno() == -1:
            clients.remove(client_socket)
            client_socket.close()
            continue

        # Skip sending to the sender
        if client_socket == sender_socket:
            continue

        # Receive the audio data
        audio_data = sender_socket.recv(data_len)

        # Play the received audio data
        client_socket.sendall(struct.pack("Q", len(audio_data)) + audio_data)

def receive():
    while True:
        client_socket, addr = server_socket.accept()
        print(f"connected with {str(addr)}")

        clients.append(client_socket)

        thread = threading.Thread(target=handle, args=(client_socket,))
        thread.start()

receive()
