import tkinter as tk
import serial
import threading

# Function to start the motor in the forward direction
def start_motor_forward(event=None):
    ser.write(b'H')

# Function to stop the motor
def stop_motor(event=None):
    ser.write(b'R')

# Function to start the motor in the backward direction
def start_motor_backward(event=None):
    ser.write(b'B')

# Function to read data from serial port
def read_serial():
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            print(f'Received from Arduino: {line}')
            # Parse data as needed
            # Example: If Arduino sends "Sensor1: 123 Sensor2: 456", parse it here

# Initialize the serial connection
ser = serial.Serial('COM4', 115200, timeout=0.1)  # Adjust the COM port and baudrate as needed

# Create a thread for reading serial data
serial_thread = threading.Thread(target=read_serial)
serial_thread.daemon = True  # Set the thread as daemon so it exits when the main program exits
serial_thread.start()

# Create the GUI window
root = tk.Tk()
root.title("Stepper Motor Control")

# Create a button to run the motor in the forward direction
forward_button = tk.Button(root, text="Hold to Run Forward", width=20, height=2)
forward_button.pack(pady=20)
forward_button.bind('<ButtonPress-1>', start_motor_forward)
forward_button.bind('<ButtonRelease-1>', stop_motor)

# Create a button to run the motor in the backward direction
backward_button = tk.Button(root, text="Hold to Run Backward", width=20, height=2)
backward_button.pack(pady=20)
backward_button.bind('<ButtonPress-1>', start_motor_backward)
backward_button.bind('<ButtonRelease-1>', stop_motor)

# Start the GUI loop
root.mainloop()

# Close the serial connection when the program exits
ser.close()
