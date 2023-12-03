from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont
import os


main_path = str()
water_mark_path = str()

# ************************ Functions ***********************************


# Checking if user is selecting image path or not
def is_valid_image_path(path):
    valid_extensions = {".png", ".jpg", ".jpeg", ".gif"}  # Add or remove extensions as needed
    _, file_extension = os.path.splitext(path)
    return file_extension.lower() in valid_extensions


def save_image(img):
    # Ask the user for the file path to save
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"), ("All files", "*.*")])

    # Check if the user selected a file
    if file_path:
        # Save the image to the selected file path
        img.save(file_path)
        messagebox.showinfo("Saved", f"Image saved to {file_path}")


def browse_file():
    global main_path
    # using filedialog for user to select the path using gui
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        entry_var.set(file_path)
        main_path = path_entry.get()


def watermark_file():
    global water_mark_path
    # getting path of the watermarking image using filedialog
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        watermark_var.set(file_path)
        water_mark_path = watermark_entry.get()


def add_watermark():
    # checking is main path(image path) empty or not
    if main_path:
        # Opening the main image
        bg_image = Image.open(main_path)
        bg_size = bg_image.size
        # Setting position yo add watermark
        position = (int(bg_size[0] / 100 * 10), int(bg_size[1] / 100 * 10))
        # Checking watermark is image or text
        if is_valid_image_path(watermark_entry.get()):
            # adding image as watermark
            size = (int(bg_size[0] / 100 * 15), int(bg_size[1] / 100 * 15))
            watermark_image = Image.open(water_mark_path)
            watermark_image.thumbnail(size=size)
            bg_image.paste(watermark_image, position)
            save_image(bg_image)
            reset()
        else:
            # Adding text as watermark
            draw = ImageDraw.Draw(bg_image)
            text = watermark_entry.get()
            font = ImageFont.truetype(r'C:\Users\System-Pc\Desktop\arial.ttf', 26)
            draw.text(position, text, fill=(0, 0, 0), font=font)
            save_image(bg_image)
            reset()
    # showing message if main image is not selected
    else:
        messagebox.showwarning("Empty Field", "Please add a Image path")


def reset():
    # clearing the entry field and main path
    global main_path
    path_entry.delete(0, END)
    watermark_entry.delete(0, END)
    main_path = ""


# ******************************************************************************

# creating Tkinter window
window = Tk()
window.title("Watermark Adder")
window.geometry("600x450")

entry_var = StringVar()
watermark_var = StringVar()

bg_img = PhotoImage(file="./download.png")

# Creating canvas and showing image
canvas = Canvas(window, width=225, height=225)
canvas.create_image(0, 0, anchor=NW, image=bg_img)
canvas.grid(column=2, row=1, pady=(40, 20))

# labels
label_1 = Label(window, text="Image path:", font=("Arial", 13, "normal"))
label_1.grid(column=1, row=2, padx=(90, 10), sticky="e", pady=1)

label_2 = Label(window, text="Watermark:", font=("Arial", 13, "normal"))
label_2.grid(column=1, row=3, padx=(90, 10), sticky="e", pady=1)

# Entries
path_entry = Entry(window, textvariable=entry_var, width=40)
path_entry.grid(column=2, row=2, sticky="ew", pady=1)

watermark_entry = Entry(window, textvariable=watermark_var, width=40)
watermark_entry.grid(column=2, row=3, sticky="ew", pady=1)

# Buttons
browse_button = Button(window, text="Browse", command=browse_file)
browse_button.grid(column=3, row=2, padx=(10, 10))

watermark_browse_button = Button(window, text="Browse", command=watermark_file)
watermark_browse_button.grid(column=3, row=3, padx=(10, 10))

submit_button = Button(window, text="Save", command=add_watermark)
submit_button.grid(column=2, row=4, pady=15, sticky="w", ipadx=20)

reset_button = Button(window, text="Reset", command=reset)
reset_button.grid(column=2, row=4, pady=15, sticky="e", ipadx=20)


window.mainloop()
