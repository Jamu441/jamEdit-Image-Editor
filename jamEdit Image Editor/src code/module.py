from tkinter import filedialog
from PIL import Image, ImageTk


class editor:

    def __init__(self, path, widget):
        self.path = path
        self.widget = widget
        self.image = None

    def edit_image(self, filter_option, r, b, g, filters, value):
        filter_selected = filter_option.get()
        self.widget.config(image='')
        image = Image.open(self.path)
        new_size = (int(image.width / 2.0), int(image.height / 2.0))
        resized_image = image.resize(new_size)
        converted_image = resized_image.convert('RGB')
        if filter_selected == 'NONE':
            imagetk = ImageTk.PhotoImage(converted_image)
            self.image = converted_image
            self.widget.config(image=imagetk)
            self.widget.image = imagetk
        elif filter_selected == 'QUANTIZE':
            color_filter = Image.new('RGB', new_size, (r, g, b))
            full_image = Image.blend(converted_image, color_filter, 0.5)
            effected_image = full_image.quantize(value)
            self.image = effected_image
            imagetk = ImageTk.PhotoImage(effected_image)
            self.widget.config(image=imagetk)
            self.widget.image = imagetk
        elif filter_selected != 'NONE' and filter_option.get() in list(filters.keys()):
            new_image = converted_image.filter(filters.get(filter_option.get()))
            color_filter = Image.new('RGB', new_size, (r, g, b))
            full_image = Image.blend(new_image, color_filter, 0.5)
            self.image = full_image
            imagetk = ImageTk.PhotoImage(full_image)
            self.widget.config(image=imagetk)
            self.widget.image = imagetk
        else:
            print(f'No filter of {filter_selected} found.')
            imagetk = ImageTk.PhotoImage(converted_image)
            self.widget.config(image=imagetk)
            self.widget.image = imagetk
        return self.image


class exporter:

    def __init__(self, image, width, height):
        self.image = image
        self.width = width
        self.height = height

    def export_func(self):
        size = (self.width, self.height)
        if self.image:
            full_image = self.image.resize(size)
            file_save_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG Files', '*.png'), ('JPEG Files', '*.jpg')])
            if file_save_path:
                full_image.save(file_save_path)
