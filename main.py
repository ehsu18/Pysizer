#!/usr/bin/python3
#
# Pysizer allows you to resize a lot of images in formats jpeg, jpg or png
# To compile with:
# "pyinstaller main.py --onefile --hidden-import='PIL._tkinter_finder'"
try:
    import tkinter
    import os
    from language import *
    from tkinter import messagebox, filedialog, colorchooser
    from PIL import ImageTk, Image
except ImportError as err:
    print('Error importing modules:\n', err)
    input()
    quit()

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
        self.master.bind('<Control-d>', self.charge_directory)
        self.master.protocol('WM_DELETE_WINDOW', lambda: self.exit())
        try:  # Try config the icon
            self.icon = './Graphics/ico_64.png'
            self.master.iconphoto(False,
                                  tkinter.PhotoImage(file= self.icon))
        except:
            pass

        # Variables
        self.dir_var = tkinter.StringVar()  # Origin directory
        self.dir_var.set(os.getcwd())  # Current directory
        self.final_size = tkinter.StringVar()  # Output file size in pixels
        self.final_size.set('500')
        self.current_images = []

        self.config_file = 'config.psz'
        self.color1 = '#FFF'
        self.color2 = '#364350'
        self.color3 = '#CCC'
        self.color4 = '#000'
        self.lan = 'es'
        try:
            self.charge_config()
        except:
            self.save_config()

        # Configuring main frame
        self.configure(
            padx=0,
            pady=0,
            bg=self.color1,
            highlightthickness=0
        )
        self.create_widgets()
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.pack(fill='both', expand=1)

    def create_widgets(self):
        """Method to create the main GUI"""
        self.frame_top = tkinter.Frame(self, bd=0,
                                       bg=self.color1, height=5)
        self.frame_top.grid(row=0, sticky='nsew')

        self.frame_main = tkinter.Frame(self, bd=0,
                                        bg=self.color1)
        self.frame_main.columnconfigure(0, minsize=300)
        self.frame_main.columnconfigure(1, weight=3)
        self.frame_main.rowconfigure(0, weight=1)
        self.frame_main.grid(row=1, sticky='nsew')

        self.frame_controls = tkinter.Frame(self, bd=0,
                                            bg=self.color1)
        self.frame_controls.columnconfigure(0, weight=1)
        self.frame_controls.grid(row=2, sticky='nsew')

        self.frame_bottom = tkinter.Frame(self, bd=0,
                                          bg=self.color2, height=10)
        self.frame_bottom.grid(row=3, sticky='nsew')

        self.__create_menu()
        self.__create_buttons(self.frame_controls)
        self.__create_entrys(self.frame_controls)
        self.__create_text(self.frame_controls)
        self.__create_visor(self.frame_main)
        self.__create_list(self.frame_main)
        self.charge_list()

    def __create_menu(self):
        menu_configurations = {
            'bg': self.color2,
            'fg': self.color1,
            'bd': 0,
            'relief': 'flat',
            'activebackground': self.color1,
            'activeforeground': self.color2,
            'activeborderwidth': 0
        }
        submenu_configurations = {
            'bg': self.color1,
            'fg': self.color4,
            'bd': 0,
            'relief': 'flat',
            'activebackground': self.color3,
            'activeforeground': self.color4,
            'activeborderwidth': 0
        }

        self.menubar = tkinter.Menu(self.master, **menu_configurations)

        # Menu file
        self.menu_file = tkinter.Menu(self.menubar, tearoff=0,
                                      **submenu_configurations)  # Create button
        self.menu_file.add_command(label=t_search[self.lan],
                                   command=self.charge_directory,
                                   accelerator='Crtl+D')  # Create sub_option
        self.menubar.add_cascade(label=t_file_menu[self.lan],
                                 menu=self.menu_file)  # add to menubar

        # Menu configuration
        self.menu_config = tkinter.Menu(self.menubar, tearoff=0,
                                        **submenu_configurations)
        self.menu_config.add_command(label=t_choose_color[self.lan],
                                     command=self.change_color)
        self.menu_set_language = tkinter.Menu(self.menu_config, tearoff=0,
                                              **submenu_configurations)
        self.menu_set_language.add_command(label='English', command=lambda: self.set_language('en'))
        self.menu_set_language.add_command(label='Español', command=lambda: self.set_language('es'))
        self.menu_config.add_cascade(label=t_config_lang[self.lan],
                                     menu=self.menu_set_language)

        self.menubar.add_cascade(label=t_config[self.lan],
                                 menu=self.menu_config)

        # Menu Help
        self.menu_help = tkinter.Menu(self.menubar, tearoff=0,
                                      **submenu_configurations)
        self.menu_help.add_command(label=t_how_to[self.lan],
                                   command=self.win_help)
        self.menu_help.add_command(label=t_about[self.lan],
                                   command=self.win_about)
        self.menubar.add_cascade(label=t_help[self.lan],
                                 menu=self.menu_help)

        # Meter menu al master
        self.master.config(menu=self.menubar)

    def __create_buttons(self, master):
        configurations = {
            'bg': self.color2,
            'fg': self.color1,
            'bd': 0,
            'activebackground': self.color1,
            'activeforeground': self.color2,
            'relief': 'flat',
            'highlightbackground': self.color2,
            'highlightthickness': 1
        }
        self.btn_path = tkinter.Button(
            master,
            text=t_search[self.lan],
            command=self.charge_directory,
            **configurations
        )
        self.btn_path.grid(
            column=1,
            row=0,
            pady=5,
            sticky='w',
            padx=(5, 0)
        )

        self.btn_resize = tkinter.Button(
            master,
            text=t_resize[self.lan],
            command=self.func_resize,
            **configurations
        )
        self.btn_resize.grid(
            column=4,
            row=0,
            pady=5,
            sticky='e',
            padx=(5, 5)
        )

    def __create_entrys(self, master):
        configurations = {
            'highlightthickness': 1,
            'highlightbackground': self.color3,
            'bd': 0,
            'relief': 'flat'
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
            padx=(5, 0)
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
            padx=(2, 0)
        )

    def __create_text(self, master):
        configurations = {
            'bg': self.color1,
            'fg': self.color4
        }
        self.label_final_size = tkinter.Label(
            master,
            text=t_final_size[self.lan],
            **configurations
        )
        self.label_final_size.grid(
            column=2,
            row=0,
            sticky='e',
            padx=(10, 0)
        )

    def __create_visor(self, master):
        configurations = {
            'bg': self.color1
        }
        self.img_label = tkinter.Label(
            master,
            text=t_select_image[self.lan],
            **configurations
        )
        self.img_label.grid(
            column=1,
            row=0,
            sticky='nsew',
            padx=(5, 5)
        )

    def __create_list(self, master):
        autoscrollbar_configurations = {
            'bd': 0,
            'bg': self.color3,
            'activebackground': self.color3,
            'troughcolor': self.color1,
            'width': 10,
            'elementborderwidth': 0,
            'highlightbackground': self.color1
        }
        listbox_configurations = {
            'bg': self.color1,
            'bd': 0,
            'highlightthickness': 1,
            'highlightbackground': self.color3,
            'highlightcolor': self.color3,
            'selectforeground': self.color1,
            'selectbackground': self.color2
        }
        self.framelist = tkinter.Frame(
            master,
            bd=0,
            bg=self.color1
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
            padx=(5, 3),
            pady=(0, 3)
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

    def save_config(self):
        configurations = []
        configurations.append(self.color1 + '\n')
        configurations.append(self.color2 + '\n')
        configurations.append(self.color3 + '\n')
        configurations.append(self.color4 + '\n')
        configurations.append(self.lan + '\n')

        with open(self.config_file, 'w') as f:
            f.writelines(configurations)

    def charge_config(self):
        with open(self.config_file, 'r') as f:
            configurations = f.readlines()

        self.color1 = configurations[0][:-1]
        self.color2 = configurations[1][:-1]
        self.color3 = configurations[2][:-1]
        self.color4 = configurations[3][:-1]
        self.lan = configurations[4][:-1]

    def change_color(self):
        try:
            c = str(colorchooser.askcolor(self.color2)[1])
            if c == 'None': raise Exception
        except:
            return
        self.color2 = c
        self.create_widgets()

    def win_help(self):
        autoscrollbar_configurations = {
            'bd': 0,
            'bg': self.color3,
            'activebackground': self.color3,
            'troughcolor': self.color1,
            'width': 10,
            'elementborderwidth': 0,
            'highlightbackground': self.color1
        }
        r = tkinter.Toplevel(self.master)
        r.iconphoto(False, tkinter.PhotoImage(file=self.icon))
        r.geometry('500x500')
        t = tkinter.Text(r, bg=self.color1, bd=0)
        t.grid(column=0, row=0, sticky='nsew')
        s = AutoScrollbar(r, **autoscrollbar_configurations)
        s.grid(column=1, row=0, sticky='ns')
        r.columnconfigure(0, weight=1)
        r.rowconfigure(0, weight=1)
        t.configure(yscrollcommand=s.set)
        s.configure(command=t.yview)

        t.tag_config('title', font='Noto_Sans 20 bold', spacing3=10, foreground=self.color4)
        t.tag_config('content', font='Noto_Sans12', spacing1=5, tabs=1, foreground=self.color4)

        t.insert('end', t_how_to_title[self.lan], ('title',))
        t.insert('end', t_how_to_content[self.lan], ('content',))
        t.configure(state='disabled', wrap='word', tabs='')

    def win_about(self):
        autoscrollbar_configurations = {
            'bd': 0,
            'bg': self.color3,
            'activebackground': self.color3,
            'troughcolor': self.color1,
            'width': 10,
            'elementborderwidth': 0,
            'highlightbackground': self.color1
        }
        r = tkinter.Toplevel(self.master)
        r.iconphoto(False, tkinter.PhotoImage(file=self.icon))
        r.geometry('500x500')
        t = tkinter.Text(r, bg=self.color1, bd=0)
        t.grid(column=0, row=0, sticky='nsew')
        s = AutoScrollbar(r, **autoscrollbar_configurations)
        s.grid(column=1, row=0, sticky='ns')
        r.columnconfigure(0, weight=1)
        r.rowconfigure(0, weight=1)
        t.configure(yscrollcommand=s.set)
        s.configure(command=t.yview)

        t.tag_config('title', font='Noto_Sans 20 bold', spacing3=10, foreground=self.color4)
        t.tag_config('content', font='Noto_Sans12', spacing1=5, tabs=1, foreground=self.color4)

        t.insert('end', t_about_title[self.lan], ('title',))
        t.insert('end', t_about_content[self.lan], ('content',))
        t.configure(state='disabled', wrap='word', tabs='')

    def set_language(self, lan):
        self.lan = lan
        self.create_widgets()

    def func_resize(self):
        try:
            self.__check_dir()
            if len(self.current_images) == 0: raise IndexError
            for i in self.current_images:
                img = Image.open(self.dir_var.get() + '/' + i)
                img.thumbnail((int(self.final_size.get()),
                               int(self.final_size.get())),
                              Image.ANTIALIAS)
                if i.endswith('.jpg') or i.endswith('.jpeg'):
                    img.save(self.dir_var.get() + '/resized/' + i, 'jpeg')
                elif i.endswith('.png'):
                    img.save(self.dir_var.get() + '/resized/' + i, 'png')
                else:
                    messagebox.showerror(title=t_error[self.lan],
                                         message=i + ' Can\'t be resized')
            messagebox.showinfo(message=t_all_done[self.lan])
        except IndexError:
            messagebox.showerror(title=t_error[self.lan],
                                 message=t_no_images[self.lan])
        except ValueError:
            messagebox.showerror(title=t_error[self.lan],
                                 message=t_bad_size[self.lan])
            self.final_size.set('500')
        except FileNotFoundError:
            messagebox.showerror(title=t_error[self.lan],
                                 message=t_dir_no_exist[self.lan])
        except BaseException as err:
            messagebox.showerror(title=t_error[self.lan],
                                 message=err)

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
            messagebox.showerror(title=t_error[self.lan],
                                 message=t_dir_no_exist[self.lan])
            self.current_images = []
        except BaseException as err:
            messagebox.showerror(title=t_error[self.lan],
                                 message=err)
            self.current_images = []
        finally:
            self.charge_listbox()

    def charge_listbox(self):
        self.listbox.delete(0, 'end')
        if len(self.current_images) == 0:
            self.listbox.insert('end', t_no_images[self.lan])
            self.charge_img()
            return
        for i in self.current_images:
            self.listbox.insert('end', i)

    def charge_img(self, *e):
        if self.current_images == []:
            self.__create_visor(self.frame_main)
            return
        try:
            if int(self.final_size.get()) < 1: raise ValueError
            global img
            img = self.listbox.get('anchor')
            img = Image.open(self.dir_var.get() + '/' + img)
            img.thumbnail(
                (int(self.final_size.get()), int(self.final_size.get())),
                1)
            img = ImageTk.PhotoImage(img)
            self.img_label.configure(text=None, image=img)
        except FileNotFoundError:
            self.charge_list()
        except ValueError:
            messagebox.showerror(message=t_bad_size[self.lan])
            self.final_size.set('500')
        except IsADirectoryError:
            pass
        except BaseException as err:
            messagebox.showerror(message=err)

    def exit(self):
        self.save_config()
        self.quit()

if __name__ == '__main__':
    root = tkinter.Tk()
    app = Application(root)
    app.mainloop()
