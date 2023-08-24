# Keylogger

This is a simple Python keylogger program that records key presses and sends log files to a specified email address.

## Features

- Logs key presses and application focus changes.
- Sends log files via email.
- Runs in the background.

## Prerequisites

Before using this program, you need to have the following:

- Python 3.x installed on your computer.
- Required Python packages installed (`pynput`, `requests`, `smtplib`, `win32gui`).
- A Gmail account to send logs through email.
- Less secure apps access enabled on your Gmail account (not recommended for sensitive accounts).

## Installation

1. Clone this repository to your local machine:

git clone https://github.com/yourusername/keylogger.git

Install the required Python packages:

pip install pynput requests pywin32

Update the email and password fields in the send_logs function with your Gmail credentials.

Usage

Run the keylogger: python keylogger.py

The keylogger will start recording key presses and application focus changes in the background.

To stop the keylogger, press Ctrl + C in the terminal.

Log files will be sent to the specified email address periodically.

Disclaimer

This keylogger is provided for educational and ethical purposes only. It is the user's responsibility to comply with all applicable laws in their country.

