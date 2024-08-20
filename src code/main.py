import ttkbootstrap as ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter
from edit_engine import Editor, Exporter
import random

window = ttk.Window(themename='darkly')
window.title('jamEdit')
window.geometry('1050x800')
window.iconbitmap('icon.ico')

# variables
file_path = ''
cur_path = ''
w, h = 0, 0
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
alpha_value = ttk.DoubleVar()
screen_size_width = window.winfo_screenwidth()
screen_size_height = window.winfo_screenheight()
small_window = False
error_msg = ttk.StringVar()
r_click = False
max_width_big = 900
max_height_big = 550
max_width_small = 500
max_height_small = 250

if screen_size_width < 1600 and screen_size_height < 900:
    window.geometry('800x600')
    small_window = True


# functions
def open_image():
    global file_path, w, h, dir_str, full_image, cur_path, max_width_big, max_height_big
    file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png *.jpg *.webp')])
    if file_path != '':
        cur_path = file_path
        dir_str.set(cur_path)
        image_label.config(image='')
        image = Image.open(cur_path)
        if not small_window:
            w, h = image.size
            if w / 2.0 > max_width_big or h / 2.0 > max_height_big:
                new_size = (max_width_big, max_height_big)
            else:
                new_size = (int(w / 2.0), int(h / 2.0))
        else:
            w, h = image.size
            if w / 4.0 > max_width_small or h / 4.0 > max_height_small:
                new_size = (max_width_small, max_height_small)
            else:
                new_size = (int(w / 4.0), int(h / 4.0))
        resized_image = image.resize(new_size)
        full_image = resized_image
        imagetk = ImageTk.PhotoImage(full_image)
        image_label.config(image=imagetk)
        image_label.image = imagetk
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
    if edit_value.get() < 0:
        edit_value.set(0)
    filters_dict.update({'GAUSSIAN_BLUR': ImageFilter.GaussianBlur(edit_value.get())})
    filters_dict.update({'BOX_BLUR': ImageFilter.BoxBlur(edit_value.get())})
    edit = Editor(cur_path, image_label)
    full_image = edit.edit_image(filter_options, r.get(), b.get(), g.get(), filters_dict,
                                 edit_value.get(), alpha_value.get(), small_window, error_msg)


def reset_image():
    global full_image, w, h
    image_label.config(image='')
    image = Image.open(cur_path)
    if not small_window:
        w, h = image.size
        if w / 2.0 > max_width_big or h / 2.0 > max_height_big:
            new_size = (max_width_big, max_height_big)
            print(new_size)
        else:
            new_size = (int(w / 2.0), int(h / 2.0))
            print(new_size)
    else:
        w, h = image.size
        if w / 4.0 > max_width_small or h / 4.0 > max_height_small:
            new_size = (max_width_small, max_height_small)
            print(new_size)
        else:
            new_size = (int(w / 4.0), int(h / 4.0))
            print(new_size)
    edit_width.set(image.width)
    edit_height.set(image.height)
    filter_options.set('NONE')
    edit_value.set(value=0)
    r.set(value=0)
    g.set(value=0)
    b.set(value=0)
    alpha_value.set(value=0)
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
    alpha_value.set(round(random.uniform(0, 5), 2))
    display_edits()


def export():
    global full_image
    width = edit_width.get()
    height = edit_height.get()
    export_image = Exporter(full_image, width, height)
    export_image.export_func()


def r_click_menu(event):
    global r_click
    if not r_click:
        r_click = True
        info_label = ttk.Button(window, text='Reset Size', style='danger', command=lambda: reset_size(info_label))
        info_label.place(x=window.winfo_pointerx() - window.winfo_rootx(),
                         y=window.winfo_pointery() - window.winfo_rooty())


def reset_size(widget):
    global r_click
    r_click = False
    widget.destroy()
    if w and h > 0:
        edit_width.set(w)
        edit_height.set(h)


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
entry_width = ttk.Entry(options_frame, textvariable=edit_width, style='secondary')
entry_width.grid(row=1, column=0, padx=5)

height_label = ttk.Label(options_frame, text='Height')
height_label.grid(row=0, column=1)
entry_height = ttk.Entry(options_frame, textvariable=edit_height, style='secondary')
entry_height.grid(row=1, column=1)

filter_label = ttk.Label(options_frame, text='Select filter')
filter_label.grid(row=0, column=2)
value_info = ttk.Label(options_frame, text='Value')
value_info.grid(row=0, column=3)
filter_value = ttk.Entry(options_frame, textvariable=edit_value, width=10, style='secondary')
filter_value.grid(row=1, column=3, padx=8)
default = ttk.StringVar(value='NONE')
filter_options = ttk.Combobox(options_frame, textvariable=default, values=filters_list, style='secondary')
filter_options.grid(row=1, column=2, padx=5)

red_info = ttk.Label(options_frame, text='R', foreground='red')
red_info.grid(row=0, column=4)
green_info = ttk.Label(options_frame, text='B', foreground='blue')
green_info.grid(row=0, column=5)
blue_info = ttk.Label(options_frame, text='G', foreground='green')
blue_info.grid(row=0, column=6)
red_entry = ttk.Entry(options_frame, width=3, textvariable=r, style='secondary')
red_entry.grid(row=1, column=4)
green_entry = ttk.Entry(options_frame, width=3, textvariable=b, style='secondary')
green_entry.grid(row=1, column=5, padx=5)
blue_entry = ttk.Entry(options_frame, width=3, textvariable=g, style='secondary')
blue_entry.grid(row=1, column=6)

alpha_info = ttk.Label(options_frame, text='Alpha')
alpha_info.grid(row=2, column=5)
alpha_entry = ttk.Entry(options_frame, width=4, textvariable=alpha_value, style='secondary')
alpha_entry.grid(row=3, column=5)

bottom_frame = ttk.Frame(window)
bottom_frame.pack()

error_label = ttk.Label(bottom_frame, textvariable=error_msg, font='Verdana 9 bold', foreground='pink')
error_label.pack(pady=5)
apply_button = ttk.Button(bottom_frame, text='Apply', style='danger', command=display_edits, state='disable', width=30)
apply_button.pack()

# events

entry_width.bind('<Button-3>', r_click_menu)
entry_height.bind('<Button-3>', r_click_menu)

# run
window.mainloop()
