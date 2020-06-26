# script for resize photos
# To compile with "pyinstaller main.py --onefile --hidden-import='PIL._tkinter_finder'"

import tkinter
import sys
import os
from tkinter import messagebox, filedialog
from PIL import ImageTk, Image

class AutoScrollbar(tkinter.Scrollbar):
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
    def __init__(self, master=None, *args, **kwargs):
        tkinter.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.master.title('Image Resizer')
        self.master.geometry('900x550')
        try:
            self.master.iconphoto(False, tkinter.PhotoImage(file='./Graphics/ico_64.png'))
        except:
            raise
            pass

        # Variables
        self.dir_var = tkinter.StringVar() # Origin directory
        self.dir_var.set(os.getcwd()) # Current directory
        self.finall_size = tkinter.StringVar()
        self.finall_size.set('500')

        self.configure(pady=3, padx=5, bg='#FFF')
        self.master.bind('<Return>', self.charge_list)

        self.create_widgets()
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.pack(fill='both', expand=1)
    def create_widgets(self):
        self.dir_btn = tkinter.Button(self, text='Search', command=self.charge_directory,
            bg='#CCC', fg='#000', bd=1, activebackground='#AAA', activeforeground='#FFF', relief='raised')
        self.dir_entry = tkinter.Entry(self, textvariable=self.dir_var, bd=0)
        self.img_label = tkinter.Label(self, text='Select an image', bg='#FFF')
        self.porc_label = tkinter.Label(self, text='Output file size (px):', bg='#FFF')
        self.porc_entry = tkinter.Entry(self, textvariable=self.finall_size, bd=0)
        self.resize_btn = tkinter.Button(self, text='Resize', command=self.func_resize,
            bg='#CCC', fg='#000', bd=1, activebackground='#AAA', activeforeground='#FFF', relief='raised')

        self.framelist = tkinter.Frame(self, bd=1)
        self.listbox = tkinter.Listbox(self.framelist, bd=0, highlightthickness=0)
        self.listbox.bind('<<ListboxSelect>>', self.charge_img)
        self.charge_list()
        self.yscroll = AutoScrollbar(self.framelist,
            bd=0,
            bg='#CCC',
            activebackground='#AAA',
            troughcolor='#FFF'
            )
        self.xscroll = AutoScrollbar(self.framelist, orient='horizontal',
            bd=0,
            bg='#CCC',
            activebackground='#AAA',
            troughcolor='#FFF'
            )
        self.listbox.configure(yscrollcommand=self.yscroll.set,
            xscrollcommand=self.xscroll.set)
        self.yscroll.configure(command=self.listbox.yview)
        self.xscroll.configure(command=self.listbox.xview)
        self.listbox.grid(column=0, row=0, sticky='nsew')
        self.yscroll.grid(column=1, row=0, sticky='ns')
        self.xscroll.grid(column=0, row=1, sticky='ew', columnspan=2)
        self.framelist.columnconfigure(0, weight=1)
        self.framelist.rowconfigure(0, weight=1)

        self.framelist.grid(column=0, row=0, columnspan=2, sticky='nsew')
        self.dir_entry.grid(column=0, row=1, sticky='we')
        self.dir_btn.grid(column=1, row=1, padx=5, pady=3)
        self.porc_label.grid(column=2, row=1, sticky='e')
        self.porc_entry.grid(column=3, row=1, sticky='we')
        self.resize_btn.grid(column=4, row=1, padx=5)
        self.img_label.grid(column=2, columnspan=3, row=0)
    def check_dir(self):
        try:
            os.mkdir(self.dir_var.get() + '/resized/')
        except FileExistsError:
            pass
    def func_resize(self):
        # implementar aqui una ventana de carga
        try:
            self.check_dir()
            if len(self.current_images) == 0: raise IndexError
            for i in self.current_images:
                img = Image.open(self.dir_var.get()+'/'+i)
                img.thumbnail((int(self.finall_size.get()),int(self.finall_size.get())), Image.ANTIALIAS)
                # implementar modulo re aqui.
                # Se debe comparar si termina con esa cadena y no si la contiene
                # Esto puede dar un error si se encuentran varias extensiones en
                # un mismo nombre
                # Se deberia comparar si:
                # "Cualquier cantidad de caracteres que termine en (extension)"
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
        if d != ():
            self.dir_var.set(d) 
            self.charge_list()
    def charge_list(self, *e):
        try:
            self.current_images = [i.name for i in os.scandir(self.dir_var.get()) if i.is_file()]
        except FileNotFoundError:
            messagebox.showerror(title='Error', message='This directory does not exist.')
            return
        self.current_images = [i for i in self.current_images \
            if i.endswith('.jpeg') or i.endswith('.jpg') or i.endswith('.png')]
        counter = 1
        self.listbox.delete(0, 'end')
        if len(self.current_images) > 0:
            for i in self.current_images:
                self.listbox.insert('end', [str(counter), i])
                counter += 1
        else:
            self.listbox.insert('end', 'Here are no Images')
    def charge_img(self, *e):
        try:
            i = (self.dir_var.get() + '/' + self.listbox.get('anchor')[1])
            global img
            img = Image.open(i)
            img.thumbnail((int(self.finall_size.get()), int(self.finall_size.get())), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.img_label.configure(text=None, image=img)
        except ValueError:
            messagebox.showerror(title='Error', message='Invalid size')
            self.finall_size.set('500')
            self.charge_img()
        except FileNotFoundError:
            pass
        except ZeroDivisionError:
            messagebox.showerror(title='Error', message='Can\'t resize by zero')
        except BaseException as err:
            # raise
            messagebox.showerror(title='Error', message=err)
            self.img_label.configure(image=None, text='Select an image')
        return 

if __name__ == '__main__':
    root = tkinter.Tk()
    app = Application(root)
    app.mainloop()