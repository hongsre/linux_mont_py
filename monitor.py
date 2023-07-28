import argparse
import os
import socket
import subprocess
from create_image import create_image
from send_line import send_line
 
SCRIPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")
COMMANDS = {
    "netstat": "sudo netstat -nltp",
    "dmesg": "sudo dmesg -T|tail -n 10",
    "top": "sudo top -n 1 -b|head -n 30"
}
 
def check_port(ip, port, service_name=None):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            result = s.connect_ex((ip, port))
            if result == 0:
                print(f"Port {port} is open")
            else:
                print(f"Port {port} is closed")
                handle_closed_port(ip, service_name)
    except socket.error as e:
        print(f"Error occurred while checking port {port}: {str(e)}")
        raise
 
def handle_closed_port(ip, service_name):
    if service_name:
        # 서비스 시작
        start_service(service_name, ip)
    else:
        generate_images_and_send_lines(ip, f"경고: {port} 포트가 닫혔습니다!")
 
def check_system(ip):
    try:
        generate_images_and_send_lines(ip, f"경고: 시스템 상태 이상이 감지되었습니다!")
    except Exception as e:
        print(f"Error check host {ip}: {e}")
        raise
 
def generate_images_and_send_lines(ip, message):
    for name, command in COMMANDS.items():
        create_image(command, ip, name)
 
    files = [os.path.join(SCRIPT_DIR, ip, f"{name}.png") for name in COMMANDS.keys()]
    send_line(message)
    for file in files:
        send_line(file=file)
 
def start_service(service_name, ip):
    # 서비스 시작
    command = ["systemctl", "start", service_name]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        handle_successful_service_start(service_name, ip)
    else:
        print(f"Failed to start service {service_name}. Error: {result.stderr}")
 
def handle_successful_service_start(service_name, ip):
    print(f"Service {service_name} started successfully.")
    # systemctl status
    cmd = f'sudo systemctl status {service_name}'
    create_image(cmd, ip, "status")
    msg = f"Service {service_name} started successfully."
    file = os.path.join(SCRIPT_DIR, ip, "status.png")
    send_line(msg, files=[file])
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", help="IP address")
    parser.add_argument("-p", "--port", help="Port number", type=int)
    parser.add_argument("-n", "--service-name", help="Service name")
    args = parser.parse_args()
 
    ip = args.ip
    port = args.port
    service_name = args.service_name
 
    if service_name:
        check_port(ip, port, service_name)
    else:
        check_port(ip, port)