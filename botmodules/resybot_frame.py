from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from pathlib import Path
import os
import git
import sys
from sys import platform
from subprocess import Popen, check_call
import warnings
import shutil
from tktimepicker import SpinTimePickerOld
from database import Database
from datetime import datetime, timedelta

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from settings import PYTHON_EXE, CHROME_USER_DATA
# creating a database object
db = Database("dbresy.db")

warnings.filterwarnings("ignore", category=UserWarning)
if platform == "linux" or platform == "linux2":
    pass
elif platform == "win32":
	from subprocess import CREATE_NEW_CONSOLE
import json

warnings.filterwarnings("ignore", category=UserWarning)
if platform == "linux" or platform == "linux2":
    pass
elif platform == "win32":
	from subprocess import CREATE_NEW_CONSOLE
import json

def savejson(filename, valuelist, value=False):
	# breakpoint()
	if value:
		file = open(filename, "r")
		tmplist = json.load(file)
		found = False
		# breakpoint()
		for lst1 in tmplist:
			if lst1['profilename'] == value:
				messagebox.showerror("Message box","profile name found")
				found = True
				break
		# breakpoint()
		if not found:
			with open(filename, "w") as final:
				json.dump(valuelist, final)
			return True
		else:
			return False
	else:
		# breakpoint()
		with open(filename, "w") as final:
			try:
				json.dump(valuelist.get(0, END), final)
			except:
				json.dump(valuelist, final)
		return True

def convert24time(vtime):
	hour = str(vtime.hours())
	period = vtime.period().replace(".","").upper()
	if len(str(vtime.minutes())) == 1:
		minute = f"0{str(vtime.minutes())}"
	else:
		minute = str(vtime.minutes())
	return f"{hour}:{minute} {period}"

def convert24timeSecond(vtime):
	hour = str(vtime.hours())
	period = vtime.period().replace(".","").upper()
	if len(str(vtime.minutes())) == 1:
		minute = f"0{str(vtime.minutes())}"
	else:
		minute = str(vtime.minutes())
	if len(str(vtime.seconds())) == 1:
		second = f"0{str(vtime.seconds())}"
	else:
		second = str(vtime.seconds())
	return f"{hour}:{minute}:{second} {period}"

class Window(Tk):
	def __init__(self) -> None:
		super().__init__()
		self.title('Resy.com Bot Application @2024')
		# self.resizable(0, 0)
		self.gitme = git.cmd.Git(os.getcwd())
		self.gitme.fetch()
		# breakpoint()
		self.grid_propagate(False)
		width = 1300
		height = 720
		swidth = self.winfo_screenwidth()
		sheight = self.winfo_screenheight()
		newx = int((swidth/2) - (width/2))
		newy = int((sheight/2) - (height/2))
		self.geometry(f"{width}x{height}+{newx}+{newy}")
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)
		self.columnconfigure(3, weight=1)

		self.rowconfigure(0, weight=1)
		exitButton = ttk.Button(self, text="Exit", command=lambda:self.procexit())
		# pullButton = Button(self, text='Update Script', command=lambda:self.gitPull())
		# settingButton = ttk.Button(self, text='Chrome Setup', command=lambda:chromeSetup())
		
		exitButton.grid(row=2, column=3, sticky=(E), padx=20, pady=5)
		
		mainFrame = ResyBotv5Frame(self)
		mainFrame.grid(column=0, row=0, sticky=(N, E, W, S), columnspan=4)


	def procexit(self):
		try:
			for p in Path(".").glob("__tmp*"):
				p.unlink()
		except:
			pass
		sys.exit()

class ResyBotv5Frame(ttk.Frame):
	def __init__(self, window) -> None:
		super().__init__(window)
		# configure
		self.grid(column=0, row=0, sticky=(N, E, W, S), columnspan=4)
		self.config(padding="20 20 20 20", borderwidth=1, relief='groove')
		self.chosenRow = None
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=1)
		self.columnconfigure(2, weight=1)

		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)
		self.rowconfigure(2, weight=1)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(4, weight=1)
		self.rowconfigure(5, weight=1)
		self.rowconfigure(6, weight=1)
		self.rowconfigure(7, weight=1)
		self.rowconfigure(8, weight=1)
		self.rowconfigure(9, weight=1)
		self.rowconfigure(10, weight=1)
		self.rowconfigure(11, weight=1)
		self.rowconfigure(12, weight=1)
		self.rowconfigure(13, weight=1)
		self.rowconfigure(14, weight=1)
		self.rowconfigure(15, weight=1)
		self.rowconfigure(16, weight=1)
		self.rowconfigure(17, weight=1)
		self.rowconfigure(18, weight=1)
		self.rowconfigure(19, weight=1)
		self.rowconfigure(20, weight=1)
		
		# populate
		titleLabel = TitleLabel(self, text="Resy Bot Form")
		urllabel = Label(self, text="Base URL: ")
		datelabel = Label(self, text="Date: ")
		timelabel = Label(self, text="Time: ")
		rangelabel = Label(self, text="hours before & after: ")
		seatslabel = Label(self, text="Seats: ")
		reservationlabel = Label(self, text="Reservation Type: ")
		chprofilelabel = Label(self, text="Account: ")
		runimlabel = Label(self, text="Run Immediately: ")
		rundatelabel = Label(self, text="Run Date: ")
		runtimelabel = Label(self, text="Run Time: ")
		nstoplabel = Label(self, text="Nonstop Checking: ")
		durationlabel = Label(self, text="Duration in Minutes: ")
		proxylabel = Label(self, text="Proxy: ")
		self.url = StringVar(value="https://resy.com/cities/orlando-fl/venues/kabooki-sushi-east-colonial")
		urlentry = Entry(self, width=80, textvariable=self.url)
		self.date = StringVar()
		dateentry = DateEntry(self, width= 20, date_pattern='yyyy-mm-dd', textvariable=self.date)
		self.time = StringVar()
		self.timeentry = SpinTimePickerOld(self)
		self.timeentry.addHours12()
		self.timeentry.addMinutes()
		self.timeentry.addPeriod()
		self.defseat = StringVar(value=2)
		seatsentry = Spinbox(self, from_=1, to=100, textvariable=self.defseat, state="readonly", width=5)
		seatsentry.insert(0,2)
		self.defrange = StringVar(value=0)
		rangeentry = Spinbox(self, from_=0, to=100, textvariable=self.defrange, state="readonly", width=5)
		# rangeentry.insert(0,0)
		self.reservation = StringVar()
		reservationentry = ttk.Combobox(self, textvariable=self.reservation, state="readonly", width=30)
		reservationentry['values'] =  db.reservationValues()
		reservationentry.current(0)
		self.profile=StringVar()
		chprofileentry = ttk.Combobox(self, textvariable=self.profile, state="readonly", width=30)
		chprofileentry['values'] = db.profileValues()
		chprofileentry.current(0)
		self.rundate = StringVar()
		rundateentry = DateEntry(self, width= 20, date_pattern='yyyy-mm-dd', textvariable=self.rundate)
		self.runtimeentry = SpinTimePickerOld(self)
		self.runtimeentry.addHours12()
		self.runtimeentry.addMinutes()
		self.runtimeentry.addSeconds()
		self.runtimeentry.addPeriod()
		self.runim = StringVar()
		runimentry = ttk.Combobox(self, textvariable=self.runim, state="readonly", width=5)
		runimentry['values'] = ['No','Yes']
		runimentry.current(0)
		self.nstop=StringVar()
		nstopentry = ttk.Combobox(self, textvariable=self.nstop, state="readonly", width=5)
		nstopentry['values'] = ['No','Yes']
		nstopentry.current(0)
		self.duration = StringVar(value=0)
		durationentry = Spinbox(self, from_=0, to=600, textvariable=self.duration, width=5)
		self.proxy=StringVar()
		proxyentry = ttk.Combobox(self, textvariable=self.proxy, state="readonly", width=30)
		proxyentry['values'] = db.proxyValues()
		proxyentry.current(0)

		closeButton = CloseButton(self)
		saveButton = ttk.Button(self, text='Insert Booking', command = lambda:self.savelist(url=urlentry, date=dateentry, time=self.timeentry, seats=seatsentry, reservation=reservationentry, profile=chprofileentry, range_hours=rangeentry, run_date=rundateentry, run_time=self.runtimeentry, runnow=runimentry, nonstop=nstopentry, duration=durationentry, proxy=proxyentry))
		runButton = ttk.Button(self, text='Run Booking', command=self.viewCommand)
		removeButton = ttk.Button(self, text='Delete Booking', command=self.removeCommand)
		updateButton = ttk.Button(self, text='Update Booking', command=self.updateCommand)

		# layout
		titleLabel.grid(column = 0, row = 0, sticky = (W, E, N, S), columnspan=3)
		urllabel.grid(column = 0, row = 1, sticky=(W))
		urlentry.grid(column = 0, row = 1, sticky=(E))
		datelabel.grid(column = 0, row = 2, sticky=(W))
		dateentry.grid(column = 0, row = 2, sticky=(E))
		timelabel.grid(column = 0, row = 3, sticky=(W))
		self.timeentry.grid(column = 0, row = 3, sticky=(E))
		rangelabel.grid(column = 0, row = 4, sticky=(W))
		rangeentry.grid(column = 0, row = 4, sticky=(E))
		seatslabel.grid(column = 0, row = 5, sticky=(W))
		seatsentry.grid(column = 0, row = 5, sticky=(E))
		reservationlabel.grid(column = 0, row = 6, sticky=(W))
		reservationentry.grid(column = 0, row = 6, sticky=(E))
		rundatelabel.grid(column = 2, row = 1, sticky=(W))
		rundateentry.grid(column = 2, row = 1, sticky=(E))
		runtimelabel.grid(column = 2, row = 2, sticky=(W))
		self.runtimeentry.grid(column = 2, row = 2, sticky=(E))
		runimlabel.grid(column = 2, row = 3, sticky=(W))
		runimentry.grid(column = 2, row = 3, sticky=(E))
		chprofilelabel.grid(column = 2, row = 4, sticky=(W))
		chprofileentry.grid(column = 2, row = 4, sticky=(E))
		nstoplabel.grid(column = 2, row = 5, sticky=(W))
		nstopentry.grid(column = 2, row = 5, sticky=(E))
		durationlabel.grid(column = 2, row = 6, sticky=(W))
		durationentry.grid(column = 2, row = 6, sticky=(E))
		proxylabel.grid(column = 2, row = 7, sticky=(W))
		proxyentry.grid(column = 2, row = 7, sticky=(E))
		# viewButton.grid(column=2, row=8, sticky=(W))
		saveButton.grid(column = 2, row = 8, sticky = (E))
		runButton.grid(column = 0, row = 8, sticky = (W))
		updateButton.grid(column = 2, row = 8, sticky = (W))
		removeButton.grid(column = 0, row = 8, sticky = (E))
		self.tableOutputFrame()
		self.viewCommand()
		self.resetForm()
                
	def savelist(self, **kwargs):
		formatted_time = convert24time(kwargs['time'])
		formatted_runtime = convert24timeSecond(kwargs['run_time'])
		db.insertCommand(url=kwargs['url'].get(), datewanted=str(kwargs['date'].get_date()), timewanted=formatted_time, seats=kwargs['seats'].get(), reservation=kwargs['reservation'].get(), account=kwargs['profile'].get(), hoursba=kwargs['range_hours'].get(), rundate=str(kwargs['run_date'].get_date()), runtime=formatted_runtime, runnow=kwargs['runnow'].get(), nonstop=kwargs['nonstop'].get(), duration=kwargs['duration'].get(), proxy=kwargs['proxy'].get())
		# savejson(filename="commandlist.json", valuelist=self.commandlist)
		self.viewCommand()
		messagebox.showinfo("Message box","Booking list Saved")
		self.resetForm()
		
	def viewCommand(self):
		self.out.delete(*self.out.get_children())  # emptying the table before reloading
		for row in db.viewCommand():
			self.out.insert("", END, values=row)

	def removeCommand(self):
		if not messagebox.askyesno(title='confirmation',message='Do you want to remove it?'):
			return
		try:
			db.removeCommand(self.chosenRow[0])
			# self.resetForm()
			self.viewCommand()
		except AttributeError as error:
			messagebox.showerror("Error!", "Please Choose an Instructor Record to Remove!")
		

	def updateCommand(self):
		if self.chosenRow == None:
			messagebox.showerror("Error!", "Please Choose an Instructor Record to Update!")
		# print(self.url.get())
		formatted_time = convert24time(self.timeentry)
		formatted_runtime = convert24timeSecond(self.runtimeentry)
		# breakpoint()
		db.updateCommand(comid=self.chosenRow[0], url=self.url.get(), datewanted=self.date.get(), timewanted=formatted_time, hoursba=self.defrange.get(), seats=self.defseat.get(), reservation=self.reservation.get(), rundate=self.rundate.get(), runtime=formatted_runtime, runnow=self.runim.get(), account=self.profile.get(), nonstop=self.nstop.get(), duration=self.duration.get(), proxy=self.proxy.get())
		self.viewCommand()
		messagebox.showinfo("Info", "Command Updates..")
		self.resetForm()
		
	def resetForm(self):
			self.url.set("https://resy.com/cities/orlando-fl/venues/kabooki-sushi-east-colonial")
			self.date.set(datetime.strftime(datetime.now(), '%Y-%m-%d'))
			self.timeentry.set12Hrs(5)
			self.timeentry.setMins(0)
			self.timeentry.setPeriod("p.m")
			self.defseat.set("2")
			self.defrange.set("0")
			self.reservation.set("<Not Set>")
			self.rundate.set(datetime.strftime(datetime.now(), '%Y-%m-%d'))
			# self.profile.set(self.chosenRow[10])
			periodrt = datetime.strftime(datetime.now(), "%p").lower()
			periodrt = periodrt[0]+"."+periodrt[1]
			self.runtimeentry.set12Hrs(datetime.strftime(datetime.now(), "%I"))
			self.runtimeentry.setMins(datetime.strftime(datetime.now(), "%M"))
			self.runtimeentry.setSecs(datetime.strftime(datetime.now(), "%S"))
			self.runtimeentry.setPeriod(periodrt)
			# self.runtimeentry.set12Hrs(self.chosenRow[8].split(":")[0])
			self.runim.set("No")
			self.nstop.set("No")
			self.duration.set("0")
			self.proxy.set("<Not Set>")
		

	def tableOutputFrame(self):
		self.tableFrame = Frame(self, bg="#DADDE6")
		self.tableFrame.place(x=0, y=400, width=1290, height=260)
		self.yScroll = Scrollbar(self.tableFrame)
		self.yScroll.pack(side=RIGHT, fill=Y)
		self.style = ttk.Style()
		self.style.configure("mystyle.Treeview", font=('Calibri', 12), rowheight=30)
		self.style.configure("mystyle.Treeview.Heading", font=('Times New Roman', 14, "bold"), sticky="w")
		self.out = ttk.Treeview(self.tableFrame, yscrollcommand=self.yScroll.set, 
        columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15), style="mystyle.Treeview")
		self.out.heading("1", text="ID")
		self.out.column("1", width=0, stretch="no")
		self.out.heading("2", text="Restaurant")
		self.out.column("2", width=200, stretch="no")
		self.out.heading("3", text="Date")
		self.out.column("3", width=5)
		self.out.heading("4", text="Time")
		self.out.column("4", width=5)
		self.out.heading("5", text="Range")
		self.out.column("5", width=2, anchor="center")
		self.out.heading("6", text="Seats")
		self.out.column("6", width=2, anchor="center")
		self.out.heading("7", text="Reservation")
		self.out.column("7", width=5)
		self.out.heading("8", text="RunDate")
		self.out.column("8", width=5)
		self.out.heading("9", text="RunTime")
		self.out.column("9", width=5) 
		self.out.heading("10", text="RNow") 
		self.out.column("10", width=70, anchor="center", stretch="no")
		self.out.heading("11", text="Account")
		self.out.column("11", width=10)
		self.out.heading("12", text="NStop")
		self.out.column("12", width=70, anchor="center", stretch="no")
		self.out.heading("13", text="Drs")
		self.out.column("13", width=70, anchor="center", stretch="no")
		self.out.heading("14", text="Proxy")
		self.out.column("14", width=10)
		self.out.heading("15", text="URL")
		self.out.column("15", width=0, stretch=0)

		self.out['show'] = 'headings'
		self.out.bind("<ButtonRelease-1>", self.getData)
		# self.comboAvail.bind("<<ComboboxSelected>>", self.selectDays)
		self.out.pack(fill=X)
		self.yScroll.config(command=self.out.yview)

	def getData(self, event):
		try:
			self.selectedRow = self.out.focus()
			self.selectedData = self.out.item(self.selectedRow)
			self.chosenRow = self.selectedData["values"]
			self.url.set(self.chosenRow[14])
			self.date.set(self.chosenRow[2])
			self.timeentry.set12Hrs(self.chosenRow[3].split(":")[0] )
			self.timeentry.setMins(self.chosenRow[3].split(":")[1].split(" ")[0])
			self.timeentry.setPeriod(self.chosenRow[3][-2:].lower()[0] + "." + self.chosenRow[3][-2:].lower()[1])
			self.defseat.set(self.chosenRow[5])
			self.defrange.set(self.chosenRow[4])
			self.reservation.set(self.chosenRow[6])
			self.rundate.set(self.chosenRow[7])
			self.profile.set(self.chosenRow[10])
			self.runtimeentry.set12Hrs(self.chosenRow[8].split(":")[0])
			self.runtimeentry.setMins(self.chosenRow[8].split(":")[1])
			self.runtimeentry.setSecs(self.chosenRow[8].split(":")[-1].split(" ")[0])
			self.runtimeentry.setPeriod(self.chosenRow[8][-2:].lower()[0] + "." + self.chosenRow[8][-2:].lower()[1])
			self.runim.set(self.chosenRow[9])
			self.nstop.set(self.chosenRow[11])
			self.duration.set(self.chosenRow[12])
			self.proxy.set(self.chosenRow[13])
		except IndexError as error:
			pass

class CloseButton(ttk.Button):
	def __init__(self, parent):
		super().__init__(parent)
		self.config(text = '< Back', command=lambda : parent.destroy())

class TitleLabel(ttk.Label):
	def __init__(self, parent, text):
		super().__init__(parent)
		font_tuple = ("Comic Sans MS", 20, "bold")
		self.config(text=text, font=font_tuple, anchor="center")

def main():
	
	window = Window()
	window.mainloop()

if __name__ == "__main__":
	if platform == "linux" or platform == "linux2":
		PYLOC = "python"
		PIPLOC = "pip"
	elif platform == "win32":
		PYLOC = PYTHON_EXE
		PIPLOC = os.getcwd() + os.sep + r"venv\Scripts\pip.exe"

main()
