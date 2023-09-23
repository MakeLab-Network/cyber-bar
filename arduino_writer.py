import os
import time
import serial

receive_file_path = "from_arduino.txt"
transmit_file_path = "to_arduino.txt"
buttons_file_path = "buttons_from_arduino.txt"


def get_file_timestamp(filepath):
    """Returns the last modified timestamp of a file."""

    return os.path.getmtime(filepath)


def read_file_content(filepath):
    """Reads the content of a file."""
    with open(filepath, 'r') as f:
        return f.read()


def write_file_content(filepath, content):
    """Reads the content of a file."""
    with open(filepath, 'w') as f:
        f.write(content)


def main():
    # FILEPATH = 'arduino_msg.txt'    # replace with the path to your file
    # replace with your COM port (e.g., 'COM3' for Windows, '/dev/ttyUSB0' for Linux)
    PORT = 'COM50'
    BAUDRATE = 9600                       # adjust the baud rate if needed

    # Initialize the serial connection
    ser = serial.Serial(PORT, BAUDRATE)
    last_timestamp = get_file_timestamp(transmit_file_path)
    print("strating")
    try:
        while True:
            current_timestamp = get_file_timestamp(transmit_file_path)
            if current_timestamp != last_timestamp:
                content = read_file_content(transmit_file_path)
                # sends the file content through the serial connection
                ser.write(content.encode())
                last_timestamp = current_timestamp
                print("File changed! Content sent.")

            if (ser.in_waiting > 0):
                # read the bytes and convert from binary array to ASCII
                from_arduino = ser.readline().decode()
                data_str = ser.read(ser.in_waiting).decode('ascii')
                if from_arduino[0] == "@":
                    write_file_content(buttons_file_path, from_arduino[1])

            # time.sleep(0.2)  # sleep for 1 second before checking again

    except KeyboardInterrupt:
        print("Script stopped by user.")
    finally:
        ser.close()


if __name__ == '__main__':
    main()
