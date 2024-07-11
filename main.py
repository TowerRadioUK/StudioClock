import tkinter as tk
import time

def update_time():
    current_time = time.strftime('%H:%M:%S')
    worded_time = get_worded_time()
    clock_label.config(text=current_time, justify='left')
    worded_label.config(text=worded_time, justify='left')
    root.after(1000, update_time)

def get_worded_time():
    current_hour = int(time.strftime('%H')) % 12
    current_minute = int(time.strftime('%M'))

    if current_minute == 0:
        worded_time = f"{number_to_words(current_hour)} o'clock"
    elif current_minute == 15:
        worded_time = f"quarter past {number_to_words(current_hour)}"
    elif current_minute == 30:
        worded_time = f"half past {number_to_words(current_hour)}"
    elif current_minute == 45:
        worded_time = f"quarter to {number_to_words((current_hour + 1) % 24)}"
    elif current_minute < 30:
        worded_time = f"{number_to_words(current_minute)} minutes past {number_to_words(current_hour)}"
    else:
        worded_time = f"{number_to_words(60 - current_minute)} minutes to {number_to_words((current_hour + 1) % 24)}"

    return worded_time

def number_to_words(n):
    return n

root = tk.Tk()
root.title("Fullscreen Digital and Worded Clock")
root.attributes('-fullscreen', True)
root.configure(bg='black')

clock_label = tk.Label(root, font=('Helvetica', 100), bg='black', fg='white')
clock_label.pack(anchor='w', padx=20, pady=20)

worded_label = tk.Label(root, font=('Helvetica', 50), bg='black', fg='white')
worded_label.pack(anchor='w', padx=20, pady=20)

update_time()

root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

root.mainloop()