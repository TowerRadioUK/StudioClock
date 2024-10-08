from flask import Flask, request, jsonify
import threading
import tkinter as tk
import time
import tomli
import os
from tkinter import messagebox
import weather
import portal

try:
    with open("config.toml", mode="rb") as fp:
        config = tomli.load(fp)
except FileNotFoundError:
    messagebox.showerror(
        "Unable to locate configuration file. config.toml was not found."
    )
    exit()

try:
    with open("pyproject.toml", mode="rb") as fp:
        pyproject = tomli.load(fp)
except FileNotFoundError:
    messagebox.showerror(
        "Unable to locate pyproject file. pyproject.toml was not found."
    )
    exit()

VERSION = pyproject["tool"]["poetry"]["version"]
TITLE = f"Tower Radio Studio Clock v{VERSION}"

TITLE = f"{config['info']['station_name']} Studio Clock v{VERSION} - Licensed to {config['info']['license_email']}"

import azuracast

# Create the Flask application
app = Flask(__name__)

# Global dictionary to keep track of active microphones and their start times
mic_start_times = {}
mic_threads = {}

keepalive_time = time.time()

# Weather information
town, owm_api = config["weather"]["town"], config["weather"]["owm_api"]


@app.route("/")
def hello():
    return TITLE


@app.route("/keepalive", methods=["POST"])
def keepalive():
    global keepalive_time
    keepalive_time = time.time()

    return jsonify({"message": "Received keepalive"}), 200


@app.route("/channelLive", methods=["POST"])
def channel_live():
    data = request.get_json()
    lampNumber = data.get("lampNumber")

    # Toggle the lamp before returning the response
    threading.Thread(target=toggle_lamp, args=(lampNumber, data.get("active"))).start()

    return jsonify({"message": f"Received lampNumber: {lampNumber}"}), 200


def toggle_lamp(lamp_number, active):
    global mic_start_times, mic_threads

    def update_mic_timer(lamp, mic_number):
        while mic_start_times.get(mic_number):
            elapsed_time = int(time.time() - mic_start_times[mic_number])
            lamp.config(text=f"Mic {mic_number}\n({elapsed_time})")
            time.sleep(1)

    # 1 - Mikey
    # 2 - Streamer connected
    # 3 - Atrium listening
    # 4 - FAULT

    # 5 - Mic 1
    # 6 - Mic 2
    # 7 - Mic 3
    # 8 - Mic 4

    match lamp_number:
        # Main Stereo
        case 2:
            if not active:
                lamp_studiolive.config(bg="#333333")

        # FAULT
        case 4:
            if active:
                lamp_fault.config(bg="crimson", text="FAULT")
            else:
                lamp_fault.config(bg="#333333", text="FAULT")

        # FAULT - Chat active
        case 41:
            if active:
                lamp_fault.config(bg="crimson", text="FAULT\nChat active")
            else:
                lamp_fault.config(bg="#333333", text="FAULT")

        # Mic 1 - Red
        case 5:
            if active:
                mic_start_times[1] = time.time()
                lamp_mic1.config(bg="red", text="Mic 1\n(0)")
                mic_threads[1] = threading.Thread(
                    target=update_mic_timer, args=(lamp_mic1, 1)
                )
                mic_threads[1].start()
            else:
                mic_start_times.pop(1, None)
                lamp_mic1.config(bg="#333333")

        # Mic 2 - Green
        case 6:
            if active:
                mic_start_times[2] = time.time()
                lamp_mic2.config(bg="green", text="Mic 2\n(0)")
                mic_threads[2] = threading.Thread(
                    target=update_mic_timer, args=(lamp_mic2, 2)
                )
                mic_threads[2].start()
            else:
                mic_start_times.pop(2, None)
                lamp_mic2.config(bg="#333333")

        # Mic 3 - Blue
        case 7:
            if active:
                mic_start_times[3] = time.time()
                lamp_mic3.config(bg="blue", text="Mic 3\n(0)")
                mic_threads[3] = threading.Thread(
                    target=update_mic_timer, args=(lamp_mic3, 3)
                )
                mic_threads[3].start()
            else:
                mic_start_times.pop(3, None)
                lamp_mic3.config(bg="#333333")

        # Mic 4 - Yellow
        case 8:
            if active:
                mic_start_times[4] = time.time()
                lamp_mic4.config(bg="orange2", text="Mic 4\n(0)")
                mic_threads[4] = threading.Thread(
                    target=update_mic_timer, args=(lamp_mic4, 4)
                )
                mic_threads[4].start()
            else:
                mic_start_times.pop(4, None)
                lamp_mic4.config(bg="#333333")


def update_time():
    current_time = time.strftime("%H:%M:%S")
    current_seconds = int(time.strftime("%S"))

    # Update clock and worded time
    clock_label.config(text=current_time)
    worded_label.config(text=get_worded_time(current_time))

    # Update date and weather info only when minute changes
    if current_time.endswith("0:00"):
        threading.Thread(target=update_weather_and_date).start()

    ## Update labels and lamps every 10 seconds
    if current_seconds % 10 == 0:
        threading.Thread(target=update_np_and_lamps).start()

    ## Update messages lamp every 40 seconds
    if current_seconds == 40:
        threading.Thread(target=update_messages_lamp).start()

    ## Update messages lamp every 40 seconds
    if current_seconds == 20:
        threading.Thread(target=update_keepalive_fault).start()

    # Schedule the next update after 1 second
    root.after(1000, update_time)


def update_weather_and_date():
    date_label.config(text=f"{time.strftime('%A %d %B')}")
    temperature, weather_desc, _ = weather.get_weather(town, owm_api)
    website_label.config(text=f"{temperature}°C, {weather_desc}")


def update_messages_lamp():
    messages = portal.get_messages(
        config["portal"]["api_url"], config["portal"]["api_key"]
    )
    if len(messages) > 0:
        lamp_messages.config(bg="#6256CA")
    else:
        lamp_messages.config(bg="#333333")


def update_keepalive_fault():
    if keepalive_time < time.time() - 45:
        lamp_fault.config(bg="crimson", text="FAULT\nSync Failure")


def update_np_and_lamps():
    np_label.config(text=azuracast.get_now_playing())
    streamer = azuracast.get_streamer()  # Store the result once and reuse
    if streamer == "":
        lamp_autodj.config(bg="darkorchid3")
        lamp_studiolive.config(bg="#333333", text="Studio\nLive")
    elif streamer == "FAULT":
        lamp_fault.config(bg="crimson", text="FAULT\nNo streamer")
    else:
        lamp_studiolive.config(bg="green", text=f"{streamer}\nLive")
        lamp_autodj.config(bg="#333333")


def get_worded_time(current_time):
    # Extract hours and minutes from the formatted time string
    current_hour, current_minute = map(int, current_time.split(":")[:2])

    current_hour = current_hour % 12
    current_hour = (
        12 if current_hour == 0 else current_hour
    )  # Convert 0 hour to 12 for readability

    # Define phrases for each time segment
    if current_minute == 59 or current_minute == 1:
        minutes_past = "minute past"
        minutes_to = "minute to"
    else:
        minutes_past = "minutes past"
        minutes_to = "minutes to"
    o_clock = "o'clock"
    quarter_past = "quarter past"
    half_past = "half past"
    quarter_to = "quarter to"

    if current_minute == 0:
        worded_time = f"{current_hour} {o_clock}"
    elif current_minute == 15:
        worded_time = f"{quarter_past} {current_hour}"
    elif current_minute == 30:
        worded_time = f"{half_past} {current_hour}"
    elif current_minute == 45:
        next_hour = (
            current_hour % 12
        ) + 1  # Ensure next hour is also in 12-hour format
        worded_time = f"{quarter_to} {next_hour}"
    elif current_minute < 30:
        worded_time = f"{current_minute} {minutes_past} {current_hour}"
    else:
        next_hour = (
            current_hour % 12
        ) + 1  # Ensure next hour is also in 12-hour format
        worded_time = f"{60 - current_minute} {minutes_to} {next_hour}"

    return worded_time


def start_flask_app():
    app.run(host=config["server"]["host"], port=config["server"]["port"])


# Initialize the root window
root = tk.Tk()

# Window title and fullscreen
if not config["other"]["debug"]:
    root.title(TITLE)
    root.attributes("-fullscreen", True)
else:
    root.title(f"{TITLE} (Debug)")
root.configure(bg="#1a1a1a")  # Slightly lighter dark background for better contrast

# Get weather information
temperature, weather_desc, windspeed = weather.get_weather(town, owm_api)

# Set styles for fonts
HEADER_FONT = ("Helvetica", 52, "bold")
SUBHEADER_FONT = ("Helvetica", 48)
CLOCK_FONT = ("Helvetica", 196, "bold")
INFO_FONT = ("Helvetica", 32)
LAMP_FONT = ("Helvetica", 28, "bold")

# Create and configure labels
website_label = tk.Label(
    root,
    font=INFO_FONT,
    fg="yellow",
    bg="#1a1a1a",
    text=f"{temperature}°C, {weather_desc}",
)
date_label = tk.Label(
    root,
    font=SUBHEADER_FONT,
    fg="gray95",
    bg="#1a1a1a",
    text=f"{time.strftime('%A %d %B')}",
)
clock_label = tk.Label(root, font=CLOCK_FONT, fg="white", bg="#1a1a1a")
worded_label = tk.Label(root, font=HEADER_FONT, fg="gray95", bg="#1a1a1a")
np_label = tk.Label(
    root,
    font=INFO_FONT,
    fg="yellow",
    bg="#1a1a1a",
    text=azuracast.get_now_playing(),
)

# Lamp labels with clear spacing and modern look
lamp_style = {
    "font": LAMP_FONT,
    "width": 10,
    "height": 2,
    "bg": "#333333",  # Slightly lighter background for lamps
    "fg": "white",
}

lamp_mic1 = tk.Label(root, **lamp_style, text="Mic 1")
lamp_mic2 = tk.Label(root, **lamp_style, text="Mic 2")
lamp_mic3 = tk.Label(root, **lamp_style, text="Mic 3")
lamp_mic4 = tk.Label(root, **lamp_style, text="Mic 4")

lamp_autodj = tk.Label(root, **lamp_style, text="AutoDJ\nLive")
lamp_studiolive = tk.Label(root, **lamp_style, text="Studio\nLive")
lamp_messages = tk.Label(root, **lamp_style, text="Studio\nMessage")
lamp_fault = tk.Label(root, **lamp_style, text="FAULT")

# Grid Layout for Lamps
lamp_mic1.grid(row=6, column=0, padx=15, pady=15, sticky="s")
lamp_mic2.grid(row=6, column=1, padx=15, pady=15, sticky="s")
lamp_mic3.grid(row=6, column=2, padx=15, pady=15, sticky="s")
lamp_mic4.grid(row=6, column=3, padx=15, pady=15, sticky="s")

lamp_autodj.grid(row=0, column=0, padx=15, pady=15, sticky="n")
lamp_studiolive.grid(row=0, column=1, padx=15, pady=15, sticky="n")
lamp_messages.grid(row=0, column=2, padx=15, pady=15, sticky="n")
lamp_fault.grid(row=0, column=3, padx=15, pady=15, sticky="n")

# Grid Layout for Labels
website_label.grid(row=1, column=0, columnspan=4, sticky="n", padx=20, pady=(10, 0))
date_label.grid(row=2, column=0, columnspan=4, sticky="n", padx=20, pady=(10, 0))
clock_label.grid(row=3, column=0, columnspan=4, sticky="n", padx=20, pady=10)
worded_label.grid(row=4, column=0, columnspan=4, sticky="n", padx=20, pady=10)
np_label.grid(row=5, column=0, columnspan=4, sticky="n", padx=20, pady=10)

# Grid Configurations for Weight and Resizing
for i in range(4):
    root.grid_columnconfigure(i, weight=1)
for i in range(7):
    root.grid_rowconfigure(i, weight=1)

# Start the clock update loop
update_time()

# Exit on Escape keypress
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

# Open notepad when "c" is pressed
root.bind("c", lambda event: os.system("notepad config.toml"))

# Quit with q
root.bind(
    "q",
    lambda event: messagebox.askquestion(TITLE, "Are you sure you want to quit?")
    == "yes"
    and exit(),
)

# Exit on Escape keypress
root.bind(
    "f",
    lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")),
)
root.bind(
    "<F11>",
    lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")),
)

# Clear fault on "x"
root.bind(
    "x",
    lambda event: messagebox.showinfo(TITLE, "Cleared fault")
    and lamp_fault.config(bg="#333333", text="FAULT"),
)

# About dialog on "a"
root.bind(
    "a",
    lambda event: messagebox.showinfo(
        "About",
        f"{config['info']['station_name']} Studio Display\nLicensed to {config['info']['license_email']}\n\nPress 'c' to edit the config file\nPress 'f' to toggle fullscreen\nPress 'q' to quit\nPress 'x' to clear faults\n\nhttps://github.com/TowerRadioUK/StudioClock\n\nVersion {VERSION}",
    ),
)


if __name__ == "__main__":
    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=start_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    # Start the Tkinter main loop
    root.mainloop()
