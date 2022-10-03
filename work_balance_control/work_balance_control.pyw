from playsound import *
import tkinter
from tkinter import *
import tkinter as tk
from tkinter import ttk
import getpass
import sys
import os
import pyautogui
from time import sleep
from dataclasses import dataclass
import logging
import configparser

logging.basicConfig(handlers=[logging.FileHandler(os.path.join('work_balance_control.log'), 'w', 'utf-8')], level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%d.%m.%y %H:%M:%S')

config = configparser.ConfigParser()
config.read('work_balance_control.ini')
if not (config.has_section('COMMON') and config.has_section('NOTIFIERS') and config.has_section('SYSTEM')):
    logging.debug('Inactive settings in INI-file')
    sys.exit(1)
if not os.path.isfile(config.get('NOTIFIERS', 'sound_relax_begin')) or not os.path.isfile(config.get('NOTIFIERS', 'sound_relax_end')):
    logging.debug('Check sound settings in INI-file')
    sys.exit(1)
    
@dataclass
class RelaxTimer:
    current_time: int = 1
    current_work_time: int = 1
    work_duration: int = config.getint('COMMON', 'work_duration')
    work_delta: int = config.getint('COMMON', 'work_delta')
    relax_duration: int = config.getint('COMMON', 'relax_duration')
    relax_delta: int = config.getint('COMMON', 'relax_delta')
    relax_warning: int = config.getint('COMMON', 'relax_warning')  
    interrupt_pause: int = config.getint('COMMON', 'interrupt_pause')
    maximum_work_time: int = config.getint('COMMON', 'maximum_work_time')
    maximum_time: int = config.getint('COMMON', 'maximum_time')
    next_relax_time: int = config.getint('COMMON', 'work_duration')
    next_relax_duration: int = config.getint('COMMON', 'relax_duration')
    force_lock: bool = config.getboolean('SYSTEM', 'force_lock')
    fullscreen: bool = config.getboolean('SYSTEM', 'fullscreen')
    topmost: bool = config.getboolean('SYSTEM', 'topmost')
    ## 60 - 1 minute (default), 1 - 1 second (demo)
    timer_clock_cycle: int = config.getint('SYSTEM', 'timer_clock_cycle')
    ## 0 - working, 1 - relaxing, -1 - ending
    relax_state_code: int = 0
    timer_state_active: bool = True

timer = RelaxTimer()
window = Tk(); window.attributes('-fullscreen', timer.fullscreen, '-topmost', timer.topmost); window.overrideredirect(1); window.title('Контроль режима работы и отдыха'); window.geometry('1280x720'); window['bg'] = 'black'
caption = tk.StringVar(); message = tk.StringVar(); comment = tk.StringVar(); summary = tk.StringVar(); answer = tk.StringVar()
answer.set(timer.interrupt_pause)

def window_block():
    pyautogui.moveTo(x=680,y=800)
    window.protocol('WM_DELETE_WINDOW', window_block)
    window.update()

def window_warning():
    pass
    playsound(config.get('NOTIFIERS', 'sound_relax_warning'), False)
    pass
        
def window_hide():
    if window.state() == 'normal':
        playsound(config.get('NOTIFIERS', 'sound_relax_end'), False)
        window.withdraw()

def window_show():
    window.update()
    if window.state() == 'withdrawn':
        playsound(config.get('NOTIFIERS', 'sound_relax_begin'), False)    
        window.deiconify()
        
def window_clicked():
    logging.debug(f'control_interrupted: pause duration {timer.interrupt_pause}')
    timer.interrupt_pause = int(answer.get())
    window_hide()
    sleep(timer.timer_clock_cycle * timer.interrupt_pause)
    window_show()

def window_control_task():
    logging.debug(f'current time {timer.current_time}, current work time {timer.current_work_time}, next relax time {timer.next_relax_time}, next relax duration {timer.next_relax_duration}')
    summary.set(f'Время итого: {timer.current_time} минут / {timer.current_work_time} минут / {timer.current_time - timer.current_work_time} минут (всего/работа/отдых)')

    if timer.relax_warning != 0:
        ## total working time warning
        if timer.current_time == timer.maximum_time  - timer.relax_warning or timer.current_work_time == timer.maximum_work_time - timer.relax_warning:
            logging.debug('total working time warning')       
            window_warning()
        ## current working time warning
        if timer.current_time == timer.next_relax_time - timer.relax_warning:
            logging.debug('current working time warning')       
            window_warning()
            
    ## total working time limit
    if timer.current_time >= timer.maximum_time or timer.current_work_time == timer.maximum_work_time:
        logging.debug('total working time limit')
        timer.relax_state_code = -1
    ## current working time limit
    elif timer.current_time == timer.next_relax_time:
        logging.debug('current working time limit')       
        timer.relax_state_code = 1
    ## current relaxing time limit        
    elif timer.current_time == timer.next_relax_time + timer.next_relax_duration:
        logging.debug('current relaxing time limit')
        timer.relax_state_code = 0
        timer.next_relax_time = timer.current_time + timer.work_duration + timer.work_delta
        timer.next_relax_duration += timer.relax_delta
    else:
        pass

    ## -1 state code - ending
    if timer.relax_state_code == -1:
        timer_state_active = False
        logging.info('ending')
        caption.set(f'Время закончить работу')
        message.set('Пожалуйста, завершите работу. Контроль режима работы и отдыха')
        comment.set('Время выключить ПК')
        window_show()
    ## 1 state code - relaxing
    elif timer.relax_state_code == 1:
        timer_state_active = True
        logging.info('relaxing')        
        caption.set('Время отдыха')
        message.set('Пожалуйста, сделайте перерыв. Контроль режима работы и отдыха')
        comment.set(f'Время отдыха {timer.next_relax_time + timer.next_relax_duration - timer.current_time} минут')
        window_show()
    ## 0 state code - working
    elif timer.relax_state_code == 0:
        timer_state_active = True
        logging.info('working')     
        timer.current_work_time += 1
        caption.set('Время работать')
        message.set('Работайте, не отвлекайтесь. Контроль режима работы и отдыха')
        comment.set(f'Время работы {timer.next_relax_time + timer.next_relax_duration - timer.current_time} минут')
        window_hide()
    else:
        pass

    if timer_state_active:
        timer.current_time += 1
        window.after(1000 * timer.timer_clock_cycle, window_control_task)
    else:
        pass
        
def main():
    base_font_size = int(10 * ((window.winfo_screenwidth()/(1920/100) + window.winfo_screenheight()/(1080/100)) / 2) / 100)
    default_style = ttk.Style(); default_style.configure('New.TButton', font=('Helvetica', base_font_size))
    txt_caption = Label(window, font=('Arial Bold', 3 * base_font_size), fg='red', bg='black', textvariable=caption); txt_caption.grid(column=0, row=0); txt_caption.place(relx = .01, rely = .01)
    txt_message = Label(window, font=('Arial Bold', base_font_size), fg='white', bg='black', textvariable=message); txt_message.grid(column=0, row=0); txt_message.place(relx = .02, rely = .32)
    txt_comment = Label(window, font=('Arial Bold', base_font_size), fg='green', bg='black', textvariable=comment); txt_comment.grid(column=0, row=0); txt_comment.place(relx = .02, rely = .48)
    txt = Entry(window, font = f'Helvetica {base_font_size} bold', textvariable=answer); txt.place(relx = .02, rely = .64, relwidth=.025, relheight=.06)
    btn = Button(window, text='Дайте минуты завершить дела', command=window_clicked); btn.place(relx = .05, rely = .64, relwidth=.2, relheight=.06)
    txt_summary = Label(window, font=('Arial Bold', base_font_size), fg='white', bg='black', textvariable=summary); txt_summary.grid(column=0, row=0); txt_summary.place(relx = .02, rely = .80)    
    window_hide()
    if timer.force_lock:
        window_block()
    window.after(1000 * timer.timer_clock_cycle, window_control_task)
    window.mainloop()

main()
