import tkinter as tk
from PIL import ImageTk, Image
from tkinter import font
from tkinter import ttk

def create_new_game():
    print("Creating new game...")

def join_game():
    print("Joining game...")

def how_to_play():
    print("How to play...")
    
def create_rounded_button(master, text, command, relx, rely):
    button_img = Image.open("asset/buttonPurple2.png")  # Replace "buttonPurple2.png" with your button background image
    button_img = button_img.resize((240, 100), Image.ANTIALIAS)  # Resize the image as per your requirements

    button_photo = ImageTk.PhotoImage(button_img)  # Convert the PIL Image to a PhotoImage

    button_id = canvas.create_image(
        relx * canvas.winfo_width(),
        rely * canvas.winfo_height(),
        image=button_photo,
    )  # Adjust the position of the button image based on relx and rely values

    text_id = canvas.create_text(
        relx * canvas.winfo_width(),
        rely * canvas.winfo_height(),
        text=text,
        fill="white",
        font=("Arial", 12),
        anchor=tk.CENTER,
    )  # Adjust the position and other properties of the text based on relx and rely values

    canvas.tag_bind(button_id, "<Button-1>", lambda event: command())  # Bind button click to the command

    button = tk.Button(
        master,
        text=text,
        compound=tk.CENTER,
        font=("Arial", 12),
        fg="white",
        bd=0,
        highlightthickness=0,
        relief=tk.FLAT,
        padx=10,
        pady=5,
        command=command,
    )
    button.image = button_photo

    def check_hand(e):  # Runs on mouse motion
        bbox = canvas.bbox(button_id)
        if bbox[0] < e.x < bbox[2] and bbox[1] < e.y < bbox[3]:  # Checks whether the mouse is inside the boundaries
            canvas.config(cursor="hand2")
        else:
            canvas.config(cursor="")

    canvas.tag_bind(button_id, "<Enter>", check_hand)  # Bind enter event to check_hand function
    canvas.tag_bind(button_id, "<Leave>", lambda event: canvas.config(cursor=""))  # Bind leave event to restore default cursor

    return button



# Create the main window
window = tk.Tk()
window.title("SUKOLILO WEREWOLF")

# Load the background image
original_image = Image.open("asset/mainMenuBackground.jpg")
background_image = ImageTk.PhotoImage(original_image)

# Create a canvas
canvas = tk.Canvas(window, width=1920, height=1080)
canvas.pack()

# Set the background image
background_item = canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

# Create the main title label
title_text = "SUKOLILO WEREWOLF"
title_label = canvas.create_text(0, 0, text=title_text, font=("Chiller", 72, "bold"), fill="#916BBF")
canvas.update()  # Update the canvas to compute the text size

# Calculate the initial position for the label
title_x = canvas.winfo_width() // 2
title_y = int(canvas.winfo_height() * 0.2)

# Place the label on top of the buttons
canvas.coords(title_label, title_x, title_y)

# Function to update the background image and title label position
def update_background(event):
    window_width = window.winfo_width()
    window_height = window.winfo_height()

    resized_image = original_image.resize((window_width, window_height), Image.ANTIALIAS)

    updated_image = ImageTk.PhotoImage(resized_image)
    canvas.itemconfig(background_item, image=updated_image)
    canvas.image = updated_image

    # Update the position of the title label
    title_x = window_width // 2
    title_y = int(window_height * 0.2)
    canvas.coords(title_label, title_x, title_y)

# Call the update_background function initially
update_background(None)

# Bind the update_background function to the Configure event of the window
window.bind("<Configure>", update_background)

# Create the "Create New Game" button
create_game_button = create_rounded_button(canvas, "Create New Game", create_new_game, relx=0.5, rely=0.4)

# Create the "Join Game" button
join_game_button = create_rounded_button(canvas, "Join Game", join_game, relx=0.5, rely=0.5)

# Create the "How To Play" button
how_to_play_button = create_rounded_button(canvas, "How To Play", how_to_play, relx=0.5, rely=0.6)



# Start the main loop
window.mainloop()
