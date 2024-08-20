from tkinter import filedialog
from PIL import Image, ImageTk

max_width_big = 900
max_height_big = 550
max_width_small = 500
max_height_small = 250


class Editor:

    def __init__(self, path, widget):
        self.path = path
        self.widget = widget
        self.image = None

    def edit_image(self, filter_option, r, b, g, filters, value, alpha, small_window, error):
        filter_selected = filter_option.get()
        self.widget.config(image='')
        image = Image.open(self.path)
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
        converted_image = resized_image.convert('RGBA')
        if filter_selected == 'NONE':
            error.set('')
            color_filter = Image.new('RGBA', new_size, (r, g, b))
            full_image = Image.blend(converted_image, color_filter, alpha)
            imagetk = ImageTk.PhotoImage(full_image)
            self.image = full_image
            self.widget.config(image=imagetk)
            self.widget.image = imagetk
        elif filter_selected == 'QUANTIZE' and value > 0:
            error.set('')
            color_filter = Image.new('RGBA', new_size, (r, g, b))
            full_image = Image.blend(converted_image, color_filter, alpha)
            effected_image = full_image.quantize(value)
            self.image = effected_image
            imagetk = ImageTk.PhotoImage(effected_image)
            self.widget.config(image=imagetk)
            self.widget.image = imagetk
        elif filter_selected != 'NONE' and filter_selected != 'QUANTIZE':
            error.set('')
            new_image = converted_image.filter(filters.get(filter_option.get()))
            color_filter = Image.new('RGBA', new_size, (r, g, b))
            full_image = Image.blend(new_image, color_filter, alpha)
            self.image = full_image
            imagetk = ImageTk.PhotoImage(full_image)
            self.widget.config(image=imagetk)
            self.widget.image = imagetk
        elif filter_selected == 'QUANTIZE' and value <= 0:
            error.set(f'Error applying {filter_selected}, value cannot be {value}')
            imagetk = ImageTk.PhotoImage(converted_image)
            self.widget.config(image=imagetk)
            self.widget.image = imagetk
        else:
            error.set(f'Error applying {filter_selected}, unknown error.')
            imagetk = ImageTk.PhotoImage(converted_image)
            self.widget.config(image=imagetk)
            self.widget.image = imagetk
        return self.image


class Exporter:

    def __init__(self, image, width, height):
        self.image = image
        self.width = width
        self.height = height

    def export_func(self):
        size = (self.width, self.height)
        if self.image:
            full_image = self.image.resize(size)
            file_save_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG Files',
                                                                                               '*.png *.jpg')])
            if file_save_path:
                full_image.save(file_save_path)
