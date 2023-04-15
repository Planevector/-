import socket
import cv2
import numpy as np

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

PACKET_SIZE = 65507
PACKET_HEADER_SIZE = 4

while True:
    data, addr = sock.recvfrom(PACKET_SIZE)
    packet_seq = int.from_bytes(data[:PACKET_HEADER_SIZE], byteorder='big')
    packet_data = data[PACKET_HEADER_SIZE:]
    print(f"Received packet {packet_seq} with {len(packet_data)} bytes of data.")
    
    # 解码图像数据
    img = cv2.imdecode(np.frombuffer(packet_data, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is not None:
        cv2.imshow('image',img)
        cv2.waitKey(1)
       