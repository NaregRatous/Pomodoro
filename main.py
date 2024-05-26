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
timer = ""
door = True
SOUND_NAME = "Ocean Waves.mp3"  # default value
SOUND_VOLUME = 0.5
pause_flag = False
global_count = 0
# ---------------------------- PLAY MUSIC -------------------------------- #
# for test from laptop to github

def play_count_down_music():
    # Play the music file
    pygame.mixer.init()
    print(SOUND_NAME)
    print(SOUND_VOLUME)
    pygame.mixer.music.load(SOUND_NAME)  # Light Rain with bg or Ocean Waves
    pygame.mixer.music.set_volume(SOUND_VOLUME)  # Set the volume to 50%
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
    global door, global_count
    global_count = 0
    window.after_cancel(timer)
    stop_music()
    door = True
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    check_marks.config(text="")
    global reps
    reps = 0


def settings():
    global SOUND_NAME, WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN, SOUND_VOLUME
    local_sound_name = SOUND_NAME[:-4]
    settings_window = Toplevel(window)
    settings_window.config(padx=100, pady=50, bg=YELLOW)
    settings_window.title("Settings")

    work_min_label = Label(settings_window, text="Work Min=",  fg=RED, bg=YELLOW, font=(FONT_NAME, 12))
    work_min_label.grid(column=0, row=0)
    work_min_entry = Entry(settings_window, width=10)
    work_min_entry.insert(0, str(WORK_MIN))  # This line displays the current work min
    work_min_entry.grid(column=1, row=0)

    short_break_label = Label(settings_window, text="Short Break Min=", fg=RED, bg=YELLOW, font=(FONT_NAME, 12))
    short_break_label.grid(column=0, row=1)
    short_break_entry = Entry(settings_window, width=10)
    short_break_entry.insert(0, str(SHORT_BREAK_MIN))  # This line displays the current short break min
    short_break_entry.grid(column=1, row=1)

    long_break_label = Label(settings_window, text="Long Break Min=", fg=RED, bg=YELLOW, font=(FONT_NAME, 12))
    long_break_label.grid(column=0, row=2)
    long_break_entry = Entry(settings_window, width=10)
    long_break_entry.insert(0, str(LONG_BREAK_MIN))  # This line displays the current long break min
    long_break_entry.grid(column=1, row=2)

    ticking_sound_label = Label(settings_window, text="Ticking Sound", fg=RED, bg=YELLOW, font=(FONT_NAME, 12))  # This
    # line adds the "Ticking Sound" label
    ticking_sound_label.grid(column=0, row=3)

    ticking_sound_var = StringVar(settings_window)
    ticking_sound_var.set(local_sound_name)  # set the last selected item
    ticking_sound_menu = OptionMenu(settings_window, ticking_sound_var, "Ocean Waves", "Light Rain1", "Light Rain2",
                                    "Sea1", "Heavy Rain1")
    ticking_sound_menu.grid(column=1, row=3)

    sound_volume_label = Label(settings_window, text="Sound Volume", fg=RED, bg=YELLOW, font=(FONT_NAME, 12))
    sound_volume_label.grid(column=0, row=4)

    volume_var = DoubleVar()
    volume_var.set(SOUND_VOLUME)
    volume_slider = Scale(settings_window, from_=0, to=1, orient=HORIZONTAL, variable=volume_var, resolution=0.01)
    volume_slider.grid(column=1, row=4)

    def save():
        global WORK_MIN, SHORT_BREAK_MIN, LONG_BREAK_MIN, SOUND_NAME, SOUND_VOLUME
        try:
            WORK_MIN = int(work_min_entry.get())
            SHORT_BREAK_MIN = int(short_break_entry.get())
            LONG_BREAK_MIN = int(long_break_entry.get())
            SOUND_NAME = ticking_sound_var.get()
            SOUND_NAME = f"{SOUND_NAME}.mp3"
            SOUND_VOLUME = volume_var.get()
            settings_window.destroy()  # This line closes the window after saving the values
        except ValueError:
            print("Please enter a valid integer for all entries.")

    def quit_settings():
        settings_window.destroy()

    save_button = Button(settings_window, text="Save", command=save)
    save_button.grid(column=0, row=5)

    quit_button = Button(settings_window, text="Quit", command=quit_settings)
    quit_button.grid(column=1, row=5)
# ---------------------------- TIMER MECHANISM ------------------------------- # 


def pause_timer():
    global pause_flag
    pause_flag = True
    stop_music()


def start_timer():
    global reps, global_count, pause_flag
    pause_flag = False
    if global_count == 0:
        reps += 1
        work_sec = WORK_MIN * 60
        short_break_sec = SHORT_BREAK_MIN * 60
        long_break_sec = LONG_BREAK_MIN * 60
        if reps == 1 or reps == 3 or reps == 5 or reps == 7:
            title_label.config(text="Work", fg=GREEN)
            count_down(work_sec)
        elif reps == 2 or reps == 4 or reps == 6:
            title_label.config(text="Break", fg=PINK)
            count_down(short_break_sec)
        else:
            title_label.config(text="break", fg=RED)
            count_down(long_break_sec)
            reps = 0
    else:
        count_down(global_count)
        play_count_down_music()


music_thread = threading.Thread(target=play_count_down_music)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(count):
    global reps, global_count
    global_count = count
    if not pause_flag:
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
                count_min = WORK_MIN
                canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
            elif reps == 1 or reps == 3 or reps == 5:
                title_label.config(text="Break", fg=PINK)
                count_min = SHORT_BREAK_MIN
                canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
            else:
                title_label.config(text="break", fg=RED)
                count_min = LONG_BREAK_MIN
                canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

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

pause_button = Button(text="Pause", highlightthickness=0, command=pause_timer)
pause_button.grid(column=0, row=3)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

settings_button = Button(text="Settings", highlightthickness=0, command=settings)
settings_button.grid(column=1, row=2)

check_marks = Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)


window.mainloop()
