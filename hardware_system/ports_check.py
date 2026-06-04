import serial.tools.list_ports

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    available_ports = []
    for port, desc, hwid in sorted(ports):
        available_ports.append({
            "port": port,
            "description": desc,
            "hwid": hwid
        })
    return available_ports

if __name__ == "__main__":
    ports = list_serial_ports()
    if ports:
        print("Available serial ports:")
        for port_info in ports:
            print(f"Port: {port_info['port']}, Description: {port_info['description']}, HWID: {port_info['hwid']}")
    else:
        print("No serial ports found.")
