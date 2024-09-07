from flask import Flask, request, jsonify
import threading
import tkinter as tk
import time
import tomli
import os
from tkinter import messagebox
import weather

VERSION = "1.1.0"
TITLE = f"Tower Radio Studio Clock v{VERSION}"

try:
    with open("config.toml", mode="rb") as fp:
        config = tomli.load(fp)
except FileNotFoundError:
    messagebox.showerror(
        TITLE, "Unable to locate configuration file. config.toml was not found."
    )
    exit()

TITLE = f"{config['info']['station_name']} Studio Clock v{VERSION} - Licensed to {config['info']['license_email']}"

import azuracast

# Create the Flask application
app = Flask(__name__)

# Global dictionary to keep track of active microphones and their start times
mic_start_times = {}
mic_threads = {}


# Weather information
town, owm_api = config["weather"]["town"], config["weather"]["owm_api"]


@app.route("/")
def hello():
    return TITLE


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
                lamp_pil.config(bg="#161616")

        # FAULT
        case 4:
            if active:
                lamp_fault.config(bg="crimson", text="FAULT")
            else:
                lamp_fault.config(bg="#161616", text="FAULT")

        # FAULT - Chat active
        case 41:
            if active:
                lamp_fault.config(bg="crimson", text="FAULT\nChat active")
            else:
                lamp_fault.config(bg="#161616", text="FAULT")

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
                lamp_mic1.config(bg="#161616")

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
                lamp_mic2.config(bg="#161616")

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
                lamp_mic3.config(bg="#161616")

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
                lamp_mic4.config(bg="#161616")


def update_time():
    current_time = time.strftime("%H:%M:%S")
    current_seconds = int(time.strftime("%S"))
    worded_time = get_worded_time(current_time)

    clock_label.config(text=current_time)
    worded_label.config(text=worded_time)

    # Mikey lamp - Red when AutoDJ is active, updates every 3 seconds

    if current_time.endswith("0:00"):
        date_label.config(text=f"{time.strftime('%A %d %B')}")
        temperature, weather_desc, windspeed = weather.get_weather(town, owm_api)
        website_label.config(text=f"{temperature}°C, {weather_desc}")

    if current_seconds % 3 == 0:
        np_label.config(text=azuracast.get_now_playing())
        if azuracast.get_streamer() == "":
            lamp_mikey.config(bg="darkorchid3")
            lamp_pil.config(bg="#161616")
        elif azuracast.get_streamer() == "FAULT":
            lamp_fault.config(bg="crimson", text="FAULT\nNo streamer")
        else:
            lamp_pil.config(bg="green")
            lamp_mikey.config(bg="#161616")

    root.after(500, update_time)


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


# Create the main window
root = tk.Tk()
if not config["other"]["debug"]:
    root.title(TITLE)
    root.attributes("-fullscreen", True)
else:
    root.title(f"{TITLE} (Debug)")
root.configure(bg="#161616")

# Create the labels for the clock and worded time
temperature, weather_desc, windspeed = weather.get_weather(town, owm_api)

website_label = tk.Label(
    root,
    font=("Helvetica", 38),
    fg="yellow",
    bg="#161616",
    text=f"{temperature}°C, {weather_desc}",
)
date_label = tk.Label(
    root,
    font=("Helvetica", 48),
    fg="gray95",
    bg="#161616",
    text=f"{time.strftime('%A %d %B')}",
)
clock_label = tk.Label(root, font=("Helvetica", 196), fg="white", bg="#161616")
worded_label = tk.Label(root, font=("Helvetica", 52), fg="gray95", bg="#161616")
np_label = tk.Label(
    root,
    font=("Helvetica", 32),
    fg="yellow",
    bg="#161616",
    text=azuracast.get_now_playing(),
)

size = 36
# Create the lamp labels with text
lamp_mic1 = tk.Label(
    root, font=("Helvetica", size), width=10, height=4, bg="#161616", fg="white"
)
lamp_mic2 = tk.Label(
    root, font=("Helvetica", size), width=10, height=4, bg="#161616", fg="white"
)
lamp_mic3 = tk.Label(
    root, font=("Helvetica", size), width=10, height=4, bg="#161616", fg="white"
)
lamp_mic4 = tk.Label(
    root, font=("Helvetica", size), width=10, height=4, bg="#161616", fg="white"
)

lamp_mikey = tk.Label(
    root, font=("Helvetica", size), width=10, height=4, bg="#161616", fg="white"
)
lamp_pil = tk.Label(
    root, font=("Helvetica", size), width=10, height=4, bg="#161616", fg="white"
)
lamp_atrium = tk.Label(
    root, font=("Helvetica", size), width=10, height=4, bg="#161616", fg="white"
)
lamp_fault = tk.Label(
    root, font=("Helvetica", size), width=10, height=4, bg="#161616", fg="white"
)

lamp_mic1.config(bg="#161616", fg="gray95", text="Mic 1")
lamp_mic2.config(bg="#161616", fg="gray95", text="Mic 2")
lamp_mic3.config(bg="#161616", fg="gray95", text="Mic 3")
lamp_mic4.config(bg="#161616", fg="gray95", text="Mic 4")

lamp_mikey.config(bg="#161616", fg="gray95", text="AutoDJ\nLive")
lamp_pil.config(bg="#161616", fg="gray95", text="Studio\nLive")
lamp_atrium.config(bg="#161616", fg="gray95", text="Atrium\nPlaying")
lamp_fault.config(bg="#161616", fg="gray95", text="FAULT")

# Grid layout with centered labels and lamps at the top
lamp_mic1.grid(row=6, column=0, padx=5, pady=5, sticky="s")
lamp_mic2.grid(row=6, column=1, padx=5, pady=5, sticky="s")
lamp_mic3.grid(row=6, column=2, padx=5, pady=5, sticky="s")
lamp_mic4.grid(row=6, column=3, padx=5, pady=5, sticky="s")

# Grid layout with centered labels and lamps at the top
lamp_mikey.grid(row=0, column=0, padx=5, pady=5, sticky="n")
lamp_pil.grid(row=0, column=1, padx=5, pady=5, sticky="n")
lamp_atrium.grid(row=0, column=2, padx=5, pady=5, sticky="n")
lamp_fault.grid(row=0, column=3, padx=5, pady=5, sticky="n")

website_label.grid(
    row=1,
    column=0,
    columnspan=4,
    sticky="n",
    padx=20,
    pady=0,
)
date_label.grid(
    row=2,
    column=0,
    columnspan=4,
    sticky="n",
    padx=20,
    pady=10,
)
clock_label.grid(
    row=3,
    column=0,
    columnspan=4,
    sticky="n",
    padx=20,
    pady=10,
)
worded_label.grid(row=4, column=0, columnspan=4, sticky="n", padx=20, pady=10)
np_label.grid(row=5, column=0, columnspan=4, sticky="n", padx=20, pady=10)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)


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
    and lamp_fault.config(bg="#161616", text="FAULT"),
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
