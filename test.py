import socket
import threading
import pyaudio
import pickle
import struct

host_name = socket.gethostname()
host_ip = '192.168.1.102'
print(host_name)
port = 9611

p = pyaudio.PyAudio()

print(p.get_default_input_device_info())