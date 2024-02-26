from tkinter import *
from tkintermapview import TkinterMapView
import customtkinter
from datetime import datetime
import os
import time
import webbrowser
import requests
import io

import os
from PIL import Image
import matplotlib.pyplot as plt  
#from queue import Queue
#pip install folium
import folium
from PIL import Image, ImageTk

import sat_map as satMap
import db_handel as dbControl
import stationControl as controler

customtkinter.set_appearance_mode("System")  
customtkinter.set_default_color_theme("blue")#we can put : "green"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.MAX_DATA_TO_PLOT = 6
        self.LENGHTOFDATA = 20
        self.TEMPGRAPHIMG = "tempGraph.png"
        self.HUMIGRAPHIMG = "humiGraph.png"
        self.ALTIGRAPHIMG = "altiGraph.png"
        self.logData = ""
        self.temp = [-1,-1,-1]

        # configure window
        self.title("Vaayuvega Flight Panel")
        self.geometry(f"{1200}x{600}+{100}+{50}")
        self.minsize(1200,600)
        self.maxsize(1400,700)
        #self.logo = PhotoImage(file = f"{os.path.dirname(__file__)}\logo.png") #Windows
        self.logo = PhotoImage(file = f"{os.path.dirname(__file__)}/logo.png") #Linux
        self.iconphoto(False, self.logo)

        self.start_time = time.time()

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(14, weight=1)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        self.Logo = customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(80, 80))
        self.home_frame1 = customtkinter.CTkLabel(master=self.sidebar_frame, text="", image=self.Logo)
        self.home_frame1.grid(row=0, column=0, padx=5, pady=2, sticky="")

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Vaayuvega\nFlight\nControl", font=customtkinter.CTkFont(size=20, weight="bold"), justify='left')
        self.logo_label.grid(row=1, column=0, padx=5, pady=(2,2), sticky="")
        self.label_radio_groupU = customtkinter.CTkLabel(master=self.sidebar_frame, text="Up Time",font=customtkinter.CTkFont(size=15, weight="bold"), justify='left')
        self.label_radio_groupU.grid(row=2, column=0, padx=5, pady=(2,2), sticky="")
        self.label_radio_groupUm = customtkinter.CTkLabel(master=self.sidebar_frame, text="00:00:00",font=customtkinter.CTkFont(size=13), justify='left')
        self.label_radio_groupUm.grid(row=3, column=0, padx=5, pady=(2,2), sticky="")
        self.label_radio_groupF = customtkinter.CTkLabel(master=self.sidebar_frame, text="Flight Time",font=customtkinter.CTkFont(size=15, weight="bold"), justify='left')
        self.label_radio_groupF.grid(row=4, column=0, padx=5, pady=(2,2), sticky="")
        self.label_radio_groupFm = customtkinter.CTkLabel(master=self.sidebar_frame, text="00:00:00",font=customtkinter.CTkFont(size=13), justify='left')
        self.label_radio_groupFm.grid(row=5, column=0, padx=5, pady=(2,2), sticky="")
        self.label_radio_groupC = customtkinter.CTkLabel(master=self.sidebar_frame, text="Current Time",font=customtkinter.CTkFont(size=15, weight="bold"), justify='left')
        self.label_radio_groupC.grid(row=6, column=0, padx=5, pady=(2,2), sticky="")
        self.label_radio_groupCm = customtkinter.CTkLabel(master=self.sidebar_frame, text="00:00:00",font=customtkinter.CTkFont(size=13), justify='left')
        self.label_radio_groupCm.grid(row=7, column=0, padx=5, pady=(2,2), sticky="")

        #lol
        #self.label_radio_groupCmz = customtkinter.CTkLabel(master=self.sidebar_frame, text=".",font=customtkinter.CTkFont(size=13, weight="bold"), justify='left')
        #self.label_radio_groupCmz.grid(row=7, column=0, padx=10, pady=20, sticky="")
        #self.label_radio_groupCma = customtkinter.CTkLabel(master=self.sidebar_frame, text=".",font=customtkinter.CTkFont(size=13, weight="bold"), justify='left')
        #self.label_radio_groupCma.grid(row=8, column=0, padx=10, pady=20, sticky="")
        #lol
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 10))
        #self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite"],
        #                                                               command=self.change_map)
        #self.map_option_menu.grid(row=11, column=0, padx=(20, 20), pady=(10, 0))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=10, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=11, column=0, padx=20, pady=(10, 20))
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.download_in_CSV, text="Download")
        self.sidebar_button_3.grid(row=12, column=0, padx=20, pady=10)

        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        #self.radio_var = tkinter.IntVar(value=0)
        self.status = controler.satC_Device()
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Connect Sat :",font=customtkinter.CTkFont(size=20, weight="bold"), justify='left')
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.COMentry = customtkinter.CTkEntry(master=self.radiobutton_frame, placeholder_text="COM4")#, textvariable=comNEnter)
        self.COMentry.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.Boudentry = customtkinter.CTkEntry(master=self.radiobutton_frame, placeholder_text="9600")#, textvariable=boudRateEnter)
        self.Boudentry.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.sidebar_button_3 = customtkinter.CTkButton(master=self.radiobutton_frame, command=self.connectD, text="Connect")
        self.sidebar_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")
        self.sidebar_button_3 = customtkinter.CTkButton(master=self.radiobutton_frame, command=self.download_in_CSV, text="Connect Database")
        self.sidebar_button_3.grid(row=4, column=2, pady=10, padx=20, sticky="n")
        self.connectStatusText = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Not Connected",font=customtkinter.CTkFont(size=13,weight="bold"), justify='left')
        self.connectStatusText.grid(row=5, column=2, padx=5, pady=(2,5), sticky="")

        #self.label_radio_groupUm = customtkinter.CTkLabel(master=self.sidebar_frame, text="00:00:00",font=customtkinter.CTkFont(size=13, weight="bold"), justify='left')
        #self.label_radio_groupUm.grid(row=2, column=0, padx=5, pady=(2,5), sticky="")

        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.GyroXYZ = customtkinter.CTkLabel(master=self.checkbox_slider_frame, text=("Gyro Data:\nX:---\nY:---\nZ:---"),font=customtkinter.CTkFont(size=13, weight="bold"), justify='left')
        self.GyroXYZ.grid(row=2, column=1, padx=5, pady=(5,5), sticky="")
        self.AcceXYZ = customtkinter.CTkLabel(master=self.checkbox_slider_frame, text=("Acce Data:\nX:---\nY:---\nZ:---"),font=customtkinter.CTkFont(size=13, weight="bold"), justify='left')
        self.AcceXYZ.grid(row=2, column=2, padx=5, pady=(5,5), sticky="")
        self.MagXYZ = customtkinter.CTkLabel(master=self.checkbox_slider_frame, text=("Magn Data:\nX:---\nY:---\nZ:---"),font=customtkinter.CTkFont(size=13, weight="bold"), justify='left')
        self.MagXYZ.grid(row=3, column=1, padx=5, pady=(5,5), sticky="")
        self.PressureL = customtkinter.CTkLabel(master=self.checkbox_slider_frame, text=("Pressure :\n---Pa"),font=customtkinter.CTkFont(size=13, weight="bold"), justify='left')
        self.PressureL.grid(row=3, column=2, padx=5, pady=(5,5), sticky="")
        self.packetNo = customtkinter.CTkLabel(master=self.checkbox_slider_frame, text=("Packet No: \n---"),font=customtkinter.CTkFont(size=13, weight="bold"), justify='center')
        self.packetNo.grid(row=4, column=1, padx=5, pady=(5,5), sticky="")
        self.batteryP = customtkinter.CTkLabel(master=self.checkbox_slider_frame, text=("Battery: \n---%"),font=customtkinter.CTkFont(size=13, weight="bold"), justify='center')
        self.batteryP.grid(row=4, column=2, padx=5, pady=(5,5), sticky="")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Location")
        self.tabview.add("Calibration 01")
        self.tabview.add("Calibration 02")
        self.tabview.tab("Calibration 01").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Calibration 02").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Location").grid_columnconfigure(0, weight=1)

        self.optionmenu_1 = customtkinter.CTkEntry(self.tabview.tab("Calibration 01"), placeholder_text="Temperature ±XX °C")
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(5, 10))
        self.optionmenu_2 = customtkinter.CTkEntry(self.tabview.tab("Calibration 01"), placeholder_text="Humidity ±XX %")
        self.optionmenu_2.grid(row=1, column=0, padx=20, pady=(5, 10))
        self.optionmenu_3 = customtkinter.CTkEntry(self.tabview.tab("Calibration 01"), placeholder_text="Pressure ±XX hPa")
        self.optionmenu_3.grid(row=3, column=0, padx=20, pady=(5, 10))
        self.optionmenu_4 = customtkinter.CTkEntry(self.tabview.tab("Calibration 01"), placeholder_text="Altitude ±XX m")
        self.optionmenu_4.grid(row=4, column=0, padx=20, pady=(5, 10))
        self.combobox_1 = customtkinter.CTkButton(self.tabview.tab("Calibration 01"), text="Calibrate")#, command=self.updateGraphTemp)
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

        #self.map_widget = TkinterMapView(self.tabview.tab("Location"), corner_radius=0)
        #self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))
        self.string_input_buttonL0 = customtkinter.CTkButton(self.tabview.tab("Location"), text="Open Map",
                                                           command=self.launchMap)
        self.string_input_buttonL0.grid(row=1, column=0, padx=20, pady=(5, 10))
        self.AltiL = customtkinter.CTkLabel(master=self.tabview.tab("Location"), text=("Altiude  :\n---m\n(From Ground Level)"),font=customtkinter.CTkFont(size=14), justify='center')
        self.AltiL.grid(row=2, column=0, padx=5, pady=(5,10), sticky="")
        self.LatiL = customtkinter.CTkLabel(master=self.tabview.tab("Location"), text=("Latitude :\n---"),font=customtkinter.CTkFont(size=14), justify='center')
        self.LatiL.grid(row=3, column=0, padx=5, pady=(5,10), sticky="")
        self.LogiL = customtkinter.CTkLabel(master=self.tabview.tab("Location"), text=("longitude:\n---"),font=customtkinter.CTkFont(size=14), justify='center')
        self.LogiL.grid(row=4, column=0, padx=5, pady=(5,10), sticky="")

        self.DB = dbControl.database()

        # Create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self)#, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=2, columnspan=1, padx=(20, 0), pady=(20, 0), sticky="nsew")#row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(3, weight=1)

        # Create progress bars and labels for each graph
        self.progressbar_temp = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_temp.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progress_label_temp = customtkinter.CTkLabel(self.slider_progressbar_frame, text="Temperature: 0°C", anchor="w")
        self.progress_label_temp.grid(row=0, column=1, padx=(10, 20), pady=(10, 10), sticky="ew")

        self.progressbar_humi = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_humi.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progress_label_humi = customtkinter.CTkLabel(self.slider_progressbar_frame, text="Humidity: 0%", anchor="w")
        self.progress_label_humi.grid(row=1, column=1, padx=(10, 20), pady=(10, 10), sticky="ew")

        self.progressbar_alti = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_alti.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progress_label_alti = customtkinter.CTkLabel(self.slider_progressbar_frame, text="Altitude: 0m", anchor="w")
        self.progress_label_alti.grid(row=2, column=1, padx=(10, 20), pady=(10, 10), sticky="ew")

        self.progressbar_battery = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_battery.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progress_label_battery = customtkinter.CTkLabel(self.slider_progressbar_frame, text="Battery : 0%", anchor="w")
        self.progress_label_battery.grid(row=3, column=1, padx=(10, 20), pady=(10, 10), sticky="ew")

        self.map = customtkinter.CTkFrame(self, width=250)
        self.map.grid(row=0, column=1, rowspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.LogPG = customtkinter.CTkLabel(self.map, text="LOG Stats : ", anchor="w",  font=customtkinter.CTkFont(size=20, weight="bold"), justify='left')
        self.LogPG.grid(row=0, column=1, padx=(10, 20), pady=(10, 10), sticky="ew")
        self.textbox = customtkinter.CTkTextbox(self.map, height=500, width=380)
        self.textbox.grid(row=1, column=1, rowspan=2, padx=(10, 0), pady=(10, 0), sticky="ns")
        self.textbox.grid_columnconfigure(0, weight=1)
        self.textbox.grid_rowconfigure(2, weight=2)
        self.logData = "UI Launch\n"
        self.textbox.insert("0.0", self.logData)
        # Change this area :---
        '''
        self.graph_frame = customtkinter.CTkFrame(self)#, fg_color="transparent")
        self.graph_frame.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.graph_frame.grid_columnconfigure(2, weight=1)
        self.graph_frame.grid_rowconfigure(1, weight=1)

        self.altiPlate = customtkinter.CTkFrame(self, width=250)
        self.altiPlate.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        '''

    def openMap(self):
        app = satMap.App()
        app.start()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        self.logData = "Changed Mode\n"
        self.textbox.insert("0.0", self.logData)
        customtkinter.set_appearance_mode(new_appearance_mode)
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

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
        now = datetime.now()
        current_time = now.strftime("%H%M%S")
        self.logData = "Downloading CSV at your local directry\n"
        self.textbox.insert("0.0", self.logData)
        print("Downloading CSV at your local directry")
        self.DB.downloadData(fname="CanSat_Data_{}".format(current_time))
    
    def launchMap(self):
        webbrowser.open('https://aprs.fi/#!z=1500&lat=13.1686&lng=77.5350')

    def connectD(self):
        self.logData = "Data Collected are: {},{}\n".format(self.COMentry.get(),self.Boudentry.get())
        self.textbox.insert("0.0", self.logData)
        print("Data Collected are: {},{}".format(self.COMentry.get(),self.Boudentry.get())) 
        self.status.connectToDevice(portN=str(self.COMentry.get()),boudRateN=int(self.Boudentry.get()))
    
    def updateConn_stats(self):
        if(self.status.isConnect()):
            if(self.logData != "Module Connected\n"):
                self.logData = "Module Connected\n"
                self.textbox.insert("0.0", self.logData)
            self.connectStatusText.configure(text="Connected")
        else:
            if(self.logData != "Module failed to Connected\n"):
                self.logData = "Module failed to Connected\n"
                self.textbox.insert("0.0", self.logData)
            self.connectStatusText.configure(text="Not Connected")
        self.connectStatusText.after(200, self.updateConn_stats)

    def updateDataDashboard(self):
        self.dataCame = self.status.giveData()
        self.after(200, self.updateDataDashboard)

    def updateFlightTime(self):
        if(self.status.isConnect() and self.dataCame!=None and len(self.dataCame)==self.LENGHTOFDATA):
            self.logData = "{}\n".format(self.dataCame[2])
            self.textbox.insert("0.0", self.logData)
            self.label_radio_groupFm.configure(text="{}".format(self.dataCame[2]))
        self.label_radio_groupFm.after(200, self.updateFlightTime)
    def updatePacketCount(self):
        if(self.status.isConnect() and self.dataCame!=None and len(self.dataCame)==self.LENGHTOFDATA):
            self.logData = "Packet No: \n{}".format(self.dataCame[1])
            self.textbox.insert("0.0", self.logData)
            self.packetNo.configure(text="Packet No: \n{}".format(self.dataCame[1]))
        self.packetNo.after(200, self.updatePacketCount)
    
    def updateGyro(self):
        if(self.status.isConnect() and self.dataCame!=None and len(self.dataCame)==self.LENGHTOFDATA):
            self.logData = "Gyro Data: |X:{} |Y:{} |Z:{}\n".format(self.dataCame[3],self.dataCame[4],self.dataCame[5])
            self.textbox.insert("0.0", self.logData)
            self.GyroXYZ.configure(text="Gyro Data:\nX:{}\nY:{}\nZ:{}".format(self.dataCame[3],self.dataCame[4],self.dataCame[5]))
        self.GyroXYZ.after(200, self.updateGyro)

    def updateAcce(self):
        if(self.status.isConnect() and self.dataCame!=None and len(self.dataCame)==self.LENGHTOFDATA):
            self.logData = "Acce Data: |X:{} |Y:{} |Z:{}\n".format(self.dataCame[6],self.dataCame[7],self.dataCame[8])
            self.textbox.insert("0.0", self.logData)
            self.AcceXYZ.configure(text="Acce Data:\nX:{}\nY:{}\nZ:{}".format(self.dataCame[6],self.dataCame[7],self.dataCame[8]))
        self.AcceXYZ.after(200, self.updateAcce)

    def updateMage(self):
        if(self.status.isConnect() and self.dataCame!=None and len(self.dataCame)==self.LENGHTOFDATA):
            self.logData = "Magn Data: |X:{} |Y:{} |Z:{}\n".format(self.dataCame[9],self.dataCame[10],self.dataCame[11])
            self.textbox.insert("0.0", self.logData)
            self.MagXYZ.configure(text="Magn Data:\nX:{}\nY:{}\nZ:{}".format(self.dataCame[9],self.dataCame[10],self.dataCame[11]))
        self.MagXYZ.after(200, self.updateMage)

    def updatePressure(self):
        if(self.status.isConnect() and self.dataCame!=None and len(self.dataCame)==self.LENGHTOFDATA):
            self.logData = "Pressure : {}Pa\n".format(self.dataCame[13])
            self.textbox.insert("0.0", self.logData)
            self.PressureL.configure(text="Pressure :\n{}Pa".format(self.dataCame[13]))
        self.PressureL.after(200, self.updatePressure)
    
    def updateBatteryP(self):
        if(self.status.isConnect() and self.dataCame!=None and len(self.dataCame)==self.LENGHTOFDATA):
            self.logData = "Battery : {}%\n".format(self.dataCame[19])
            self.textbox.insert("0.0", self.logData)
            self.batteryP.configure(text="Battery :\n{}%".format(self.dataCame[19]))
            self.progressbar_battery.set(self.dataCame[19])
        self.batteryP.after(200, self.updateBatteryP)
    
    def updateAlti(self):
        if(self.status.isConnect() and self.dataCame!=None and len(self.dataCame)==self.LENGHTOFDATA):
            self.logData = "Altiude: {}m | (From Ground Level)\n".format(self.dataCame[12])
            self.textbox.insert("0.0", self.logData)
            self.AltiL.configure(text="Altiude:\n{}m\n(From Ground Level)".format(self.dataCame[12]))
        self.AltiL.after(200, self.updateAlti)

    def updateLati(self):
        if(self.status.isConnect() and self.dataCame!=None and len(self.dataCame)==self.LENGHTOFDATA):
            self.logData = "Latitude : {}\n".format(self.dataCame[17])
            self.textbox.insert("0.0", self.logData)
            self.LatiL.configure(text="Latitude :\n{}".format(self.dataCame[17]))
        self.LatiL.after(200, self.updateLati)

    def updateLongi(self):
        if(self.status.isConnect() and self.dataCame!=None and len(self.dataCame)==self.LENGHTOFDATA):
            self.logData = "longitude: {}\n".format(self.dataCame[18])
            self.textbox.insert("0.0", self.logData)
            self.LogiL.configure(text="longitude:\n{}".format(self.dataCame[18]))
        self.LogiL.after(200, self.updateLongi)

    #def updateGraphTemp(self):
        '''
        self.dataTG = self.DB.getGraphData()
        self.dataTG = self.dataTG[0]
        x = self.dataTG[0]
        y = self.dataTG[1]
        #print("X : {}".format(x))
        #print("Y : {}".format(y))
        plt.plot(x, y) 
        plt.title('Temperature Values')
        plt.xlabel('Time Stamp')
        plt.ylabel('Temperature °C')
        #plt.show() 
        plt.savefig(self.TEMPGRAPHIMG)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        self.large_test_image0 = customtkinter.CTkImage(Image.open(os.path.join(image_path, self.TEMPGRAPHIMG)), size=(320, 240))
        self.home_frame_large_image_label0 = customtkinter.CTkLabel(master=self.graph_frame, text="", image=self.large_test_image0, justify='center')
        self.home_frame_large_image_label0.grid(row=0, column=0, padx=5, pady=5)
        self.after(1000, self.updateGraphTemp)
        '''
        #self.dataTG = self.DB.getGraphData()
        #self.dataTG = self.dataTG[0]
        #x = self.dataTG[0]
        #y = self.dataTG[1]
        #print("X : {}".format(x))
        #print("Y : {}".format(y))
        #self.after(1000, self.updateGraphTemp)

    #def updateGraphHumi(self):
        '''
        self.dataHG = self.DB.getGraphData()
        self.dataHG = self.dataHG[2]
        x = self.dataHG[0]
        y = self.dataHG[1]
        #print("X : {}".format(x))
        #print("Y : {}".format(y))
        plt.plot(x, y) 
        plt.title('Humidity Values')
        plt.xlabel('Time Stamp')
        plt.ylabel('Humidity %')
        #plt.show() 
        plt.savefig(self.HUMIGRAPHIMG)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        self.large_test_image1 = customtkinter.CTkImage(Image.open(os.path.join(image_path, self.HUMIGRAPHIMG)), size=(320, 240))
        self.home_frame_large_image_label1 = customtkinter.CTkLabel(master=self.graph_frame, text="", image=self.large_test_image1, justify='center')
        self.home_frame_large_image_label1.grid(row=0, column=1, padx=5, pady=5)
        self.after(1000, self.updateGraphHumi)
        '''
        #self.dataHG = self.DB.getGraphData()
        #self.dataHG = self.dataHG[2]
        #x = self.dataHG[0]
        #y = self.dataHG[1]
        #print("X : {}".format(x))
        #print("Y : {}".format(y))

        #self.progressbar_1.set(x)
        # Update progress bar labels
        #self.progress_label_1.config(text=f"Progress 1: {value_1}%")

        #self.after(1000, self.updateGraphHumi)

    #def updateGraphAlti(self):
        '''
        self.dataAG = self.DB.getGraphData()
        self.dataAG = self.dataAG[1]
        x = self.dataAG[0]
        y = self.dataAG[1]
        #print("X : {}".format(x))
        #print("Y : {}".format(y))
        plt.plot(x, y) 
        plt.title('Altitude Values')
        plt.xlabel('Time Stamp')
        plt.ylabel('Altitude m')
        #plt.show() 
        plt.savefig(self.ALTIGRAPHIMG)
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        self.large_test_image2 = customtkinter.CTkImage(Image.open(os.path.join(image_path, self.ALTIGRAPHIMG)), size=(320, 240))
        self.home_frame_large_image_label2 = customtkinter.CTkLabel(master=self.altiPlate, text="", image=self.large_test_image2)
        self.home_frame_large_image_label2.grid(row=0, column=0, padx=5, pady=5)
        self.after(1000, self.updateGraphAlti)
        '''
        #self.dataAG = self.DB.getGraphData()
        #self.dataAG = self.dataAG[1]
        #x = self.dataAG[0]
        #y = self.dataAG[1]
        #print("X : {}".format(x))
        #print("Y : {}".format(y))
        #self.after(1000, self.updateGraphAlti)
    
    def updateProgress(self):
        self.dataAG = self.DB.getGraphData()
        self.dataAG = self.dataAG[1]
        xA = self.dataAG[0]
        yA = self.dataAG[1]
        self.dataHG = self.DB.getGraphData()
        self.dataHG = self.dataHG[2]
        xH = self.dataHG[0]
        yH = self.dataHG[1]
        self.dataTG = self.DB.getGraphData()
        self.dataTG = self.dataTG[0]
        xT = self.dataTG[0]
        yT = self.dataTG[1]
        
        # Your logic to get the values for the progress bars
        value_temp = int(yT[0])/100
        value_humi = int(yH[0])/100
        value_alti = round(int(yA[0])/300, 2)
        #print(value_temp)
        #print(value_humi)
        #print(value_alti)

        # Update progress bar values
        self.progressbar_temp.set(value_temp)
        self.progressbar_humi.set(value_humi)
        self.progressbar_alti.set(value_alti)

        # Update progress bar labels
        self.progress_label_temp.configure(text=f"Temperature: {int(yT[0])}°C")
        self.progress_label_humi.configure(text=f"Humidity: {int(yH[0])}%")
        self.progress_label_alti.configure(text=f"Altitude: {int(yA[0])}m")

        value_temp = int(yT[0])
        value_humi = int(yH[0])
        value_alti = int(yA[0])
        print(self.temp)
        if([value_alti,value_humi,value_temp] != self.temp):
            self.temp = [value_alti,value_humi,value_temp]
            self.logData = f"Temperature: {value_temp}°C \nHumidity: {value_humi}% \nAltitude: {value_alti}m \n"
            self.textbox.insert("0.0", self.logData)

        # Schedule the method to be called after a certain interval
        self.after(1000, self.updateProgress)


    def dumpDB(self):
        if(self.status.isConnect() and self.dataCame!=None and len(self.dataCame)==self.LENGHTOFDATA):
            self.DB.dumpData(self.dataCame)
        self.after(200, self.dumpDB)

    def backupData(self):
        if(self.status.isConnect() and self.dataCame!=None):
            now = datetime.now()
            current_time = now.strftime("%w%d%y")
            self.DB.createLiveData(fname="CanSat_Data_Backup_{}".format(current_time),data=self.dataCame)
        self.after(200, self.backupData)

        

if __name__ == "__main__":                                                 
    app = App() 
    app.current_time_fun()
    app.current_upTime_fun()
    app.updateConn_stats()

    app.updateDataDashboard()
    app.dumpDB()
    app.updateFlightTime()
    app.updatePacketCount()
    app.updateGyro()
    app.updateAcce()
    app.updateMage()
    app.updateAlti()
    app.updateLongi()
    app.updateLati()
    app.updatePressure()
    #app.updateGraphTemp()
    #app.updateGraphHumi()
    #app.updateGraphAlti()
    app.updateBatteryP()
    app.updateProgress()

    app.backupData()

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

# Plot a img (it will overwrite and show
# catter plot
# Figma to python fopr GUI