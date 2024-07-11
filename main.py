from flask import Flask, request, jsonify
import threading
import tkinter as tk
import time

# Create the Flask application
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Welcome to the Tower Radio Studio Clock. Goodbye.'

# Function to handle the POST request to /micLive
@app.route('/micLive', methods=['POST'])
def mic_live():
    data = request.get_json()
    mic_number = data.get('micNumber')

    if mic_number is None:
        return jsonify({'error': 'Mic number parameter is required'}), 400

    # Perform any necessary action based on micNumber
    print(f"Received micNumber: {mic_number}")

    toggle_lamp(mic_number)

    return jsonify({'message': f'Received micNumber: {mic_number}'}), 200

def toggle_lamp(lamp_number):
    # 1 - Mikey
    # 2 - PlayIt Live
    # 3 - Dead Air
    # 4 - Fault

    # 5 - Mic 1
    # 6 - Mic 2
    # 7 - Mic 3
    # 8 - Mic 4

    match lamp_number:
        case 5:
            text = 'Mic 1'
            if lamp_mic1.cget('bg') == 'black':
                lamp_mic1.config(bg='red', text=text)
            else:
                lamp_mic1.config(bg='black', text=text)
        case 6:
            text = 'Mic 2'
            if lamp_mic2.cget('bg') == 'black':
                lamp_mic2.config(bg='blue', text=text)
            else:
                lamp_mic2.config(bg='black', text=text)
        case 7:
            text = 'Mic 3'
            if lamp_mic3.cget('bg') == 'black':
                lamp_mic3.config(bg='green', text=text)
            else:
                lamp_mic3.config(bg='black', text=text)
        case 8:
            text = 'Mic 4'
            if lamp_mic4.cget('bg') == 'black':
                lamp_mic4.config(bg='brown', text=text)
            else:
                lamp_mic4.config(bg='black', text=text)
            

def update_time():
    current_time = time.strftime('%H:%M:%S')
    current_minute = int(time.strftime('%S'))
    worded_time = get_worded_time(current_time)

    clock_label.config(text=current_time, justify='left')
    worded_label.config(text=worded_time, justify='left')

    # Update lamp colors and text based on the current minute
    if current_minute % 2 == 0:
        lamp_200.config(bg='red', text='Mikey')
    else:
        lamp_200.config(bg='black', text='Mikey')

    if current_minute % 2 != 0:
        lamp_215.config(bg='green', text='PlayIt\nLive')
    else:
        lamp_215.config(bg='black', text='PlayIt\nLive')

    if current_minute == 30:
        lamp_230.config(bg='blue', text='Dead\nAir')
    else:
        lamp_230.config(bg='black', text='Dead\nAir')

    if current_minute == 45:
        lamp_245.config(bg='yellow', text='test')
    else:
        lamp_245.config(bg='black', text='test')

    root.after(1000, update_time)

def get_worded_time(current_time):
    # Extract hours and minutes from the formatted time string
    current_hour, current_minute = map(int, current_time.split(":")[:2])

    current_hour = current_hour % 12
    current_hour = 12 if current_hour == 0 else current_hour  # Convert 0 hour to 12 for readability

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
        next_hour = (current_hour % 12) + 1  # Ensure next hour is also in 12-hour format
        worded_time = f"{quarter_to} {next_hour}"
    elif current_minute < 30:
        worded_time = f"{current_minute} {minutes_past} {current_hour}"
    else:
        next_hour = (current_hour % 12) + 1  # Ensure next hour is also in 12-hour format
        worded_time = f"{60 - current_minute} {minutes_to} {next_hour}"

    return worded_time

def start_flask_app():
    app.run(port=25543)

# Create the main window
root = tk.Tk()
root.title("Fullscreen Digital and Worded Clock")
root.attributes('-fullscreen', True)
root.configure(bg='black')

# Create the labels for the clock and worded time
clock_label = tk.Label(root, font=('Helvetica', 196), fg='white', bg='black')
worded_label = tk.Label(root, font=('Helvetica', 64), fg='white', bg='black')

size = 36
# Create the lamp labels with text
lamp_mic1 = tk.Label(root, font=('Helvetica', size), width=8, height=4, bg='black', fg='white', wraplength=300)
lamp_mic2 = tk.Label(root, font=('Helvetica', size), width=8, height=4, bg='black', fg='white', wraplength=300)
lamp_mic3 = tk.Label(root, font=('Helvetica', size), width=8, height=4, bg='black', fg='white', wraplength=300)
lamp_mic4 = tk.Label(root, font=('Helvetica', size), width=8, height=4, bg='black', fg='white', wraplength=300)

lamp_200 = tk.Label(root, font=('Helvetica', size), width=8, height=4, bg='black', fg='white', wraplength=150)
lamp_215 = tk.Label(root, font=('Helvetica', size), width=8, height=4, bg='black', fg='white', wraplength=150)
lamp_230 = tk.Label(root, font=('Helvetica', size), width=8, height=4, bg='black', fg='white', wraplength=150)
lamp_245 = tk.Label(root, font=('Helvetica', size), width=8, height=4, bg='black', fg='white', wraplength=150)

lamp_mic1.config(bg='black', text='Mic 1')
lamp_mic2.config(bg='black', text='Mic 2')
lamp_mic3.config(bg='black', text='Mic 3')
lamp_mic4.config(bg='black', text='Mic 4')

# Grid layout with centered labels and lamps at the top
lamp_mic1.grid(row=3, column=0, padx=15, pady=15, sticky='s')
lamp_mic2.grid(row=3, column=1, padx=15, pady=15, sticky='s')
lamp_mic3.grid(row=3, column=2, padx=15, pady=15, sticky='s')
lamp_mic4.grid(row=3, column=3, padx=15, pady=15, sticky='s')

# Grid layout with centered labels and lamps at the top
lamp_200.grid(row=0, column=0, padx=15, pady=15, sticky='n')
lamp_215.grid(row=0, column=1, padx=15, pady=15, sticky='n')
lamp_230.grid(row=0, column=2, padx=15, pady=15, sticky='n')
lamp_245.grid(row=0, column=3, padx=15, pady=15, sticky='n')

clock_label.grid(row=1, column=0, columnspan=4, sticky='n', padx=20, pady=(root.winfo_screenheight() // 4 - 200, 0))
worded_label.grid(row=2, column=0, columnspan=4, sticky='n', padx=20, pady=10)

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

if __name__ == '__main__':
    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=start_flask_app)
    flask_thread.daemon = True
    flask_thread.start()

    # Start the Tkinter main loop
    root.mainloop()
