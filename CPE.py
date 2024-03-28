import tkinter as tk

from tkinter import filedialog
from tkinter import  *
from tkinter import ttk
from PIL import ImageTk,Image
import os
from shutil import copy2
import shutil
import ntpath
from tkinter.filedialog import askopenfile,asksaveasfile,askdirectory
import threading
import webbrowser
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC,ID3,Encoding,TIT2,TPE1,TPE2,TALB,TYER,TCON,TRCK,TCOM
from mutagen.mp3 import MP3
from PIL import ImageTk, Image
root=tk.Tk()
canvas1=tk.Canvas(root,width=500, height= 400,highlightthickness=0,bg="#4cb7e1")
canvas1.pack()


#canvas1.create_window(250,150,window=entry1)
select_playlist=tk.StringVar()

def elect_playlist():
    entry1.delete(0,"end")
    l=askopenfile(title="select Playlist",filetype=[("Playlists","*.m3u"),("Playlist","*.pls")])
    
    entry2.insert(0,l.name)
    select_playlist.set(l.name)
    #select_playlist.get()
    
 
    entry1.insert(0,ntpath.basename(l.name))
entry2=tk.Entry(root,textvariable=select_playlist,width=35)    
entry1=tk.Entry(root,width=22,font=2,justify="center")

canvas1.create_window(250,200,window=entry1)

button1=tk.Button(master=root,text="Select Playlist",command=elect_playlist,width=13,height=1,bd=0)
canvas1.create_window(440,200,window=button1)
print (select_playlist.get())
f_name=tk.StringVar()

numb=tk.IntVar()

song_name=tk.StringVar()

def cancel():
    root1.destroy()
def try_again():
    root1.destroy()
    convert()
    
def convert():
    global playlist
    global summ
   
    playlist_size=0
    p_s=open(select_playlist.get(),"r")
    pss=[dirr.strip() for dirr in p_s]
    for i in pss:
        if "ï»¿" in i:
            i=i.replace("ï»¿","")
        if os.path.isfile(i):    
            playlist_size+=os.path.getsize(i)/1e6
    
    k=askdirectory(title="Select Folder to Save Songs in ")
    
    root_drive,linkk=os.path.splitdrive(k)
    
    total,used,free=shutil.disk_usage(root_drive)
    free_space=free/1e6
    
    print("playlist size=",playlist_size)
    print("Available Space=",free_space)
   
    
    if free_space<playlist_size:
        global root1
        global canvas1
        root1=tk.Tk()
        canvas1=tk.Canvas(master=root1,width=195,height=120)
        canvas1.pack()
        required_space=playlist_size-free_space
        
        required_space=round(required_space,2)
        button_try=tk.Button(root1,text="Try Again",command=try_again)
        button_cancel=tk.Button(root1,text="Cancel",command=cancel)
        canvas1.create_text(95,40,text="Insufficient Space!")
        canvas1.create_text(95,45,text="Free up: "+ str(required_space)+" MB")
        canvas1.create_window(150,95,window=button_cancel,width=70)
        canvas1.create_window(38+10,95,window=button_try,width=70)
    
    elif free_space>playlist_size:
        



    
        entry3.insert(0,k)
        f_name.set(k)
        l=open(select_playlist.get(),"r")
        foldername=f_name.get()
        file_ex=os.path.basename(select_playlist.get())
        if file_ex.endswith(".m3u"):
            file_ex=file_ex.replace(".m3u","")
        elif file_ex.endswith(".pls"):
            file_ex=file_ex.replace(".pls","")


        foldername="/".join([foldername,file_ex])
        foldername="".join([foldername," [Chilled Playlist Exporter]"])
        try:
            
            
            
            os.mkdir(foldername)
        except:
            for i in range(1,100):
                  if os.path.isdir("".join([foldername,"_"+str(i)])) =="False":
                    
                
                    foldername="".join([foldername,"_"+str(i)])
                    os.mkdir(foldername)
                    print (foldername)
                    break

        playlist=[line.strip() for line in l]
        no=1
        playlis=[]
        dfs=[k for k in playlist if os.path.isfile(k)] 
        count=len(dfs)
        increment=100/count  
    
    
        def scan():

            no=1
            bar=ttk.Progressbar(master=root,mode="determinate",length=150,variable=numb,orient="horizontal")
            num=0
            canvas1.create_window(250,250,window=bar)
            widget=tk.Label(root,textvariable=song_name,bg="#4cb7e1",width=30,anchor="w")
            widget.pack()

            canvas1.create_window(250,230,window=widget)
            print (len(playlist))
            for track_dir in playlist:
                if "ï»¿" in track_dir:
                    track_dir=track_dir.replace("ï»¿","")
                if os.path.isfile(track_dir):

                    filename=ntpath.basename(track_dir)
                    if no>9:
                        filename=[str(no),". ",filename]
                    else:
                        filename=["0",str(no),". ",filename]
                    filename="".join(filename)
                    destination=os.path.join(foldername,filename)
                    destination.replace('\\','\\')
                    playlis.append(destination)
                    song_name.set(os.path.basename(track_dir))
                    copy2(track_dir,destination)
                    s=MP3(destination)
                    s2=ID3(destination)

                    if "TRCK" in s.keys():
                        s2.setall("TRCK",[])

                    s2.add(TRCK(encoding=0,text=str(no)))
                    s2.save()
                    """
                    try:

                        rename=EasyID3(destination)
                        rename["Album"]="".join([file_ex,"[Chilled Playlist Converter]"])
                        rename.save()
                    except:
                        pass
                    """
                    num=num+increment
                    numb.set(num)


                    if round(num)==100:
                         bar.destroy()
                         widget.destroy()
                         bar=ttk.Progressbar(master=root,mode="determinate",length=150,variable=numb,orient="horizontal")
                         widget=tk.Label(root,textvariable=song_name,bg="#4cb7e1",width=30,anchor="w")   

                    no+=1


        threading.Thread(target=scan).start()


    
entry3=tk.Entry(master=root,textvariable=f_name,width=23)
button2=tk.Button(master=root,text="    Export Music    ",bd=0,highlightthickness=0,command=convert)
canvas1.create_window(250,300,window=button2)


#Images
#Image_Logo=tk.PhotoImage(master=canvas1,file="C:\\Users\\THULARE KABELO\\Documents\\Business\\Chilled Fridays Listening Sessions\\Music Program Codes\\Chilled Playlist Exporter.png").subsample(16,16)
#canvas1.create_image(250,90,image=Image_Logo)

#Filename

canvas1.create_text(110,200,text="Filename :")

#Rounded reactangules

Image_bar=tk.PhotoImage(master=canvas1,file="BAR.png").subsample(2,3)
Exporter=Image.open("Chilled Playlist Exporter.png")
Exporter=Exporter.resize((200,86),Image.ANTIALIAS)
Image_exporter=ImageTk.PhotoImage(master=root,image=Exporter)
#logo_panel=tk.Label(master=root,image=Image_exporter)
canvas1.create_image(250,90,image=Image_exporter)
canvas1.create_image(250,316,image=Image_bar)
Image_selct_Playlis=tk.PhotoImage(master=canvas1,file="BAR.png").subsample(2,3)
canvas1.create_image(440.4999999999999,215.5,image=Image_selct_Playlis)

Image_entry=tk.PhotoImage(master=canvas1,file="BAR.png").subsample(1,3)
canvas1.create_image(250,215.5,image=Image_entry)

#Social media

class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground





def twitter():
    new=2;
    url="https://www.twitter.com/ChilledFridays";
    webbrowser.open(url,new=new); 
    
button3=HoverButton(root,fg="white",bg="white",activebackground="#00acee",width=35,height=30, command= twitter , bd=0 )
canvas1.create_window(350,375, window= button3)   

Image5=tk.PhotoImage(master=canvas1,file="ttw.png").subsample(22)
canvas1.create_image(350,375,image=Image5)
button3.config(image=Image5,compound=CENTER,)


def facebook():
    new=2;
    url="https://www.facebook.com/ChilledFridays";
    webbrowser.open(url,new=new); 
    
button4=HoverButton(root,fg="white",bg="white",activebackground="#3B5998",width=45,height=37, command= facebook , bd=0 )
canvas1.create_window(425,375, window= button4)

Image3=tk.PhotoImage(master=canvas1,file="black-facebook.png").subsample(22)
canvas1.create_image(425,375,image=Image3)
button4.config(image=Image3,compound=CENTER,)

def instagram():
    new=2;
    url="https://www.instagram.com/ChilledFridays";
    webbrowser.open(url,new=new); 
    
button5=HoverButton(root,fg="white",bg="white",activebackground="#DD2A7B",width=45,height=37, command= instagram , bd=0 )
canvas1.create_window(150,375, window= button5)

Image4=tk.PhotoImage(master=canvas1,file="instagram-12.png").subsample(16)
canvas1.create_image(150,375,image=Image4)
button5.config(image=Image4,compound=CENTER,)

def youtube():
    new=2;
    url="https://www.youtube.com/channel/UC_Ujffi2OBwqqPd74s2YCEQ";
    webbrowser.open(url,new=new); 
    
button6=HoverButton(root,fg="white",bg="white",activebackground="#FF0000",width=45,height=37, command= youtube , bd=0 )
canvas1.create_window(75,375, window= button6)

Image2=tk.PhotoImage(master=canvas1,file="transp youtube.png").subsample(15)
canvas1.create_image(75,375,image=Image2)
button6.config(image=Image2,compound=CENTER,)

def hearthis():
    new=2;
    url="https://www.hearthis.at/chilled-fridays";
    webbrowser.open(url,new=new); 
    
button7=HoverButton(root,fg="white",bg="white",activebackground="#1DB954", width=57,height=32,command= hearthis , bd=0 )
canvas1.create_window(250,375, window= button7)

Image6=tk.PhotoImage(master=canvas1,file="turntables.png").subsample(8)
canvas1.create_image(250,375,image=Image6)
button7.config(image=Image6,compound=RIGHT)

#Progress Bar




root.configure(background="#4cb7e1")

root.resizable(width=False,height = False)

root.title("Chilled Playlist Exporter")

    
root.mainloop()   


# In[ ]:




