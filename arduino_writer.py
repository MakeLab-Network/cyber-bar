import os
import time
import serial

receive_file_path = "from_arduino.txt"
transmit_file_path = "to_arduino.txt"


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
            print(current_timestamp)
            if current_timestamp != last_timestamp:
                print(1)
                content = read_file_content(transmit_file_path)
                # sends the file content through the serial connection
                ser.write(content.encode())
                last_timestamp = current_timestamp
                print("File changed! Content sent.")

                # while (True):
                #     from_arduino = ser.readline().decode()
                #     print(f"from: {from_arduino}")
                #     if from_arduino:
                #         if from_arduino[0] == "$":
                #             write_file_content(receive_file_path, from_arduino)
                #             break
            time.sleep(1.0)  # sleep for 1 second before checking again

    except KeyboardInterrupt:
        print("Script stopped by user.")
    finally:
        ser.close()


if __name__ == '__main__':
    main()
