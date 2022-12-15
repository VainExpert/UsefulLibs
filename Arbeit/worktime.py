from tkinter import *
from tkinter import ttk
import winsound
import time
import os.path

#Read Log-File into Log
def read_log():
    global table

    count = 0
    with open("log.txt", "r") as f:
        for line in f:
            vals = line.rstrip().split(' ')
            table.insert(parent = '', index = 'end', iid = count, text = '', 
                values = (vals[0], vals[1], vals[2], vals[3], vals[4]))
            count += 1

#Init Window
ws = Tk()
ws.geometry('512x512')
ws.title('Arbeitszeit')
ws.config(bg='#299617')
ws.resizable(0, 0)

style = ttk.Style(ws)
style.configure('TNotebook.Tab', width=ws.winfo_screenwidth())

#Init Tabs
tab_control = ttk.Notebook(ws)
timer_tab = Frame(tab_control)
log_tab = Frame(tab_control)
options_tab = Frame(tab_control)

tab_control.add(timer_tab, text = "Timer")
tab_control.add(log_tab, text = "Log")
tab_control.add(options_tab, text = "Optionen")

tab_control.pack(expand = 1, fill = "both")

#Labels for Log
table = ttk.Treeview(log_tab, height = 512)
table['columns'] = ('date', 'worktime', 'pausetime', 'money', 'file')

table.column("#0", width=0,  stretch=NO)
table.column('date', anchor=CENTER, width=80)
table.column('worktime', anchor=CENTER, width=80)
table.column('pausetime', anchor=CENTER, width=80)
table.column('money', anchor=CENTER, width=80)
table.column('file', anchor=CENTER, width=80)

table.heading("#0",text="",anchor=CENTER)
table.heading('date', text='Datum', anchor=CENTER)
table.heading('worktime', text='Arbeitszeit', anchor=CENTER)
table.heading('pausetime', text='Pausenzeit', anchor=CENTER)
table.heading('money', text='Lohn', anchor=CENTER)
table.heading('file', text='Zeitprotokoll', anchor=CENTER)

if os.path.isfile("log.txt") and os.access("log.txt", os.R_OK):
    read_log()

table.pack(fill = 'both')

#Labels and Buttons for Options
options_tab.columnconfigure(tuple(range(3)), weight = 1)
options_tab.rowconfigure(tuple(range(6)), weight = 1)

alarm = IntVar(ws, 1)
lbl_title = Label(options_tab, text = 'Einstellungen', font = "Verdana 20 bold")

lbl_wage = Label(options_tab, text = 'Studenlohn:', font = 'Verdana 10')
lbl_max_ptime = Label(options_tab, text = 'Maximale Gesamtpausenzeit (h):', font = 'Verdana 10')
lbl_max_contptime = Label(options_tab, text = 'Maximale Pausenzeit (min) am Stück:', font = 'Verdana 10')
lbl_max_wtime = Label(options_tab, text = 'Maximale Arbeitszeit (h):', font = 'Verdana 10')
lbl_alarmbool = Label(options_tab, text = 'Zeitenalarm:', font = 'Verdana 10')

slide_wage = Scale(options_tab, from_ = 12, to = 100, orient = HORIZONTAL, length = 180)
slide_maxptime = Scale(options_tab, from_ = 0, to = 3, orient = HORIZONTAL, length = 180)
slide_max_contptime = Scale(options_tab, from_ = 0, to = 60, orient = HORIZONTAL, length = 180)
slide_maxwtime = Scale(options_tab, from_ = 1, to = 16, orient = HORIZONTAL, length = 180)
check_alarm = Checkbutton(options_tab, variable = alarm)

slide_wage.set(25)
slide_maxptime.set(2)
slide_max_contptime.set(45)
slide_maxwtime.set(8)

lbl_title.grid(column = 0, row = 0)
lbl_wage.grid(column = 0, row = 1, pady = 20, padx = 5, sticky = W)
lbl_max_ptime.grid(column = 0, row = 2, pady = 20, padx = 5, sticky = W)
lbl_max_contptime.grid(column = 0, row = 3, pady = 20, padx = 5, sticky = W)
lbl_max_wtime.grid(column = 0, row = 4, pady = 20, padx = 5, sticky = W)
lbl_alarmbool.grid(column = 0, row = 5, pady = 20, padx = 5, sticky = W)

slide_wage.grid(column = 2, row = 1, pady = 20, padx = 20, columnspan = 2)
slide_maxptime.grid(column = 2, row = 2, pady = 20, padx = 20, columnspan = 2)
slide_max_contptime.grid(column = 2, row = 3, pady = 20, padx = 20, columnspan = 2)
slide_maxwtime.grid(column = 2, row = 4, pady = 20, padx = 20, columnspan = 2)
check_alarm.grid(column = 2, row = 5, pady = 20, padx = 20)

#Init Global Variables for Time
minutes = 0
hours = 0
pmin = 0
phours = 0

tempwmin = 0
tempwh = 0
temppmin = 0
tempph = 0

pausetimes = []
worktimes = []

state = 0

wage = slide_wage.get()
max_ptime = slide_maxptime.get()
max_contptime = slide_max_contptime.get()
max_wtime = slide_maxwtime.get()

#Calculate made money
def calc_money():
    global hours, minutes, wage
    money = 0

    money = hours * wage
    if minutes < 15:
        return money
    elif minutes > 45:
        return money + wage
    else:
        return money + ((minutes / 60) * wage)

#format minutes and hours to display correctly
def format_time(hours, minutes):
    if minutes < 10:
        displaymin = "0" + str(minutes)
    else:
        displaymin = str(minutes)
            
    if hours < 10:
        displayh = "0" + str(hours)
    else:
        displayh = str(hours)
    
    return displayh + ":" + displaymin

#Save times to file
def save_protocol():
    global worktimes, pausetimes

    with open('{}.txt'.format(time.strftime('%Y-%m-%d', time.localtime())), 'w') as f:
        f.write("{}\n".format(worktimes[0][0]))
        f.write("Arbeitszeiten:\n")
        
        count = 0
        for element in worktimes:
            if(len(element) > 1):
                f.write("{}. {} {} ".format(count, element[0], element[1]))
                count += 1
        
        count = 0
        f.write("Pausenzeiten:\n")
        for element in pausetimes:
            if len(element) > 1:
                f.write("{}. {} {} ".format(count, element[0], element[1]))
                count += 1
        
        f.write("\nGesamte Arbeitszeit: {}".format(worktimes[-1][0]))
        f.write("\nGesamte Pausenzeit: {}".format(pausetimes[-1][0]))
        f.write("\nGesamter Lohn: {}".format(calc_money()))

        f.write("\nSession Einstellungen:")
        f.write("\Maximale Pausenzeit: {}".format(max_ptime))
        f.write("\nMaximale Pausenzeit am Stück: {}".format(max_contptime))
        f.write("\nMaximale Arbeitszeit: {}".format(max_wtime))

        global curr_file
        curr_file = f.name

#Save Log
def save_log():
    global hours, minutes
    global phours, pmin
    global curr_file

    table.insert(parent = '', index = 'end', iid = 0, text = '', 
        values = (time.strftime('%d-%m-%Y', time.localtime()), format_time(hours, minutes), format_time(phours, pmin), calc_money(), curr_file))

    with open("log.txt", "a") as f:
        f.write("{} {} {} {} {}\n".format(time.strftime('%d-%m-%Y', time.localtime()), format_time(hours, minutes), format_time(phours, pmin), calc_money(), curr_file))

#Pop-Up Window
def popup_msg(msg):
    popup = Tk()
    popup.wm_title("Achtung!")
    label = ttk.Label(popup, text = msg, font = "Verdana 10")
    label.pack(side = "top", fill = "x", pady = 10)
    bttn = ttk.Button(popup, text = "Okay", command = popup.destroy)
    bttn.pack()
    popup.mainloop()

#Main Clock Function (Counter)
def clock_lbl(lbl):
    def clock():
        global hours, minutes

        if state == 1:
            if minutes >= max_contptime:
                if alarm:
                    for i in range(3):
                        winsound.Beep(2000,500)
                popup_msg("Maximale Pausenzeit erreicht! Zeit zu arbeiten!")

            if hours >= max_ptime:
                if alarm:
                    for i in range(5):
                        winsound.Beep(1000,500)
                popup_msg("Keine Pausenzeit mehr! Zeit zu arbeiten!")

        elif state == 2:
            if hours >= max_wtime:
                if alarm:
                    for i in range(7):
                        winsound.Beep(1000, 500)
                popup_msg("Maximale Arbeitszeit erreicht! Zeit für eine Pause!")

        if minutes == 60:
            minutes = 0
            hours += 1

        display = format_time(hours, minutes)
        lbl['text'] = display
            
        lbl.after(60000, clock)    
        minutes += 1
    clock()     

#Start clock function
def start_work(lbl, lbl_crr):
    start_btn['text'] = 'Ende'
    start_btn['command'] = lambda:end_work(lbl, lbl_current)
    pause_btn['state'] = 'normal'
    lbl_crr['text'] = 'Arbeit'

    global worktimes, state
    worktimes.append([time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())])
    state = 2

    clock_lbl(lbl)

#Stop Clock Function
def end_work(lbl, lbl_crr):
    global temppmin, tempph
    global tempwmin, tempwh
    global minutes, hours
    global pmin, phours
    global worktimes, pausetimes
    global table, state

    worktimes.append([time.strftime("%H:%M:%S", time.localtime()), format_time(hours, minutes)])
    worktimes.append([format_time(hours, minutes)])
    pausetimes.append([format_time(phours, pmin)])
    
    save_protocol()
    save_log()
    
    minutes = 0
    hours = 0
    pmin = 0
    phours = 0
    tempph = 0
    temppmin = 0
    tempwh = 0
    tempwmin = 0

    start_btn['text'] = 'Start'
    start_btn['command'] = lambda:start_work(lbl, lbl_current)
    pause_btn['state'] = 'disabled'
    lbl['text'] = '00:00'
    lbl_crr['text'] = 'Warte'
    state = 0

#Pause Clock Function and Start from 0 again
def pause_work(lbl, lbl_crr):
    start_btn['state'] = 'disabled'
    pause_btn['text'] = 'Weiter'
    pause_btn['command'] = lambda:continue_work(lbl, lbl_current)
    lbl_crr['text'] = 'Pause'
    
    global temppmin, tempph
    global tempwmin, tempwh
    global minutes, hours
    global worktimes, state

    worktimes.append([time.strftime("%H:%M:%S", time.localtime()), format_time(hours, minutes)])
    state = 1

    tempwmin = minutes
    tempwh = hours
    minutes = temppmin
    hours = tempph
    clock_lbl(lbl)

#Continue clock function from previous worktime
def continue_work(lbl, lbl_crr):
    start_btn['state'] = 'normal'
    pause_btn['text'] = 'Pause'
    pause_btn['command'] = lambda:pause_work(lbl, lbl_current)
    lbl_crr['text'] = 'Arbeit'
    
    global temppmin, tempph
    global tempwmin, tempwh
    global minutes, hours
    global pmin, phours
    global pausetimes, state

    pausetimes.append([time.strftime("%H:%M:%S", time.localtime()), format_time(hours, minutes)])
    state = 2

    temppmin = minutes
    tempph = hours
    pmin += temppmin
    phours += tempph
    minutes = tempwmin
    hours = tempwh
    clock_lbl(lbl)

#Init Background and Label
bg = PhotoImage(file = 'uhr.png')
img = Label(timer_tab, image = bg)
img.pack(fill = 'both')

lbl = Label(
    timer_tab, 
    text = "00:00",
    font = "Verdana 30 bold"
    )

lbl_time = Label(
    timer_tab, 
    text = "Stunden", 
    foreground = "black", 
    font = "Verdana 20 bold"
    )

lbl_current = Label(
    timer_tab, 
    text = "Warte", 
    foreground = "black", 
    font = "Verdana 20 bold"
    )

lbl.place(x = 188, y = 335)
lbl_time.place(x = 188, y = 385)
lbl_current.place(x = 10, y = 15)

#Init Buttons
start_btn = Button(
    timer_tab, 
    text = 'Start', 
    width = 15, 
    command = lambda:start_work(lbl, lbl_current)
    )

pause_btn = Button(
    timer_tab, 
    text = 'Pause', 
    width = 15, 
    state = 'disabled', 
    command = lambda:pause_work(lbl, lbl_current)
    )

start_btn.place(x = 135, y = 440)
pause_btn.place(x = 255, y = 440)

ws.mainloop()