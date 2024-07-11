from flask import Flask, request, jsonify
import threading
import tkinter as tk
import time

DEBUG = True

# Create the Flask application
app = Flask(__name__)


@app.route("/")
def hello():
    return "Welcome to the Tower Radio Studio Clock. Goodbye."


@app.route("/channelLive", methods=["POST"])
def channel_live():
    data = request.get_json()
    lampNumber = data.get("lampNumber")

    # Perform any necessary action based on micNumber
    print(f"Received lampNumber: {lampNumber}")

    # Toggle the lamp before returning the response
    threading.Thread(target=toggle_lamp, args=(lampNumber, data.get("active"))).start()

    return jsonify({"message": f"Received lampNumber: {lampNumber}"}), 200


def toggle_lamp(lamp_number, active):
    # 1 - Mikey
    # 2 - PlayIt Live
    # 3 - Dead Air
    # 4 - Fault

    # 5 - Mic 1
    # 6 - Mic 2
    # 7 - Mic 3
    # 8 - Mic 4

    match lamp_number:
        # Main Stereo
        case 2:
            if active:
                lamp_pil.config(bg="green")
            else:
                lamp_pil.config(bg="black")

        # Dead Air
        case 4:
            if active:
                lamp_deadair.config(bg="blue")
                lamp_pil.config(bg="crimson")
            else:
                lamp_deadair.config(bg="black")
                lamp_pil.config(bg="black")
        
        # FAULT
        case 4:
            if active:
                lamp_pil.config(bg="crimson")
            else:
                lamp_pil.config(bg="black")

        # Mic 1 - Red
        case 5:
            if active:
                lamp_mic1.config(bg="red")
            else:
                lamp_mic1.config(bg="black")

        # Mic 2 - Blue
        case 6:
            if active:
                lamp_mic2.config(bg="blue")
            else:
                lamp_mic2.config(bg="black")

        # Mic 3 - Green
        case 7:
            if active:
                lamp_mic3.config(bg="green")
            else:
                lamp_mic3.config(bg="black")

        # Mic 4 - Yellow
        case 8:
            if active:
                lamp_mic4.config(bg="orange2")
            else:
                lamp_mic4.config(bg="black")


def update_time():
    current_time = time.strftime("%H:%M:%S")
    current_minute = int(time.strftime("%S"))
    worded_time = get_worded_time(current_time)

    clock_label.config(text=current_time)
    worded_label.config(text=worded_time)

    # Update lamp colors and text based on the current minute
    if current_minute == 30:
        lamp_mikey.config(bg="red")
    else:
        lamp_mikey.config(bg="black")

    root.after(1000, update_time)


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
    app.run(host="0.0.0.0", port=25543)


# Create the main window
root = tk.Tk()
root.title("Tower Radio - Studio Clock")
if not DEBUG:
    root.attributes("-fullscreen", True)
root.configure(bg="black")

# Create the labels for the clock and worded time
clock_label = tk.Label(root, font=("Helvetica", 196), fg="white", bg="black")
worded_label = tk.Label(root, font=("Helvetica", 64), fg="white", bg="black")

size = 36
# Create the lamp labels with text
lamp_mic1 = tk.Label(
    root, font=("Helvetica", size), width=10, height=4, bg="black", fg="white"
)
lamp_mic2 = tk.Label(
    root, font=("Helvetica", size), width=10, height=4, bg="black", fg="white"
)
lamp_mic3 = tk.Label(
    root, font=("Helvetica", size), width=10, height=4, bg="black", fg="white"
)
lamp_mic4 = tk.Label(
    root, font=("Helvetica", size), width=10, height=4, bg="black", fg="white"
)

lamp_mikey = tk.Label(
    root, font=("Helvetica", size), width=10, height=4, bg="black", fg="white"
)
lamp_pil = tk.Label(
    root, font=("Helvetica", size), width=10, height=4, bg="black", fg="white"
)
lamp_deadair = tk.Label(
    root, font=("Helvetica", size), width=10, height=4, bg="black", fg="white"
)
lamp_fault = tk.Label(
    root, font=("Helvetica", size), width=9, height=4, bg="black", fg="white"
)

lamp_mic1.config(bg="black", text="Mic 1")
lamp_mic2.config(bg="black", text="Mic 2")
lamp_mic3.config(bg="black", text="Mic 3")
lamp_mic4.config(bg="black", text="Mic 4")

lamp_mikey.config(bg="black", text="Mikey")
lamp_pil.config(bg="black", text="PlayIt\nLive")
lamp_deadair.config(bg="black", text="Dead\nAir")
lamp_fault.config(bg="black", text="FAULT")

# Grid layout with centered labels and lamps at the top
lamp_mic1.grid(row=3, column=0, padx=15, pady=15, sticky="s")
lamp_mic2.grid(row=3, column=1, padx=15, pady=15, sticky="s")
lamp_mic3.grid(row=3, column=2, padx=15, pady=15, sticky="s")
lamp_mic4.grid(row=3, column=3, padx=15, pady=15, sticky="s")

# Grid layout with centered labels and lamps at the top
lamp_mikey.grid(row=0, column=0, padx=15, pady=15, sticky="n")
lamp_pil.grid(row=0, column=1, padx=15, pady=15, sticky="n")
lamp_deadair.grid(row=0, column=2, padx=15, pady=15, sticky="n")
lamp_fault.grid(row=0, column=3, padx=15, pady=15, sticky="n")

clock_label.grid(
    row=1,
    column=0,
    columnspan=4,
    sticky="n",
    padx=20,
    pady=(root.winfo_screenheight() // 4 - 200, 0),
)
worded_label.grid(row=2, column=0, columnspan=4, sticky="n", padx=20, pady=10)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)

# Start the clock update loop
update_time()

# Exit on Escape keypress
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

if __name__ == "__main__":
    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=start_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    # Start the Tkinter main loop
    root.mainloop()
