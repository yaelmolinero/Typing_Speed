import random
from tkinter import *
from tkinter import ttk
from random import sample

TIMER = 60
WPM_SCORE = 0
CPM_SCORE = 0
FAILED = 0
id_word = 0
again = None
is_started = False
list_words = []

def random_words():
    global list_words

    list_words = []
    words.delete('1.0', END)

    with open("./random_words.txt", encoding="utf8") as file:
        for line in file.readlines():
            w = line.replace('\n', '')
            list_words.append(w)
        list_words = sample(list_words, 500)
        for w in list_words:
            words.insert(END, f"{w} ")

def select_word():
    text_input.set(value="")
    size = len(list_words[id_word])
    words.tag_remove('select', "1.0", END)
    words.tag_add('select', f"1.{pos}", f"1.{pos + size + 1}")
    words.see(f"1.{pos + 150}")

def change_word():
    global pos
    for n in range(20):
        pos += 1
        if words.get(f"1.{pos}") == " ":
            break

def writing(event):
    global pos, is_started, WPM_SCORE, CPM_SCORE, FAILED, id_word
    letter = f"1.{pos}"
    char = event.keysym

    if not is_started:
        is_started = True
        count_down()

    if char == "space":
        check_word()
        update_score()
        id_word += 1
        if words.get(f"1.{pos}") != " ":
            change_word()
        select_word()

    elif len(char) > 1:
        return
    elif char.lower() == words.get(letter).lower():
        words.tag_add('good', letter)
        CPM_SCORE += 1
    else:
        words.tag_add('wrong', letter)
        FAILED += 1
        mistakes.configure(text=f"{FAILED:02d}")
    pos += 1

def deleting(event):
    global pos
    if len(typing.get()) <= 0:
        return
    else:
        pos -= 1

        letter = f"1.{pos}"
        words.tag_remove('good', letter)
        words.tag_remove('wrong', letter)

def check_word():
    global WPM_SCORE

    last_word = typing.get().strip()
    if last_word == list_words[id_word]:
        WPM_SCORE += 1

def update_score():
    wpm.configure(text=f"{WPM_SCORE:02d}")
    cpm.configure(text=f"{CPM_SCORE:02d}")

def count_down():
    global TIMER, again
    TIMER -= 1

    if TIMER >= 0:
        timer.configure(text=f"{TIMER:02d}")
        again = window.after(1000, count_down)
    else:
        typing.state(['disabled'])

def reset():
    global TIMER, WPM_SCORE, CPM_SCORE, FAILED, id_word, again, is_started, pos
    TIMER, WPM_SCORE, CPM_SCORE, FAILED = 60, 0, 0, 0
    id_word, pos, is_started = 0, 0, False

    if again is None:
        return

    timer.configure(text="60")
    words.tag_remove('good', "1.0", END)
    words.tag_remove('wrong', "1.0", END)
    words.tag_remove('select', "1.0", END)

    update_score()
    mistakes.configure(text=f"00")
    random_words()
    select_word()
    window.after_cancel(again)
    typing.state(['!disabled'])
    typing.focus()


# --------------- INITIALIZE WINDOW --------------- #
window = Tk()
window.title("Typing Speed Test")
window.geometry("900x500")
window.resizable(False, False)
window.configure(bg="#202020", padx=100, pady=50)

# --------------- STYLE WIDGETS --------------- #
s = ttk.Style()
s.theme_use('alt')

s.configure('resetBtn.TButton', background='#2C2C2C', foreground='#fff', borderwidth=0,
            font=('Arial', 12))
s.map('resetBtn.TButton', background=[('active', '#3E3E3E')])

s.configure('score.TLabel', background='#2C2C2C', foreground='#fff', font=('Arial', 22, 'bold'),
            padding=20, relief='flat')
s.configure('tags.TLabel', background='#202020', foreground='#fff', font=('Arial', 14, 'bold'),
            padding=20, relief='flat')
s.configure('invisible.TLabel', background='#202020', foreground='#202020')

s.configure('TEntry', fieldbackground='#2C2C2C', background='blue', foreground='#fff',
            font=('Arial', 14), padding=5, relief='solid')

# --------------- TIMER --------------- #
timer = ttk.Label(window, text='60', style='score.TLabel')
timer.grid(row=0, column=0)
ttk.Label(window, text="seconds", style='tags.TLabel').grid(row=1, column=0)

# --------------- SCORE --------------- #
ttk.Label(window, text="invisible", style='invisible.TLabel').grid(row=0, column=1)

wpm = ttk.Label(window, text="00", style='score.TLabel')
wpm.grid(row=0, column=2)
ttk.Label(window, text="WPM", style='tags.TLabel').grid(row=1, column=2)

cpm = ttk.Label(window, text="00", style='score.TLabel')
cpm.grid(row=0, column=3)
ttk.Label(window, text="CPM", style='tags.TLabel').grid(row=1, column=3)

mistakes = ttk.Label(window, text="00", style='score.TLabel')
mistakes.grid(row=0, column=4)
ttk.Label(window, text='Mistakes', style='tags.TLabel').grid(row=1, column=4)

reset_btn = ttk.Button(window, text='Reset', command=reset, style='resetBtn.TButton')
reset_btn.grid(row=2, column=4, sticky='e')

# --------------- SHOW WORDS --------------- #
pos = 0
words = Text(window, width=60, height=5, autoseparators=True)
words.configure(font=('Arial', 14, 'bold'), fg='#999999', bg='#2C2C2C', pady=25, padx=15,
                borderwidth=0)
words.grid(row=3, column=0, columnspan=5, sticky='we')
words.tag_config('select', foreground='#fff')
words.tag_config('good', foreground='#3AFF00')
words.tag_config('wrong', foreground='#FF1500')

random_words()

# --------------- ENTRY --------------- #
text_input = StringVar()
typing = ttk.Entry(window, textvariable=text_input, style='write.TEntry', justify=CENTER)
typing.grid(row=4, column=0, columnspan=5, pady=15, sticky='we')
typing.focus()
typing.bind('<Key>', writing)
typing.bind('<BackSpace>', deleting)

select_word()
words.see('1.0')
window.mainloop()
