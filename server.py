import socket
import threading
import pyaudio
import pickle
import struct

host_ip = '10.10.10.159'
port = 9611

# Create a socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host_ip, (port-1)))
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

def broadcast(data_len):
    """_summary_
    This function sends messages to all the connected clients
    """
    for client_socket in clients:
        # Receive the audio data
        audio_data = client_socket.recv(data_len)

        # Play the received audio data
        stream.write(audio_data)

def handle(client_socket):
    while True:
        try:
            # Receive the packed message containing the length and audio data
            message = client_socket.recv(8)

            # Unpack the message to get the length of the audio data
            data_len = struct.unpack("Q", message)[0]

            
            broadcast(data_len)
 
        # We are constantly trying to get messages from the client. It will not 
        # give an error if the client doesn't send anything. it will only
        # give an error when the client is not there anymore
        except:
            clients.remove(client_socket)
            client_socket.close()
            #broadcast(f"".encode('ascii'))
            break

def receive():
    while True:
        client_socket, addr = server_socket.accept()
        print(f"connected with {str(addr)}")

        clients.append(client_socket)
        #broadcast(f"{addr} joined the call".encode('ascii'))
        #client_socket.send("Connected to the server!".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client_socket,))
        thread.start()

receive()
 

# t1 = threading.Thread(target=audio_stream, args=())
# t1.start()


# def audio_stream():

#     # Accept an incoming client connection and retrieve the client socket and address
#     client_socket, addr = server_socket.accept()
#     print(f"connected with {addr}")

#     # Continuously stream audio data from the microphone to the client
#     while client_socket:
#         try:
#             # Read audio data from the microphone
#             if stream.is_active():
#                 data = stream.read(CHUNK, exception_on_overflow = False)

#             # Pack the length of the data and the data itself using struct
#             message = struct.pack("Q", len(data)) + data

#             # Send the packed message to the client
#             client_socket.sendall(message)
#         except Exception as e:
#             # Handle any exceptions and print an error message
#             print(f"Error: {str(e)}")
#             break
        
#         # Cleanup: Stop the audio stream, close the stream, terminate PyAudio, and close the server socket
#         # if stream.is_active():
#         #     stream.stop_stream()
#         # stream.close()
#         # p.terminate()
#     client_socket.close()