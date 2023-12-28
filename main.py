import os
from tkinter import Tk, filedialog, messagebox
from tkinter import ttk
from PIL import Image

selected_image_paths = []
logo_path = ""

def select_logo():
    global logo_path
    logo_path = filedialog.askopenfilename(title="Select Logo", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    logo_name_label.config(text=f"Selected Logo: {os.path.basename(logo_path)}")

def select_images():
    global selected_image_paths
    file_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_paths:
        selected_image_paths = list(file_paths)
        display_selected_image_names()


def resize_images():
    global selected_image_paths, logo_path
    # if not logo_path:
    #     messagebox.showwarning("Warning", "Please select a logo first.")
    #     return

    if selected_image_paths:
        try:
            if logo_path != "":
                logo = Image.open(logo_path)

            for original_path in selected_image_paths:
                original_image = Image.open(original_path)
                resized_image = original_image.resize((round(
                    original_image.size[0] / original_image.size[1] * int(height_entry.get())),
                                                       int(height_entry.get())))

                output_directory = "resized_images"
                os.makedirs(output_directory, exist_ok=True)
                if logo_path != "":
                    logo_position = (resized_image.width - logo.width, resized_image.height - logo.height)
                    resized_image.paste(logo, logo_position, logo)

                resized_image_filename = f"resized_with_logo_{os.path.basename(original_path)}"
                resized_image_path = os.path.join(output_directory, resized_image_filename)
                resized_image.save(resized_image_path)

            messagebox.showinfo("Success", "Images resized successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Error resizing images: {e}")

def display_selected_image_names():
    global selected_image_paths
    image_names = [os.path.basename(path) for path in selected_image_paths]
    names_label.config(text=f"Selected Images: {', '.join(image_names)}")

window = Tk()
window.title("Image Resizer")
window.geometry("400x400")

label1 = ttk.Label(window, text='Upload files and resize them. If you want, you can add logo to')
label1.grid(row=0, column=0, columnspan=2, pady=10)

button_select = ttk.Button(window, text="Select Images", command=select_images)
button_select.grid(row=1, column=0, pady=10)

names_label = ttk.Label(window, text="Selected Images:")
names_label.grid(row=2, column=0, pady=5)

button_select_logo = ttk.Button(window, text="Select Logo", command=select_logo)
button_select_logo.grid(row=3, column=0, pady=10)

logo_name_label = ttk.Label(window, text="Selected Logo:")
logo_name_label.grid(row=4, column=0, pady=5)

height_label = ttk.Label(window, text="Desired Height:")
height_label.grid(row=5, column=0, pady=5)

height_entry = ttk.Entry(window)
height_entry.grid(row=5, column=1, pady=5)

button_resize = ttk.Button(window, text="Resize Images", command=resize_images)
button_resize.grid(row=6, column=0, pady=10)


window.mainloop()