import tkinter as tk
from tkinter import messagebox
import pyautogui
import time
import threading
import keyboard

# Global flag to track the state of the auto clicker
auto_clicker_running = False
current_hotkey = "F4"  # Default hotkey


# Function to perform the clicking action
def auto_click(interval, button):
    pyautogui.PAUSE = 0  # Reduce the pause time to zero
    pyautogui.MINIMUM_DURATION = 0  # Remove any minimum duration
    pyautogui.MINIMUM_SLEEP = 0  # Remove any minimum sleep
    pyautogui.MINIMUM_INTERVAL = 0  # Remove any minimum interval

    while not stop_event.is_set():
        pyautogui.click(button=button)
        time.sleep(interval)


# Function to start the auto clicker
def start_clicker():
    global auto_clicker_running
    if not auto_clicker_running:
        try:
            interval = float(interval_entry.get())
            button = button_var.get()

            global stop_event
            stop_event = threading.Event()

            threading.Thread(target=auto_click, args=(interval, button)).start()
            auto_clicker_running = True
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for interval.")
    else:
        stop_clicker()


# Function to stop the auto clicker
def stop_clicker():
    global auto_clicker_running
    if auto_clicker_running:
        stop_event.set()
        auto_clicker_running = False
    else:
        messagebox.showerror("Error", "Auto clicker is not running.")


# Function to update the hotkey
def update_hotkey():
    global current_hotkey
    new_hotkey = hotkey_entry.get()
    if new_hotkey:
        # Unbind the old hotkey
        keyboard.remove_hotkey(current_hotkey)
        current_hotkey = new_hotkey
        # Bind the new hotkey
        keyboard.add_hotkey(current_hotkey, start_clicker)
        messagebox.showinfo("Info", f"Hotkey updated to {current_hotkey}")


# Create the main window
root = tk.Tk()
root.title("Auto Clicker")

# Interval label and entry
tk.Label(root, text="Interval (seconds):").grid(row=0, column=0, padx=10, pady=10)
interval_entry = tk.Entry(root)
interval_entry.insert(0, "0.0001")  # Set default value to 0.0001
interval_entry.grid(row=0, column=1, padx=10, pady=10)

# Mouse button label and radio buttons
tk.Label(root, text="Button:").grid(row=1, column=0, padx=10, pady=10)
button_var = tk.StringVar(value="left")
tk.Radiobutton(root, text="Left", variable=button_var, value="left").grid(
    row=1, column=1, padx=10, pady=10, sticky="w"
)
tk.Radiobutton(root, text="Right", variable=button_var, value="right").grid(
    row=1, column=1, padx=10, pady=10
)

# Hotkey label and entry
tk.Label(root, text="Hotkey:").grid(row=2, column=0, padx=10, pady=10)
hotkey_entry = tk.Entry(root)
hotkey_entry.insert(0, "F4")  # Set default hotkey to F4
hotkey_entry.grid(row=2, column=1, padx=10, pady=10)

# Update hotkey button
tk.Button(root, text="Set Hotkey", command=update_hotkey).grid(
    row=3, column=0, columnspan=2, padx=10, pady=10
)

# Instructions label
tk.Label(root, text="Press 'F4' to start/stop the auto clicker (default)").grid(
    row=4, column=0, columnspan=2, padx=10, pady=10
)

# Set global hotkey for F4 to toggle the auto clicker
keyboard.add_hotkey(current_hotkey, start_clicker)

# Run the main loop
root.mainloop()

# Clean up hotkeys on exit
keyboard.unhook_all_hotkeys()
