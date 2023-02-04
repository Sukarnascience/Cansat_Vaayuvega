from tkinter import *
from tkintermapview import TkinterMapView
import customtkinter
from datetime import datetime
import os
import time

customtkinter.set_appearance_mode("System")  
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Vaayuvega Flight Panel")
        self.geometry(f"{1200}x{600}+{100}+{50}")
        self.minsize(1200,600)
        self.maxsize(1400,700)
        self.logo = PhotoImage(file = f"{os.path.dirname(__file__)}\logo.png")
        self.iconphoto(False, self.logo)

        self.start_time = time.time()

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Vaayuvega\nFlight\nControl", font=customtkinter.CTkFont(size=20, weight="bold"), justify='left')
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.label_radio_groupU = customtkinter.CTkLabel(master=self.sidebar_frame, text="Up Time",font=customtkinter.CTkFont(size=15, weight="bold"), justify='left')
        self.label_radio_groupU.grid(row=1, column=0, padx=10, pady=(5,5), sticky="")
        self.label_radio_groupUm = customtkinter.CTkLabel(master=self.sidebar_frame, text="00:00:00",font=customtkinter.CTkFont(size=13, weight="bold"), justify='left')
        self.label_radio_groupUm.grid(row=2, column=0, padx=10, pady=(5,5), sticky="")
        self.label_radio_groupF = customtkinter.CTkLabel(master=self.sidebar_frame, text="Flight Time",font=customtkinter.CTkFont(size=15, weight="bold"), justify='left')
        self.label_radio_groupF.grid(row=3, column=0, padx=10, pady=(5,5), sticky="")
        self.label_radio_groupFm = customtkinter.CTkLabel(master=self.sidebar_frame, text="00:00:00",font=customtkinter.CTkFont(size=13, weight="bold"), justify='left')
        self.label_radio_groupFm.grid(row=4, column=0, padx=10, pady=(5,5), sticky="")
        self.label_radio_groupC = customtkinter.CTkLabel(master=self.sidebar_frame, text="Current Time",font=customtkinter.CTkFont(size=15, weight="bold"), justify='left')
        self.label_radio_groupC.grid(row=5, column=0, padx=10, pady=(5,5), sticky="")
        self.label_radio_groupCm = customtkinter.CTkLabel(master=self.sidebar_frame, text="00:00:00",font=customtkinter.CTkFont(size=13, weight="bold"), justify='left')
        self.label_radio_groupCm.grid(row=6, column=0, padx=10, pady=(5,5), sticky="")

        #lol
        self.label_radio_groupCmz = customtkinter.CTkLabel(master=self.sidebar_frame, text=".",font=customtkinter.CTkFont(size=13, weight="bold"), justify='left')
        self.label_radio_groupCmz.grid(row=7, column=0, padx=10, pady=20, sticky="")
        self.label_radio_groupCma = customtkinter.CTkLabel(master=self.sidebar_frame, text=".",font=customtkinter.CTkFont(size=13, weight="bold"), justify='left')
        self.label_radio_groupCma.grid(row=8, column=0, padx=10, pady=20, sticky="")
        #lol
         
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=12, column=0, padx=20, pady=(10, 10))
        #self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite"],
        #                                                               command=self.change_map)
        #self.map_option_menu.grid(row=11, column=0, padx=(20, 20), pady=(10, 0))
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.download_in_CSV, text="Download")
        self.sidebar_button_3.grid(row=13, column=0, padx=20, pady=10)

        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        #self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Connect Sat :",font=customtkinter.CTkFont(size=20, weight="bold"), justify='left')
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.entry = customtkinter.CTkEntry(master=self.radiobutton_frame, placeholder_text="COM4")
        self.entry.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.entry = customtkinter.CTkEntry(master=self.radiobutton_frame, placeholder_text="9600")
        self.entry.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.sidebar_button_3 = customtkinter.CTkButton(master=self.radiobutton_frame, command=self.download_in_CSV, text="Connect")
        self.sidebar_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")
        self.sidebar_button_3 = customtkinter.CTkButton(master=self.radiobutton_frame, command=self.download_in_CSV, text="Connect Database")
        self.sidebar_button_3.grid(row=4, column=2, pady=10, padx=20, sticky="n")

        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        
        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Calibration 01")
        self.tabview.add("Calibration 02")
        self.tabview.add("Location")
        self.tabview.tab("Calibration 01").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Calibration 02").grid_columnconfigure(0, weight=1)

        self.optionmenu_1 = customtkinter.CTkEntry(self.tabview.tab("Calibration 01"), placeholder_text="Temperature ±XX °C")
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(5, 10))
        self.optionmenu_2 = customtkinter.CTkEntry(self.tabview.tab("Calibration 01"), placeholder_text="Humidity ±XX %")
        self.optionmenu_2.grid(row=1, column=0, padx=20, pady=(5, 10))
        self.optionmenu_3 = customtkinter.CTkEntry(self.tabview.tab("Calibration 01"), placeholder_text="Pressure ±XX hPa")
        self.optionmenu_3.grid(row=3, column=0, padx=20, pady=(5, 10))
        self.optionmenu_4 = customtkinter.CTkEntry(self.tabview.tab("Calibration 01"), placeholder_text="Altitude ±XX m")
        self.optionmenu_4.grid(row=4, column=0, padx=20, pady=(5, 10))
        self.combobox_1 = customtkinter.CTkButton(self.tabview.tab("Calibration 01"), text="Calibrate",
                                                           command=self.download_in_CSV)
        self.combobox_1.grid(row=5, column=0, padx=20, pady=(5, 10))

        self.string_input_button0 = customtkinter.CTkButton(self.tabview.tab("Calibration 02"), text="Set Current Time",
                                                           command=self.download_in_CSV)
        self.string_input_button0.grid(row=0, column=0, padx=20, pady=(5, 10))
        self.string_input_button1 = customtkinter.CTkButton(self.tabview.tab("Calibration 02"), text="Set Gyro Sensor",
                                                           command=self.download_in_CSV)
        self.string_input_button1.grid(row=1, column=0, padx=20, pady=(5, 10))
        self.string_input_button2 = customtkinter.CTkButton(self.tabview.tab("Calibration 02"), text="Set Alti Sensor",
                                                           command=self.download_in_CSV)
        self.string_input_button2.grid(row=2, column=0, padx=20, pady=(5, 10))
        self.optionmenu_24 = customtkinter.CTkEntry(self.tabview.tab("Calibration 02"), placeholder_text="Air Speed ±XX knot")
        self.optionmenu_24.grid(row=3, column=0, padx=20, pady=(5, 10))
        self.string_input_button3 = customtkinter.CTkButton(self.tabview.tab("Calibration 02"), text="Calibrate",
                                                           command=self.download_in_CSV)
        self.string_input_button3.grid(row=4, column=0, padx=20, pady=(5, 10))

        self.map_widget = TkinterMapView(self.tabview.tab("Location"), corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def current_time_fun(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.label_radio_groupCm.configure(text=current_time)
        self.label_radio_groupCm.after(200, self.current_time_fun)

    def current_upTime_fun(self):
        elapsed_time = time.time() - self.start_time
        minutes, seconds = divmod(elapsed_time, 60)
        hours, minutes = divmod(minutes, 60)
        self.label_radio_groupUm.configure(text="{:0>2}:{:0>2}:{:0>2}".format(int(hours), int(minutes), int(seconds)))
        self.label_radio_groupUm.after(200, self.current_upTime_fun)

    def download_in_CSV(self):
        print("CSV")

if __name__ == "__main__":
    app = App()
    app.current_time_fun()
    app.current_upTime_fun()
    app.mainloop()
# screen size and position
#window = Tk()
#window2 = customtkinter.CTk() 
#window2.geometry("1200x600+100+50")

#window.geometry('1200x600+100+50')
#window.minsize(1200,600)
#window.maxsize(1400,700)

#window.mainloop()
#window2.mainloop()

'''
    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
'''
