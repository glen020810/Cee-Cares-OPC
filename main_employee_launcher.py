import requests
import socket
import time
import os
import subprocess
import sys

# IP ng Admin PC - palitan kung iba
server_ip = '192.168.1.6'

# Local file na magtatanda kung approved na
approval_file = 'approval_status.txt'

client_name = socket.gethostname()

def is_approved_locally():
    """Check kung may approval file at 'approved' ang status."""
    if os.path.exists(approval_file):
        with open(approval_file, 'r') as f:
            status = f.read().strip()
            return status == 'approved'
    return False

def save_approval_locally():
    """Gumawa ng local file para hindi na ulit mag-request sa future."""
    with open(approval_file, 'w') as f:
        f.write('approved')

def launch_employee_app():
    """Buksan ang Employee Application."""
    print("[✔] Launching Employee Application...")
    if sys.platform.startswith('win'):
        subprocess.Popen(['python', 'employee_admin.py'], shell=True)
    else:
        subprocess.Popen(['python3', 'employee_admin.py'])

def request_approval():
    """Magpadala ng connection request sa server."""
    try:
        response = requests.post(f'http://{server_ip}:5000/request_access', json={"client_name": client_name})
        if response.status_code == 200:
            status = response.json().get('status')
            return status
        else:
            print(f"[✖] Unexpected server response: {response.status_code}")
    except Exception as e:
        print(f"[✖] Cannot connect to server: {e}")
    return None

def main():
    if is_approved_locally():
        print("[✔] Already approved. Launching EMS...")
        launch_employee_app()
        return

    print("[…] Requesting server approval...")
    
    while True:
        status = request_approval()

        if status == 'approved':
            print("[✔] Approved by server!")
            save_approval_locally()
            launch_employee_app()
            break
        elif status == 'pending':
            print("[…] Waiting for admin approval...")
        else:
            print("[✖] Unexpected response or cannot connect. Retrying...")

        time.sleep(5)  # Retry every 5 seconds

if __name__ == '__main__':
    main()
