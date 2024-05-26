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
    pygame.mixer.music.load('Light Rain with bg.mp3')
    pygame.mixer.music.set_volume(0.25)  # Set the volume to 50%
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

check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)






window.mainloop()











