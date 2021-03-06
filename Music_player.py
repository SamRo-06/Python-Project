from tkinter import *
from tkinter import filedialog
from pygame import *
import os
import pickle


class Player(Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.pack()
        mixer.init()

        if os.path.exists('songs.pickle'):
            with open('songs.pickle', 'rb') as f:
                self.playlist = pickle.load(f)
        else:
            self.playlist = []

        self.current = 0
        self.paused = True
        self.played = False

        self.create_frames()
        self.track_widgets()
        self.control_widgets()
        self.tracklist_widgets()

        self.root.bind('<Left>', self.prev_song)
        self.root.bind('<space>', self.play_pause_song)
        self.root.bind('<Right>', self.next_song)

    def create_frames(self):
        self.track = LabelFrame(self, text='Song Track',font=("Comic Sans", 15, "bold"),bg="coral3", fg="white", bd=5, relief=GROOVE)
        self.track.config(width=410, height=300)
        self.track.grid(row=0, column=0, padx=10)

        self.tracklist = LabelFrame(self, text=f'PlayList - {str(len(self.playlist))}',font=("Comic Sans", 15, "bold"),bg="coral3", fg="white", bd=5, relief=GROOVE)
        self.tracklist.config(width=190, height=400)
        self.tracklist.grid(row=0, column=1, rowspan=3, pady=5)

        self.controls = LabelFrame(self,font=("Comic Sans", 15, "bold"),bg="azure3", fg="white", bd=2, relief=GROOVE)
        self.controls.config(width=410, height=80)
        self.controls.grid(row=2, column=0, pady=5, padx=10)

    def track_widgets(self):
        self.canvas = Label(self.track, image=img)
        self.canvas.configure(width=400, height=240)
        self.canvas.grid(row=0, column=0)

        self.songtrack = Label(self.track, font=("Corbel", 16, "bold"),bg="light cyan", fg="dark slate gray")
        self.songtrack['text'] = 'Music MP3 Player'
        self.songtrack.config(width=30, height=1)
        self.songtrack.grid(row=1, column=0, padx=10)

    def control_widgets(self):
        self.loadSongs = Button(self.controls, bg='coral3', fg='white', font=10)
        self.loadSongs['text'] = 'Load Songs'
        self.loadSongs['command'] = self.retrieve_songs
        self.loadSongs.grid(row=0, column=0, padx=10)

        self.prev = Button(self.controls, image=prev)
        self.prev['command'] = self.prev_song
        self.prev.grid(row=0, column=1)

        self.pause = Button(self.controls, image=pause)
        self.pause['command'] = self.pause_song
        self.pause.grid(row=0, column=2)

        self.next = Button(self.controls, image=next_)
        self.next['command'] = self.next_song
        self.next.grid(row=0, column=3)

        self.volume = DoubleVar(self)
        self.slider = Scale(self.controls, from_=0, to=10, orient=HORIZONTAL)
        self.slider['variable'] = self.volume
        self.slider.set(8)
        mixer.music.set_volume(0.8)
        self.slider['command'] = self.change_volume
        self.slider.grid(row=0, column=4, padx=5)

    def tracklist_widgets(self):
        self.scrollbar = Scrollbar(self.tracklist, orient=VERTICAL)
        self.scrollbar.grid(row=0, column=1, rowspan=5, sticky='ns')

        self.list = Listbox(self.tracklist, selectmode=SINGLE,yscrollcommand=self.scrollbar.set, selectbackground='coral')
        self.enumerate_songs()
        self.list.config(height=22)
        self.list.bind('<Double-1>', self.play_song)

        self.scrollbar.config(command=self.list.yview)
        self.list.grid(row=0, column=0, rowspan=5)

    def retrieve_songs(self):
        self.songlist = []
        directory = filedialog.askdirectory()
        for root_, dirs, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1] == '.mp3':
                    path = (root_ + '/' + file).replace('\\', '/')
                    self.songlist.append(path)

        with open('songs.pickle', 'wb') as f:
            pickle.dump(self.songlist, f)
        self.playlist = self.songlist
        self.tracklist['text'] = f'PlayList - {str(len(self.playlist))}'
        self.list.delete(0, END)
        self.enumerate_songs()

    def enumerate_songs(self):
        for index, song in enumerate(self.playlist):
            self.list.insert(index, os.path.basename(song))

    def play_pause_song(self, event):
        if self.paused:
            self.play_song()
        else:
            self.pause_song()

    def play_song(self, event=None):
        if event is not None:
            self.current = self.list.curselection()[0]
            for i in range(len(self.playlist)):
                self.list.itemconfigure(i, bg="white")

        print(self.playlist[self.current])
        mixer.music.load(self.playlist[self.current])
        self.songtrack['anchor'] = 'w'
        self.songtrack['text'] = os.path.basename(self.playlist[self.current])

        self.pause['image'] = play
        self.paused = False
        self.played = True
        self.list.activate(self.current)
        self.list.itemconfigure(self.current, bg='coral')

        mixer.music.play()

    def pause_song(self):
        if not self.paused:
            self.paused = True
            mixer.music.pause()
            self.pause['image'] = pause
        else:
            if self.played == False:
                self.play_song()
            self.paused = False
            mixer.music.unpause()
            self.pause['image'] = play

    def prev_song(self, event=None):
        self.master.focus_set()
        if self.current > 0:
            self.current -= 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current + 1, bg='white')
        self.play_song()

    def next_song(self, event=None):
        self.master.focus_set()
        if self.current < len(self.playlist) - 1:
            self.current += 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current - 1, bg='white')
        self.play_song()

    def change_volume(self, event=None):
        self.v = self.volume.get()
        mixer.music.set_volume(self.v / 10)


# ----------------------------- Main -------------------------------------------

if __name__ == '__main__':
    root = Tk()
    root.geometry('600x400')
    root.title('Music Player')
    root.resizable(0,0)

    img = PhotoImage(file='m.png')
    next_ = PhotoImage(file='next.gif')
    prev = PhotoImage(file='previous.gif')
    play = PhotoImage(file='play.gif')
    pause = PhotoImage(file='pause.gif')

    app = Player(root)
    app.mainloop()
