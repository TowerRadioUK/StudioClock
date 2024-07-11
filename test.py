import tkinter as tk

# Function to create a label and add it to the grid
def create_label(text, row, column):
  label = tk.Label(window, text=text)
  label.grid(row=row, column=column)

# Create the main window
window = tk.Tk()
window.title("4x3 Grid")

# Loop to create labels and place them on the grid
for row in range(4):
  for column in range(3):
    label_text = f"Cell ({row+1}, {column+1})"
    create_label(label_text, row, column)

# Start the event loop
window.mainloop()