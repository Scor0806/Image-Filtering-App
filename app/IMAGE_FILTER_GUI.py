#   IMAGE FILTER GUI

import tkinter.font as font
import os

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from Filter import Olympic
from Filter import BasicFilter
from skimage import io, color
from PIL import Image, ImageTk
from datetime import datetime


#   16:9 ratios:: 1024x576, 1152x648, 1280x720, 1366x768, 1600x900, 1920x1080


class Application(Tk):

    def __init__(self):
        global is_low_frequency
        super(Application, self).__init__()

        base_folder = os.path.dirname(__file__)
        image_path = os.path.join(base_folder, 'icon5.gif')

        #   SETTING UP MAIN CANVAS
        self.title("Photo Filter App")
        self.minsize(1024, 576)
        self.geometry("1024x576")
        img = PhotoImage(file=image_path)
        self.iconphoto(True, img)
        canvas = Canvas(self)
        canvas.pack()

        self.fontSize = font.Font(size=25)

        #   QUADRANT OF FRAME PLACEMENT
        self.frame_q1 = Frame(self, bg='#202020')
        self.frame_q1.place(relx=.66, rely=0, relwidth=.33, relheight=.80)

        self.frame_q2 = Frame(self, bg='#202020')
        self.frame_q2.place(relx=0, rely=0, relwidth=0.33, relheight=0.80)

        self.frame_q4 = Frame(self, bg='#505050')
        self.frame_q4.place(relx=0, rely=.8, relwidth=1, relheight=0.20)

        #   CANVAS IMAGE PLACEMENT
        self.img_canvas_q2 = Canvas(self.frame_q2, bg='black')
        self.img_canvas_q2.place(relx=0, rely=0.1, relwidth=1, relheight=0.90)

        self.img_canvas_q1 = Canvas(self.frame_q1, bg='black')
        self.img_canvas_q1.place(relx=0, rely=0.1, relwidth=1, relheight=0.90)

        #   CONTAINER WHERE FRAMES ARE STACKED AND SHOWN BASED ON COMBOBOX OPTION
        middle_container = Frame(self)
        middle_container.place(relx=.33, rely=.0, relwidth=0.33, relheight=0.80)

        #   FRAME QUADRANT 1 BUTTONS AND TOOLS
        self.applybuttonImg = Image.open('apply_button.png')
        self.applybuttonImg = self.applybuttonImg.resize((75, 25), Image.ANTIALIAS)
        self.applybuttonImg = ImageTk.PhotoImage(self.applybuttonImg)
        self.filter_combo()
        self.select_filter_btn = Button(self.frame_q1, image=self.applybuttonImg, bg='#202020',
                                        command=self.options_select).grid(row=0, column=1)

        #   FRAME QUADRANT 2 BUTTONS AND TOOLS
        self.upload_button = Image.open('upload_2.png')
        self.upload_button = self.upload_button.resize((200, 35), Image.ANTIALIAS)
        self.buttonImg = ImageTk.PhotoImage(self.upload_button)

        self.upload_button = Button(self.frame_q2, image=self.buttonImg, bg='#202020', command=self.fileDialog) \
            .pack(side='top')

        #   FRAME QUADRANT 4 BUTTONS AND TOOLS

        #   MIDDLE FRAME BUTTONS AND TOOLS
        self.frames = {}
        for F in (SelectFilterPage, ButterworthPage, GaussianPage, OlympicPage, HomomorphicPage, IdealPage):
            page_name = F.__name__
            frame = F(parent=middle_container, controller=self)
            self.frames[page_name] = frame

            #   PLACE ALL PAGES IN SAME LOCATION
            frame.grid(row=0, column=1, sticky="nsew")
            if page_name != 'SelectFilterPage':
                self.apply_filter_btn = Button(self.frames[page_name], image=self.applybuttonImg, bg='#202020',
                                               command=self.filter).grid(row=8, column=0, sticky='w')

        self.show_frame("SelectFilterPage")

    def show_frame(self, page_name):
        '''Show frame for the given page name'''

        frame = self.frames[page_name]
        frame.tkraise()

    #   QUADRANT 1 COMBOBOX FUNCTION
    def filter_combo(self):
        self.box_value = StringVar()
        self.box = ttk.Combobox(self.frame_q1, textvariable=self.box_value, width=30, state='readonly',
                                justify='center')
        self.box['values'] = ("SELECT FILTER", "Butterworth", "Gaussian", "Olympic", "Homomorphic", "Ideal")
        self.box.grid(row=0, column=0)
        self.box.current(0)

    #   PRINT FILTER COMBOBOX VALUE
    def options_select(self):
        #   Print to Console for Debugging
        print(self.box_value.get())

        self.show_frame(self.box_value.get() + "Page")

    #   OPEN FILE DIALOG TO UPLOAD IMAGE
    def fileDialog(self):
        global new_img_gray

        self.filename = filedialog.askopenfilename(initialdir='/', title='Select A File',
                                                   filetypes=(("jpeg", "*.jpg"), ("All Files", "*.*")))
        img_color = io.imread(self.filename)
        self.img_gray = color.rgb2gray(img_color)
        new_img_gray = self.img_gray

        output_dir = 'output/'
        image_name = self.filename.split(".")
        # output_image_name = output_dir + "filtered_image_" + datetime.now().strftime("%m%d-%H%M%S") + ".jpg"
        self.img_canvas_q2.image = ImageTk.PhotoImage(image=Image.fromarray(self.img_gray))
        self.img_canvas_q2.create_image(0, 0, image=self.img_canvas_q2.image, anchor='nw')

    def filter(self):
        #   Grab current Frame value from Combobox value if value is not SELECT FILTER
        print("Inside filter function but not inside if statement")

        if self.box_value.get() != "SELECT FILTER":
            print("filter function inside if statement is a hit!")
            frame = self.frames[self.box_value.get() + "Page"]

            #   Apply filter from user selection
            filtered_img = frame.apply_filter(new_img_gray)

            #   Convert and store image in variable
            self.img_canvas_q1.image = ImageTk.PhotoImage(image=Image.fromarray(filtered_img))

            #   Anchor image in Q1 Frame
            self.img_canvas_q1.create_image(0, 0, image=self.img_canvas_q1.image, anchor='nw')

            self.evaluation(frame.is_low_frequency())

    def evaluation(self, low_frequency):
        img = new_img_gray

        if low_frequency:
            gaussian_low_class = BasicFilter.Filtering(img, 'gaussian_l', 100)
            butterworth_low_class = BasicFilter.Filtering(img, 'butterworth_l', 100, 2)
            ideal_low_class = BasicFilter.Filtering(img, 'ideal_l', 100)

            g_filter = gaussian_low_class.filtering()
            b_filter = butterworth_low_class.filtering()
            i_filter = ideal_low_class.filtering()

            print("----------- EXECUTING-1 ------------")
            psnr_1 = BasicFilter.PSNR(img, g_filter)
            psnr_2 = BasicFilter.PSNR(img, b_filter)
            psnr_3 = BasicFilter.PSNR(img, i_filter)

            print(psnr_1)
            print(psnr_2)
            print(psnr_3)

        else:
            gaussian_high_class = BasicFilter.Filtering(img, 'gaussian_l', 100)
            butterworth_high_class = BasicFilter.Filtering(img, 'butterworth_l', 100, 2)
            ideal_high_class = BasicFilter.Filtering(img, 'ideal_l', 100)

            g_filter = gaussian_high_class.filtering()
            b_filter = butterworth_high_class.filtering()
            i_filter = ideal_high_class.filtering()

            print("----------- EXECUTING-2 ------------")
            psnr_1 = BasicFilter.PSNR(img, g_filter)
            psnr_2 = BasicFilter.PSNR(img, b_filter)
            psnr_3 = BasicFilter.PSNR(img, i_filter)

            print(psnr_1)
            print(psnr_2)
            print(psnr_3)


#   DEFAULT PAGE IN MIDDLE FRAME
class SelectFilterPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label1 = Label(self, text="\nFREQUENCY FILTERING\n", font=("Apple Chancery", 18), wraplength=300, padx=30,
                       justify=LEFT)
        label1.grid(row=0, column=0, sticky='n')
        label2 = Label(self, text="1.Please upload the picture \n 2.Choose the filter \n 3.click on apply",
                       font=("Helvetica", 16), wraplength=300,
                       justify=LEFT)
        label2.grid(row=1, column=0)


#   PAGE IN MIDDLE FRAME
class ButterworthPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.radValue = StringVar()
        self.cutoffValue = IntVar()
        self.orderValue = IntVar()

        label = Label(self, text="\nBUTTERWORTH FILTER OPTIONS\n", font=("Apple Chancery", 20), wraplength=300, padx=15,
                      justify=LEFT)
        label.grid(row=0, columnspan=2, sticky='n')

        bw_low = Radiobutton(self, text='Low Frequency', value='butterworth_l', variable=self.radValue)
        bw_high = Radiobutton(self, text='High Frequency', value='butterworth_h', variable=self.radValue)

        bw_low.grid(row=2, columnspan=2, sticky='w')
        bw_high.grid(row=3, columnspan=2, sticky='w')

        label_cutoff = Label(self, text='Select Cutoff:',
                             font=font.Font(size=18), wraplength=200,
                             justify=RIGHT)
        label_cutoff.grid(row=4, column=0, sticky='w')

        cutoff_slider = Scale(self, from_=50, to=150, orient=HORIZONTAL, variable=self.cutoffValue)
        cutoff_slider.grid(row=4, column=1, columnspan=2, sticky='w')

        label_order = Label(self, text='Order:', font=font.Font(size=18), wraplength=200, justify=RIGHT)
        label_order.grid(row='6', column=0, sticky='w')

        order_slider = Scale(self, from_=0, to=10, orient=HORIZONTAL, variable=self.orderValue)
        order_slider.grid(row=6, column=1, columnspan=2, sticky='w')

    def apply_filter(self, image):
        print("apply_filter function hit!")
        cutoff_selected = self.cutoffValue.get()
        order_selected = self.orderValue.get()
        return self.butterworth(image, cutoff_selected, order_selected)

    def butterworth(self, image, cutoff, order):
        print("butterworth function hit!")
        self.rad_selected = self.radValue.get()

        butterworth = BasicFilter.Filtering(image, self.rad_selected, cutoff, order)
        output = butterworth.filtering()
        return output

    def is_low_frequency(self):
        frequency = self.rad_selected
        if frequency == 'butterworth_l':
            return True
        else:
            return False


# PAGE IN MIDDLE FRAME
class GaussianPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.radValue = StringVar()
        self.sliderValue = IntVar()

        label = Label(self, text="\nGAUSSIAN FILTER\n OPTIONS\n", font=("Apple Chancery", 20), wraplength=300, padx=15,
                      justify=LEFT)
        label.grid(row=0, columnspan=2, sticky='n')

        gaussian_low = Radiobutton(self, text='Low Frequency', value='gaussian_l', variable=self.radValue)
        gaussian_high = Radiobutton(self, text='High Frequency', value='gaussian_h', variable=self.radValue)

        gaussian_low.grid(row=2, columnspan=2, sticky='w')
        gaussian_high.grid(row=3, columnspan=2, sticky='w')

        cutoff_slider = Scale(self, from_=50, to=150, orient=HORIZONTAL, variable=self.sliderValue)
        cutoff_slider.grid(row=4, column=1, sticky='w')

        label = Label(self, text='Select Cutoff:',
                      font=("Apple Chancery", 18), wraplength=200,
                      justify=RIGHT)
        label.grid(row=4, column=0, sticky='w')

    def apply_filter(self, image):
        print("apply_filter function hit!")
        slider_selected = self.sliderValue.get()
        return self.gaussian(image, slider_selected)

    def gaussian(self, image, cutoff):
        print("gaussian function hit!")
        self.rad_selected = self.radValue.get()

        gaussian = BasicFilter.Filtering(image, self.rad_selected, cutoff)
        output = gaussian.filtering()
        return output

    def is_low_frequency(self):
        frequency = self.rad_selected
        if frequency == 'gaussian_l':
            return True
        else:
            return False


#   PAGE IN MIDDLE FRAME
class OlympicPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.radValue = IntVar()
        self.sliderValue = IntVar()

        label = Label(self, text="Olympic Filter Options", font=controller.fontSize, wraplength=200,
                      justify=LEFT)
        label.grid(row=0, column=0, sticky='n')
        button = Button(self, text="Go to the HomomorphicPage",
                        command=lambda: controller.show_frame("HomomorphicPage"))
        button.grid(row=2, column=0, sticky='w')

        #   RADIO BUTTONS
        win_size_rad_3 = Radiobutton(self, text='Window Size = 3', value=3, variable=self.radValue)
        win_size_rad_3.grid(row=3, column=0, sticky='w', columnspan=3)
        win_size_rad_5 = Radiobutton(self, text='Window Size = 5', value=5, variable=self.radValue)
        win_size_rad_5.grid(row=4, column=0, sticky='w', columnspan=3)

        cutoff_slider = Scale(self, from_=50, to=150, orient=HORIZONTAL, variable=self.sliderValue)
        cutoff_slider.grid(row=4, column=1, sticky='w')

    def apply_filter(self):
        print("apply_filter function hit!")
        return

    # def olympic(self):

    def radio_event(self):
        self.rad_selected = self.radValue.get()

        filter_img = self.controller.img_canvas_q1.image
        olympic_img = Olympic.olympic(filter_img, self.rad_selected)
        self.controller.img_canvas_q1.create_image(0, 0, image=self.controller.img_canvas_q1.image, anchor='nw')

    def is_low_frequency(self):
        frequency = self.rad_selected
        if frequency == 'olympic_l':
            return True
        else:
            return False


#   PAGE IN MIDDLE FRAME
class HomomorphicPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.radValue = StringVar()
        self.sliderValue = IntVar()

        label = Label(self, text="Homomorphic Filter Options", font=controller.fontSize, wraplength=250,
                      justify=LEFT)
        label.grid(row=0, column=0, sticky='n')
        button = Button(self, text="Go to the IdealPage",
                        command=lambda: controller.show_frame("IdealPage"))
        button.grid(row=2, column=0, sticky='w')

        cutoff_slider = Scale(self, from_=50, to=150, orient=HORIZONTAL, variable=self.sliderValue)
        cutoff_slider.grid(row=4, column=1, sticky='w')

    def apply_filter(self):
        print("apply_filter function hit!")
        return
    # def homomorphic(self, image=self.controller.buttonImg):


#   PAGE IN MIDDLE FRAME
class IdealPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.radValue = StringVar()
        self.sliderValue = IntVar()

        label = Label(self, text="\nIDEAL FILTER\n OPTIONS\n", font=("Apple Chancery", 20), wraplength=300, padx=30,
                      justify=LEFT)
        label.grid(row=0, columnspan=2, sticky='n')

        ideal_low = Radiobutton(self, text='Low Frequency', value='ideal_l', variable=self.radValue)
        ideal_high = Radiobutton(self, text='High Frequency', value='ideal_h', variable=self.radValue)

        ideal_low.grid(row=2, columnspan=2, sticky='w')
        ideal_high.grid(row=3, columnspan=2, sticky='w')

        cutoff_slider = Scale(self, from_=50, to=150, orient=HORIZONTAL, variable=self.sliderValue)
        cutoff_slider.grid(row=4, column=1, sticky='w')

        label = Label(self, text='Select Cutoff:',
                      font=font.Font(size=18), wraplength=200,
                      justify=RIGHT)
        label.grid(row=4, column=0, sticky='w')

    def apply_filter(self, image):
        print("apply_filter function hit!")
        slider_selected = self.sliderValue.get()
        return self.ideal(image, slider_selected)

    def ideal(self, image, cutoff):
        self.rad_selected = self.radValue.get()

        ideal = BasicFilter.Filtering(image, self.rad_selected, cutoff)
        output = ideal.filtering()
        return output

    def is_low_frequency(self):
        frequency = self.rad_selected
        if frequency == 'ideal_l':
            return True
        else:
            return False


if __name__ == '__main__':
    app = Application()
    app.mainloop()
