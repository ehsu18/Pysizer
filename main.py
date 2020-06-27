#!/usr/bin/python3
#
# Pysizer allows you to resize a lot of images in formats jpeg, jpg or png
# To compile with:
# "pyinstaller main.py --onefile --hidden-import='PIL._tkinter_finder'"
try:
    import tkinter
    import os
    from tkinter import messagebox, filedialog
    from PIL import ImageTk, Image
except ImportError as err:
    raise

class AutoScrollbar(tkinter.Scrollbar):
    """A class that inherits from Scrollbar for make it auto-hiding

    Source:
    http://effbot.org/zone/tkinter-autoscrollbar.htm
    """
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        tkinter.Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise tkinter.TclError
    def place(self, **kw):
        raise tkinter.TclError

class Application(tkinter.Frame):
    """Main class of the application"""
    def __init__(self, master=None, *args, **kwargs):
        """Here are defined the variables, geometry's and others"""

        # Configuring Master
        tkinter.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.master.title('Pysizer')
        self.master.geometry('900x600')
        try: # Try config the icon
            self.master.iconphoto(False,
                tkinter.PhotoImage(file='./Graphics/ico_64.png'))
        except:
            pass

        # Variables
        self.dir_var = tkinter.StringVar() # Origin directory
        # try with:  os.get_exec_path()
        self.dir_var.set(os.getcwd()) # Current directory
        self.final_size = tkinter.StringVar() # Output file size in pixels
        self.final_size.set('500')
        self.current_images = []

        # Constants will be here (Icon Directory, Language sheet, etc)

        # Configuring main frame
        self.configure(
            padx=0,
            pady=0,
            bg='#FFF',
            highlightthickness=0
            )
        self.create_widgets()
        self.charge_list()
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.pack(fill='both', expand=1)

    def create_widgets(self):
        """Method to create the main GUI"""
        self.frame_top = tkinter.Frame(self, bd=0, bg='#FFF', height=5)
        self.frame_top.grid(row=0, sticky='nsew')

        self.frame_main = tkinter.Frame(self, bd=0, bg='#FFF')
        self.frame_main.columnconfigure(0, minsize=300)
        self.frame_main.columnconfigure(1, weight=3)
        self.frame_main.rowconfigure(0, weight=1)
        self.frame_main.grid(row=1, sticky='nsew')

        self.frame_controls = tkinter.Frame(self, bd=0, bg='#FFF')
        self.frame_controls.columnconfigure(0, weight=1)
        self.frame_controls.grid(row=2, sticky='nsew')

        self.frame_bottom = tkinter.Frame(self, bd=0, bg='#28F', height=10)
        self.frame_bottom.grid(row=3, sticky='nsew')

        self.__create_buttons(self.frame_controls)
        self.__create_entrys(self.frame_controls)
        self.__create_text(self.frame_controls)
        self.__create_visor(self.frame_main)
        self.__create_list(self.frame_main)

    def __create_buttons(self, master):
        configurations = {
            'bg':'#28F',
            'fg':'#FFF',
            'bd':0,
            'activebackground':'#FFF',
            'activeforeground':'#28F',
            'relief':'flat',
            'highlightbackground':'#28F',
            'highlightthickness':1
            }
        self.btn_path = tkinter.Button(
            master,
            text='Search',
            command=self.charge_directory,
            **configurations
            )
        self.btn_path.grid(
            column=1,
            row=0,
            pady=5,
            sticky='w',
            padx=(5,0)
            )

        self.btn_resize = tkinter.Button(
            master,
            text='Resize',
            command=self.func_resize,
            **configurations
            )
        self.btn_resize.grid(
            column=4,
            row=0,
            pady=5,
            sticky='e',
            padx=(5,5)
            )

    def __create_entrys(self, master):
        configurations = {
            'highlightthickness':1,
            'highlightbackground':'#CCC',
            'bd':0,
            'relief':'flat'
            }
        self.entry_path = tkinter.Entry(
            master,
            textvariable=self.dir_var,
            **configurations
            )
        self.entry_path.bind('<Return>', self.charge_list)
        self.entry_path.bind('<Key-KP_Enter>', self.charge_list)
        self.entry_path.grid(
            column=0,
            row=0,
            sticky='nsew',
            pady=5,
            padx=(5,0)
            )

        self.entry_final_size = tkinter.Entry(
            master,
            width=5,
            textvariable=self.final_size,
            **configurations
            )
        self.entry_final_size.bind('<Return>', self.charge_img)
        self.entry_final_size.bind('<Key-KP_Enter>', self.charge_img)
        self.entry_final_size.grid(
            column=3,
            row=0,
            sticky='nsew',
            pady=5,
            padx=(2,0)
            )

    def __create_text(self, master):
        configurations = {
            'bg':'#FFF'
            }
        self.label_final_size = tkinter.Label(
            master,
            text='Output file size (px):',
            **configurations
            )
        self.label_final_size.grid(
            column=2,
            row=0,
            sticky='e',
            padx=(10,0)
            )

    def __create_visor(self, master):
        configurations = {
            'bg':'#FFF'
            }
        self.img_label = tkinter.Label(
            master,
            text='Select an image',
            **configurations
            )
        self.img_label.grid(
            column=1,
            row=0,
            sticky='nsew',
            padx=(5,5)
            )

    def __create_list(self, master):
        autoscrollbar_configurations = {
            'bd':0,
            'bg':'#CCC',
            'activebackground':'#CCC',
            'troughcolor':'#FFF',
            'width':10,
            'elementborderwidth':0,
            'highlightbackground':'#F00'
            }
        listbox_configurations = {
            'bg':'#FFF',
            'fg':'#000',
            'bd':0,
            'highlightthickness':1,
            'highlightbackground':'#CCC',
            'highlightcolor':'#CCC',
            'selectforeground':'#FFF',
            'selectbackground':'#28F'
            }
        self.framelist = tkinter.Frame(
            master,
            bd=0,
            bg='#FFF'
            )
        self.framelist.columnconfigure(0, weight=1)
        self.framelist.rowconfigure(0, weight=1)
        self.framelist.grid(
            column=0,
            row=0,
            sticky='nsew'
            )

        self.listbox = tkinter.Listbox(
            self.framelist,
            **listbox_configurations
            )
        self.listbox.grid(
            column=0,
            row=0,
            sticky='nsew',
            padx=(5,3),
            pady=(0,3)
            )
        self.yscroll = AutoScrollbar(
            self.framelist,
            **autoscrollbar_configurations
            )
        self.yscroll.grid(
            column=1,
            row=0,
            sticky='ns',
            )
        self.xscroll = AutoScrollbar(self.framelist,
            orient='horizontal',
            **autoscrollbar_configurations
            )
        self.xscroll.grid(
            column=0,
            row=1,
            sticky='ew',
            columnspan=2
            )

        self.listbox.bind('<<ListboxSelect>>', self.charge_img)
        self.listbox.configure(yscrollcommand=self.yscroll.set,
            xscrollcommand=self.xscroll.set)
        self.yscroll.configure(command=self.listbox.yview)
        self.xscroll.configure(command=self.listbox.xview)

    def __check_dir(self):
        try:
            os.mkdir(self.dir_var.get() + '/resized/')
        except FileExistsError:
            pass

    def func_resize(self):
        try:
            self.__check_dir()
            if len(self.current_images) == 0: raise IndexError
            for i in self.current_images:
                img = Image.open(self.dir_var.get()+'/'+i)
                img.thumbnail((int(self.final_size.get()),int(self.final_size.get())), Image.ANTIALIAS)
                if i.endswith('.jpg') or i.endswith('.jpeg'):
                    img.save(self.dir_var.get() + '/resized/'+i, 'jpeg')
                elif i.endswith('.png'):
                    img.save(self.dir_var.get() + '/resized/'+i, 'png')
                else:
                    messagebox.showerror(title='Problem with an file', message=i+' Can\'t be resized')
            messagebox.showinfo(title='All done', message='Images resized successfully')
        except IndexError:
            messagebox.showerror(title='Error', message='Here are no images')
        except ValueError:
            messagebox.showerror(title='Error', message='Bad size')
            self.finall_size.set('500')
        except FileNotFoundError:
            messagebox.showerror(title='Error', message='This directory does not exist.')
            return
        except BaseException as err:
            messagebox.showerror(message=err)
            raise
        finally:
            pass

    def charge_directory(self, *e):
        d = filedialog.askdirectory()
        if len(d) != 0:
            self.dir_var.set(d)
            self.charge_list()

    def charge_list(self, *e):
        try:
            self.current_images = [i.name
                for i in os.scandir(self.dir_var.get())
                if i.is_file()
                if i.name.endswith('.jpg') or
                i.name.endswith('.jpeg') or
                i.name.endswith('.png')
                ]
        except FileNotFoundError:
            messagebox.showerror(message='This directory doesn\'t exist')
            self.current_images = []
        except BaseException as err:
            messagebox.showerror(message=err)
            self.current_images = []
        finally:
            self.charge_listbox()

    def charge_listbox(self):
        self.listbox.delete(0,'end')
        if len(self.current_images) == 0:
            self.listbox.insert('end','Here are no images')
            self.charge_img()
            return
        for i in self.current_images:
            self.listbox.insert('end', i)


    def charge_img(self, *e):
        if self.current_images == []:
            self.__create_visor(self.frame_main)
            return
        try:
            global img
            img = self.listbox.get('anchor')
            img = Image.open(self.dir_var.get() + '/' + img)
            img.thumbnail(
                (int(self.final_size.get()),int(self.final_size.get())),
                1)
            img = ImageTk.PhotoImage(img)
            self.img_label.configure(text=None, image=img)
        except FileNotFoundError:
            self.charge_list()

if __name__ == '__main__':
    root = tkinter.Tk()
    app = Application(root)
    app.mainloop()
