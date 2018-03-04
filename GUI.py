import Tix

from googleapiclient.errors import HttpError

import data_gatherer
from tkinter import *
import Tkinter as tki
from textblob import TextBlob
import time
import Tkinter
import tkMessageBox

from visualization import show_data_in_scatter_graph


def show_data(self,message):
    self.root = tki.Tk()

    # create a Frame for the Text and Scrollbar
    txt_frm = tki.Frame(self.root, width=600, height=600)
    txt_frm.pack(fill="both", expand=True)
    # ensure a consistent GUI size
    txt_frm.grid_propagate(False)
    # implement stretchability
    txt_frm.grid_rowconfigure(0, weight=1)
    txt_frm.grid_columnconfigure(0, weight=1)

    # create a Text widget
    self.txt = tki.Text(txt_frm, borderwidth=3, relief="sunken")
    self.txt.config(font=("consolas", 12), undo=True, wrap='word')
    self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
    self.txt.insert(INSERT, message)
    # create a Scrollbar and associate it with txt
    scrollb = tki.Scrollbar(txt_frm, command=self.txt.yview)
    scrollb.grid(row=0, column=1, sticky='nsew')
    self.txt['yscrollcommand'] = scrollb.set

def search_lyrics():
   ans = data_gatherer.get_lyrics_and_youtube_comments(e1.get(),e2.get())
   scores = semantic_analyser(e1.get(),e2.get())
   if(scores[0] != 0):
        data_to_show = "Song NLP score: " + str(scores[0])+"\nSong lyrics:\n" +ans[0] +"\nComments NLP score: " + \
                  str(scores[1])+"\nComments:\n\n"
        for i in range (0,len(ans[1])):
            data_to_show+= ans[1][i] + "\n"
        show_data(master,data_to_show)
   else: tkMessageBox.showinfo("Error", "We are sorry this song couldn't be found")



def semantic_analyser(artist,song_name):
    lyric_plus_comment=[]

    lyrics_plus_commments = data_gatherer.get_lyrics_and_youtube_comments(artist, song_name.replace(unichr(226), ""))

    lyrics = lyrics_plus_commments[0]
    comments = lyrics_plus_commments[1]
    if (lyrics[:18] != "Exception occurred"):
        semantic_result_lyrics =TextBlob(lyrics.replace("\n", " ").replace("\r", "").replace(unichr(226), "")).sentiment.polarity
        j=1
        sum_for_average_score=0
        if (comments != None):
            for comment in comments:
                score = TextBlob(comment.replace("\n", "").replace("\r", "")).sentiment.polarity
                if (score != 0 ):
                    sum_for_average_score +=score
                    j+=1
        score_avg = sum_for_average_score / j
    else: return [0,0]
    lyric_plus_comment.append(semantic_result_lyrics)
    lyric_plus_comment.append(score_avg)
    return lyric_plus_comment


def apply_on_all_lyrics_semantic_analyser():

    files = []
    if var1.get():
        files.append("rock.txt")
    if var2.get():
        files.append("pop.txt")
    if var3.get():
        files.append("metal.txt")
    if var4.get():
        files.append("reggae.txt")
    if var5.get():
        files.append("jazz.txt")
    big_array={}
    for file in files:
        with open(file, 'r') as ins:
            lyrics_name = ins.read()
            lyrics_name_array = lyrics_name.split("%%")
            temp_array = []
        for song_name_and_artist in lyrics_name_array:
            artist_and_song_name = song_name_and_artist.split("$$")
            if (len(artist_and_song_name)==2):
                artist= artist_and_song_name[0].replace("\n","").replace("\r","")
                song_name = artist_and_song_name[1].replace("\n","").replace("\r","")

                temp_array.append(semantic_analyser(artist, song_name))
        big_array[file[:-4]]= temp_array
    show_data_in_scatter_graph(big_array)

def add():
    add_to_file(e1.get(),e2.get(),e3.get())

def add_to_file(artist, song_name, genre):
    scores = semantic_analyser(artist, song_name)
    if (scores[0] != 0):
        if genre in ['metal', 'pop', 'jazz', 'reggae', 'rock']:
            with open(genre + ".txt" , 'a') as file:
                file.write("\n" + artist + "$$" + song_name + "%%")
                print("", "Added song successfully")
        else: print("Error", "Please try again!\n Genre can only be: metal, rock, pop, jazz, reggae")
    else:
        print("Error", "We are sorry this song couldn't be found")


# def add_songs():
#     with open("blah.txt" ,'r') as file:
#         for i in range(0, 100):
#             file.readline()
#             file.readline()
#
#             song_name = file.readline().replace("\n","")
#             artist = file.readline().replace("\n","")
#             add_to_file(artist.replace("\n","").replace("\r",""), song_name.replace("\n","").replace("\r",""), "jazz")



master = Tk()

master.title("SEMANTIC LYRICS")

var1 = IntVar()

ch1 = Checkbutton(master, text="Rock", variable=var1).grid(row=0, sticky=W)

var2 = IntVar()
Checkbutton(master, text="Pop" ,variable=var2).grid(row=1, sticky=W)
var3 = IntVar()
Checkbutton(master, text="Metal", variable=var3).grid(row=0,column=15 ,sticky=W)
var4 = IntVar()
Checkbutton(master, text="Reggae", variable=var4).grid(row=1, column=15 ,sticky=W)
var5 = IntVar()
Checkbutton(master, text="Jazz", variable=var5).grid(row=0,column=30 , sticky=W)

#master.geometry('350x200')
Label(master, text="Artist").grid(row=5)
Label(master, text="Song name").grid(row=10)
Label(master, text="Genre").grid(row=15)

e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)

e1.grid(row=5, column=100)
e2.grid(row=10, column=100)
e3.grid(row=15, column=100)

Button(master, text='Quit', command=master.quit).grid(row=200, column=1, sticky=W, pady=4)
Button(master, text='Add song', command=add).grid(row=200, column=20, sticky=W, pady=4)
Button(master, text='Apply', command=apply_on_all_lyrics_semantic_analyser).grid(row=200, column=30, sticky=W, pady=4)
Button(master, text='Search', command=search_lyrics).grid(row=200, column=40, sticky=W, pady=4)

mainloop( )