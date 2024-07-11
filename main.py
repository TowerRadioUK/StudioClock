import tkinter as tk
import time

def update_time():
    current_time = time.strftime('%H:%M:%S')
    current_minute = int(time.strftime('%S'))
    worded_time = get_worded_time(current_time)
    
    clock_label.config(text=current_time, justify='left')
    worded_label.config(text=worded_time, justify='left')
    
    # Update lamp colors and text based on the current minute
    if current_minute % 2 == 0:
        lamp_00.config(bg='green', text='Mic 1')
    else:
        lamp_00.config(bg='black', text='Mic 1')

    if current_minute % 2 != 0:
        lamp_15.config(bg='green', text='Mic 2')
    else:
        lamp_15.config(bg='black', text='Mic 2')
        
    if current_minute == 30:
        lamp_30.config(bg='green', text='Mic 3')
    else:
        lamp_30.config(bg='black', text='Mic 3')
        
    if current_minute == 45:
        lamp_45.config(bg='green', text='Mic 4')
    else:
        lamp_45.config(bg='black', text='Mic 4')
    
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

# Create the main window
root = tk.Tk()
root.title("Fullscreen Digital and Worded Clock")
root.attributes('-fullscreen', True)
root.configure(bg='black')

# Create the labels for the clock and worded time
clock_label = tk.Label(root, font=('Helvetica', 196), fg='white', bg='black')
worded_label = tk.Label(root, font=('Helvetica', 64), fg='white', bg='black')

# Create the lamp labels with text
lamp_00 = tk.Label(root, font=('Helvetica', 32), width=5, height=2, bg='black', fg='white')
lamp_15 = tk.Label(root, font=('Helvetica', 32), width=5, height=2, bg='black', fg='white')
lamp_30 = tk.Label(root, font=('Helvetica', 32), width=5, height=2, bg='black', fg='white')
lamp_45 = tk.Label(root, font=('Helvetica', 32), width=5, height=2, bg='black', fg='white')

# Grid layout with centered labels and lamps at the top
lamp_00.grid(row=3, column=0, padx=10, pady=10, sticky='n')
lamp_15.grid(row=3, column=1, padx=10, pady=10, sticky='n')
lamp_30.grid(row=3, column=2, padx=10, pady=10, sticky='n')
lamp_45.grid(row=3, column=3, padx=10, pady=10, sticky='n')

clock_label.grid(row=1, column=0, columnspan=4, sticky='n', padx=20, pady=(root.winfo_screenheight() // 4 - 100, 0))
worded_label.grid(row=2, column=0, columnspan=4, sticky='n', padx=20, pady=10)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)

# Start the clock update loop
update_time()

# Exit on Escape keypress
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

# Main event loop
root.mainloop()
