from tkinter import *
import pygame
import threading
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 30
reps = 0
timer = None
door = True

# ---------------------------- PLAY MUSIC -------------------------------- #
def play_count_down_music():
    # Play the music file
    pygame.mixer.init()
    pygame.mixer.music.load('Ocean Waves.mp3') # Light Rain with bg or Ocean Waves
    pygame.mixer.music.set_volume(0.5)  # Set the volume to 50%
    pygame.mixer.music.play(-1)

def play_timer_up_music():
    # Play the music file
    pygame.mixer.init()
    pygame.mixer.music.load('Timer up.mp3')
    pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()
# ---------------------------- TIMER RESET ------------------------------- # 

def reset_timer():
    global door
    window.after_cancel(timer)
    stop_music()
    door = True
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    check_marks.config(text="")
    global reps
    reps = 0

def settings():
    settings_window = Toplevel(window)
    settings_window.config(padx=100, pady=50, bg=YELLOW)
    settings_window.title("Settings")

    work_min_label = Label(settings_window, text="Work Min=",  fg=RED, bg=YELLOW, font=(FONT_NAME, 12))
    work_min_label.grid(column=0, row=0)
    work_min_entry = Entry(settings_window, width=10)
    work_min_entry.insert(0, WORK_MIN)  # This line displays the current work min
    work_min_entry.grid(column=1, row=0)

    short_break_label = Label(settings_window, text="Short Break Min=", fg=RED, bg=YELLOW, font=(FONT_NAME, 12))
    short_break_label.grid(column=0, row=1)
    short_break_entry = Entry(settings_window, width=10)
    short_break_entry.insert(0, SHORT_BREAK_MIN)  # This line displays the current short break min
    short_break_entry.grid(column=1, row=1)

    long_break_label = Label(settings_window, text="Long Break Min=", fg=RED, bg=YELLOW, font=(FONT_NAME, 12))
    long_break_label.grid(column=0, row=2)
    long_break_entry = Entry(settings_window, width=10)
    long_break_entry.insert(0, LONG_BREAK_MIN)  # This line displays the current long break min
    long_break_entry.grid(column=1, row=2)

    def save():
        global WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN
        try:
            WORK_MIN = int(work_min_entry.get())
            SHORT_BREAK_MIN = int(short_break_entry.get())
            LONG_BREAK_MIN = int(long_break_entry.get())
            settings_window.destroy()  # This line closes the window after saving the values
        except ValueError:
            print("Please enter a valid integer for all entries.")

    def quit():
        settings_window.destroy()

    save_button = Button(settings_window, text="Save", command=save)
    save_button.grid(column=0, row=3)

    quit_button = Button(settings_window, text="Quit", command=quit)
    quit_button.grid(column=1, row=3)
# ---------------------------- TIMER MECHANISM ------------------------------- # 

def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    if reps ==1 or reps ==3 or reps == 5 or reps == 7:
        title_label.config(text="Work", fg=GREEN)
        count_down(work_sec)
    elif reps == 2 or reps ==4 or reps == 6:
        title_label.config(text="Break", fg=PINK)
        count_down(short_break_sec)
    else:
        title_label.config(text="break", fg=RED)
        count_down(long_break_sec)
        reps = 0

music_thread = threading.Thread(target=play_count_down_music)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global reps
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:

        global timer
        timer = window.after(1000, count_down, count - 1)
        global door

        if door:
            play_count_down_music()
            door = False

    else:
        door = True
        stop_music()
        play_timer_up_music()
        if reps == 0 or reps == 2 or reps == 4 or reps == 6:
            title_label.config(text="Work", fg=GREEN)
        elif reps == 1 or reps == 3 or reps == 5:
            title_label.config(text="Break", fg=PINK)
        else:
            title_label.config(text="break", fg=RED)

        marks = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)
        window.attributes('-topmost', 1)  # This line brings the window to the front
        window.attributes('-topmost', 0)  # This line makes other windows accessible after 1 second




# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)


title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

settings_button = Button(text="Settings", highlightthickness=0, command=settings)
settings_button.grid(column=1, row=2)

check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)






window.mainloop()











