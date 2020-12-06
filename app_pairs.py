import tkinter
import random
from playsound import playsound
from app_db_control import engine, Track, Pair
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

root = tkinter.Tk()
root.title('minimal pairs training')
root.minsize(width=450, height=220)
# root.geometry("450x220")
# root.resizable(0, 0)
frame = tkinter.Frame(root)
frame.pack()

def draw():
    session = Session()
    draw = random.choice(session.query(Pair).all())
    tracks = [[track.name, track.path] for track in draw.tracks]
    labels = [tracks[0][0], tracks[1][0]]
    answer = random.choice(tracks)
    answer, path = answer[0], answer[1]
    session.close()
    return labels, answer, path


def construct(labels, answer, path):
    def clr():
        label.destroy()
        btn_sound.destroy()
        option_1.destroy()
        option_2.destroy()
        root.unbind_all('<space>')
        root.unbind_all('<a>')
        root.unbind_all('<d>')

    choice_1, choice_2 = [lambda event=None, label=label: [clr(), check_answer(label, answer)] for label in labels]
    # choice_1 = lambda event=None: [clr(), check_answer(labels[0], answer)]
    # choice_2 = lambda event=None: [clr(), check_answer(labels[1], answer)]

    label = tkinter.Label(frame, text=f'{labels[0]}  /  {labels[1]}', width=35, height=10)
    btn_sound = tkinter.Button(frame, text='Replay sound\n<space>', command=lambda: playsound(path), width=10, height=3)
    option_1 = tkinter.Button(frame, text=f'{labels[0]}\n<a>', width=12, height=3, command=choice_1)
    option_2 = tkinter.Button(frame, text=f'{labels[1]}\n<d>', width=12, height=3, command=choice_2)

    label.grid(row=0, column=1)
    btn_sound.grid(row=1, column=1)
    option_1.grid(row=1, column=0)
    option_2.grid(row=1, column=2)

    root.bind_all('<space>', lambda event: playsound(path))
    root.bind_all('<a>', choice_1)
    root.bind_all('<d>', choice_2)
    # playsound(path)
    root.after(50, lambda: playsound(path))


def start_msg(msg_text, btn_text):
    def clr():
        label_start.destroy()
        btn_start.destroy()
        root.unbind_all('<space>')

    start = lambda event=None: [clr(), construct(*draw())]

    label_start = tkinter.Label(frame, text=msg_text, width=60, height=10)
    btn_start = tkinter.Button(frame, text=f'{btn_text}\n<space>', command=start, width=12, height=3)

    label_start.grid(row=0, column=1)
    btn_start.grid(row=1, column=1)

    root.bind_all('<space>', start)


def check_answer(label, answer):
    if label == answer:
        msg = f'{label}\n\nis\nCORRECT'
    else:
        msg = f'{label}\n\nis\nincorrect ;('
    btn_msg = 'Next'
    start_msg(msg, btn_msg)


start_message = 'Hello, let\'s begin'
btn_msg = 'Start'
start_msg(start_message, btn_msg)

root.mainloop()
