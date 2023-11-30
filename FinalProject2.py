import socket
import struct
import streamlit as st
import matplotlib.pyplot as plt
import threading

# TCP server settings
HOST = '192.168.137.1'
PORT = 6364

# Streamlit settings
st.title('Real-time Temperature Plot')

# Initialize the plot
fig, ax = plt.subplots()
line, = ax.plot([], [], label='Temperature (F)')
ax.legend()

# Initialize data lists
x_data = []
y_data = []

# Event to signal when the connection is established
connection_event = threading.Event()

def update_plot():
    while True:
        data = b""
        # Keep receiving until you have enough bytes
        while len(data) < 4:
            packet = conn.recv(4 - len(data))
            if not packet:
                break
            data += packet

        if len(data) < 4:
            break

        temperature = struct.unpack('f', data)[0]
        x_data.append(len(x_data) + 1)
        y_data.append(temperature)
        line.set_data(x_data, y_data)
        ax.relim()
        ax.autoscale_view()
        st.text(f"Received temperature: {temperature:.2f} F")

# Start receiving temperature data in the background
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    st.text(f"Listening on {HOST}:{PORT}")
    conn, addr = s.accept()
    with conn:
        st.text(f"Connected by {addr}")
        # Signal that the connection is established
        connection_event.set()
        # Run the update_plot function in the main thread
        update_plot()

# Note: The code below this line will only be executed once the connection is closed
