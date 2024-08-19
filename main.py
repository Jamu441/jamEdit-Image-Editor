import ttkbootstrap as ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter
from edit_engine import editor, exporter
import random

window = ttk.Window(themename='darkly')
window.title('jamEdit')
window.geometry('1050x800')
window.resizable(False, False)
window.iconbitmap('icon.ico')


# variables
file_path = ''
cur_path = ''
w, h = '', ''
dir_str = ttk.StringVar()
edit_width = ttk.IntVar()
edit_height = ttk.IntVar()
edit_value = ttk.IntVar()
filters_dict = {'NONE': 'NONE', 'BLUR': ImageFilter.BLUR, 'CONTOUR': ImageFilter.CONTOUR, 'DETAIL': ImageFilter.DETAIL,
                'EDGE_ENHANCE': ImageFilter.EDGE_ENHANCE, 'EDGE_ENHANCE_MORE': ImageFilter.EDGE_ENHANCE_MORE,
                'EMBOSS': ImageFilter.EMBOSS, 'FIND_EDGES': ImageFilter.FIND_EDGES,
                'SHARPEN': ImageFilter.SHARPEN, 'SMOOTH': ImageFilter.SMOOTH,
                'SMOOTH_MORE': ImageFilter.SMOOTH_MORE, 'GAUSSIAN_BLUR': ImageFilter.GaussianBlur(0),
                'BOX_BLUR': ImageFilter.BoxBlur(0), 'QUANTIZE': 'QUANTIZE'}
filters_list = list(filters_dict.keys())
r = ttk.IntVar()
b = ttk.IntVar()
g = ttk.IntVar()
full_image = None


# functions
def open_image():
    global file_path, w, h, dir_str, full_image, cur_path
    file_path = filedialog.askopenfilename(filetypes=[('PNG Files', '*.png'), ('JPEG Files', '*.jpg'), ('Webp Files', '*.webp')])
    if file_path != '':
        cur_path = file_path
        dir_str.set(cur_path)
        image_label.config(image='')
        image = Image.open(cur_path)
        new_size = (int(image.width / 2.0), int(image.height / 2.0))
        resized_image = image.resize(new_size)
        full_image = resized_image
        imagetk = ImageTk.PhotoImage(full_image)
        image_label.config(image=imagetk)
        image_label.image = imagetk
        w, h = image.size
        export_button.config(state='enable')
        apply_button.config(state='enable')
        reset_button.config(state='enable')
        random_button.config(state='enable')
        edit_width.set(w)
        edit_height.set(h)
    else:
        pass


def display_edits():
    global cur_path
    global full_image
    filters_dict.update({'GAUSSIAN_BLUR': ImageFilter.GaussianBlur(edit_value.get())})
    filters_dict.update({'BOX_BLUR': ImageFilter.BoxBlur(edit_value.get())})
    edit = editor(cur_path, image_label)
    full_image = edit.edit_image(filter_options, r.get(), b.get(), g.get(), filters_dict, edit_value.get())


def reset_image():
    global full_image
    image_label.config(image='')
    image = Image.open(cur_path)
    new_size = (int(image.width / 2.0), int(image.height / 2.0))
    resized_image = image.resize(new_size)
    full_image = resized_image
    imagetk = ImageTk.PhotoImage(full_image)
    image_label.config(image=imagetk)
    image_label.image = imagetk


def randomize():
    global edit_width, edit_height, edit_value, filters_list, r, g, b
    edit_width.set(random.randint(1, 2000))
    edit_height.set(random.randint(1, 2000))
    edit_value.set(random.randint(1, 100))
    new_filter = random.choice(filters_list)
    filter_options.set(new_filter)
    r.set(random.randint(1, 255))
    g.set(random.randint(1, 255))
    b.set(random.randint(1, 255))
    display_edits()


def export():
    width = edit_width.get()
    height = edit_height.get()
    export_image = exporter(full_image, width, height)
    export_image.export_func()


# top layout
top_frame = ttk.Frame(window)
top_frame.pack()
import_button = ttk.Button(top_frame, text='Import Image', style='secondary', command=open_image)
import_button.grid(row=0, column=0, padx=5)
export_button = ttk.Button(top_frame, text='Export Image', style='secondary', state='disable', command=export)
export_button.grid(row=0, column=1)
reset_button = ttk.Button(top_frame, text='Reset Image', style='secondary', command=reset_image, state='disable')
reset_button.grid(row=0, column=2, padx=5)
random_button = ttk.Button(top_frame, text='Randomize', style='danger', command=randomize, state='disable')
random_button.grid(row=0, column=3)

# mid layout
dir_label = ttk.Label(window, textvariable=dir_str, font='Verdana 8 bold')
dir_label.pack()
image_label = ttk.Label(window, text='Import a image')
image_label.pack()

# editing layout
options_frame = ttk.Frame(window)
options_frame.pack(pady=5)
width_label = ttk.Label(options_frame, text='Width')
width_label.grid(row=0, column=0)
entry_width = ttk.Entry(options_frame, textvariable=edit_width)
entry_width.grid(row=1, column=0, padx=5)

height_label = ttk.Label(options_frame, text='Height')
height_label.grid(row=0, column=1)
entry_height = ttk.Entry(options_frame, textvariable=edit_height)
entry_height.grid(row=1, column=1)

filter_label = ttk.Label(options_frame, text='Select filter')
filter_label.grid(row=0, column=2)
value_info = ttk.Label(options_frame, text='Value')
value_info.grid(row=0, column=3)
filter_value = ttk.Entry(options_frame, textvariable=edit_value, width=10)
filter_value.grid(row=1, column=3, padx=8)
default = ttk.StringVar(value='NONE')
filter_options = ttk.Combobox(options_frame, textvariable=default, values=filters_list)
filter_options.grid(row=1, column=2, padx=5)

red_info = ttk.Label(options_frame, text='R', foreground='red')
red_info.grid(row=0, column=4)
green_info = ttk.Label(options_frame, text='B', foreground='blue')
green_info.grid(row=0, column=5)
blue_info = ttk.Label(options_frame, text='G', foreground='green')
blue_info.grid(row=0, column=6)
red_entry = ttk.Entry(options_frame, width=3, textvariable=r)
red_entry.grid(row=1, column=4)
green_entry = ttk.Entry(options_frame, width=3, textvariable=b)
green_entry.grid(row=1, column=5, padx=5)
blue_entry = ttk.Entry(options_frame, width=3, textvariable=g)
blue_entry.grid(row=1, column=6)

bottom_frame = ttk.Frame(window)
bottom_frame.pack()

apply_button = ttk.Button(bottom_frame, text='Apply', style='danger', command=display_edits, state='disable', width=30)
apply_button.pack()

# run
window.mainloop()
