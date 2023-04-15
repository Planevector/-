import cv2
import numpy as np
import socket

UDP_IP = "192.168.2.11"
UDP_PORT = 5005
PACKET_SIZE = 65507
PACKET_HEADER_SIZE = 4

cap = cv2.VideoCapture(0)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    ret, frame = cap.read()
    encoded_frame = cv2.imencode('.jpg', frame)[1].tobytes()

    # Packetize the frame data
    for i in range(0, len(encoded_frame), PACKET_SIZE - PACKET_HEADER_SIZE):
        packet_seq_bytes = i.to_bytes(PACKET_HEADER_SIZE, byteorder='big')
        packet_data = encoded_frame[i:i + PACKET_SIZE - PACKET_HEADER_SIZE]
        packet = packet_seq_bytes + packet_data

        # Send the packet
        sock.sendto(packet, (UDP_IP, UDP_PORT))
