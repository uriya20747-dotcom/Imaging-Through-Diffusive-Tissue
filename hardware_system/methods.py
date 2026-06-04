import os
import serial
#ser = serial.Serial('/dev/ttyUSB0', 115200)

# convert each name to hexa
# example: IMO-> "49 4D 30"
def convert_ascii_hexa(name):
    result=""
    for ch in name:
        char_convert_hexa= format(ord(ch), "X")

        result+=char_convert_hexa
    spaced_string = ' '.join(result[i:i + 2] for i in range(0, len(result), 2))
    return spaced_string

# Will count the length of command by the formula: Num of Spaces+1= Length of command.
def count_len_command(image_command):
    count=0
    for i in image_command:
        if (i==' '):
            count+=1
    count+=1
    count_in_hex = format(count, 'X')
    return count_in_hex

# Will calculate the parity byte by xor between each byte.
def cal_parity_byte(image_command):
    first_command = 0xA5  # Assuming first command is represented as an integer
    res_xor = first_command

    # Convert the image command to a list of integers representing bytes
    command_without_space = [int(byte, 16) for byte in image_command.split()]

    # Perform XOR operation on each byte
    for byte in command_without_space[1:-1]:
        res_xor ^= byte
    res_xor_in_hex = format(res_xor, 'X')
    return res_xor_in_hex


def xor_strings(str1, str2):
    # if not same len xor will not works
    if len(str1) != len(str2):
        raise ValueError("Strings must have the same length for XOR operation")

    # Convert each character to its Unicode value, perform XOR, and convert back to character
    result = ''.join(chr(ord(char1) ^ ord(char2)) for char1, char2 in zip(str1, str2))
    return result
    
# Function to send commands from a file
def send_commands_from_file(file_path,ser):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            command = bytes.fromhex(line.strip())  # Convert the hex string to bytes
            ser.write(command)  # Send the command
