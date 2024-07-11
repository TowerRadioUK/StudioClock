import tkinter as tk
import time

# Function to update the time
def update_time():
    current_time = time.strftime('%H:%M:%S')  # Get current time in HH:MM:SS format
    clock_label.config(text=current_time)  # Update the label with the current time
    root.after(1000, update_time)  # Call this function again after 1000ms (1 second)

# Create the main window
root = tk.Tk()
root.title("Fullscreen Digital Clock")

# Make the window fullscreen
root.attributes('-fullscreen', True)

# Create a label to display the clock
clock_label = tk.Label(root, font=('Helvetica', 100), bg='black', fg='white')
clock_label.pack(expand=True)

# Call the function to update the time for the first time
update_time()

# Bind the escape key to exit fullscreen mode
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

# Start the Tkinter event loop
root.mainloop()
