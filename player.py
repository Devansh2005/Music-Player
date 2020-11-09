from tkinter import *
from tkinter import filedialog #ttk 
import pygame
import time
from mutagen.mp3 import MP3 #pip isntall mutagen
import tkinter.ttk as ttk

root =Tk()

root.title("Mp3 Player")
root.geometry("700x500")

# Initialize Pygame

pygame.mixer.init()

# CREATE a funcy=tion to deal with time

def play_time():
    # check if song is topped
    if stopped:
        return
    # Current time
    current_time=pygame.mixer.music.get_pos() /1000
    # time to minutes and second from ms
    converted_curernt_time= time.strftime("%M:%S", time.gmtime(current_time))

    # Reconstruct song with directory
    song=playlist_box.get(ACTIVE)
    song=f"C:/Users/Devansh/Desktop/mp3player/mp3/{song}.mp3"

    # Find curret song length
    song_mut=MP3(song)
    global song_length
    song_length = song_mut.info.length
    #Convert to time format
    converted_song_length= time.strftime("%M:%S", time.gmtime(song_length))

    # Slider length to song length
    song_slider.config(to=song_length)
    my_label.config(text=song_slider.get())

    # Check to see if song is over and end the time at bottom
    if int(song_slider.get())== int(song_length):
        stop()
        

    elif paused :
        # To see if paused -if so, then pass
        pass
    else:

        # Move slider along 1 sec at a time

        next_time = int(song_slider.get()) + 1
        # Output new time value to slider and to length of the song
        song_slider.config(to=song_length, value=next_time)

        #convert slider postition to time format
        converted_curernt_time= time.strftime("%M:%S", time.gmtime(int(song_slider.get())))
        
        # Output slider
        status_bar.config(text=f'Time: {converted_curernt_time} of {converted_song_length}')


    # status_bar.config(text=converted_song_length)

    #Add time to status bar
    if current_time>= 1:
        status_bar.config(text=f'Time: {converted_curernt_time} of {converted_song_length}')


    # Add to status bar
    status_bar.config(text=f'Time: {converted_curernt_time} of {converted_song_length}')
    # loop to check time after every ms
    status_bar.after(1000, play_time)

################################### ADD SONGS ##################
# To add one song to playlist 
def add_song(): #Line 
    song= filedialog.askopenfilename(initialdir="./mp3",title="choose a song", filetypes=(("mp3 Files","*.mp3"), )) # This is WOW  (, to make it tuple)
    # Strip out directory
    song=song.replace("C:/Users/Devansh/Desktop/mp3player/mp3/", "")
    song=song.replace(".mp3","")
    # Add to playlist
    playlist_box.insert(END, song)

# To add  many songs to playlist
def add_many_song(): #line 
    songs= filedialog.askopenfilenames(initialdir="./mp3",title="choose a song", filetypes=(("mp3 Files","*.mp3"), )) # This is WOW  (, to make it tuple)
    #Loop to songs list and replace directory structure and mp3 from song name
    for song in songs:
        # Strip out directory
        song=song.replace("C:/Users/Devansh/Desktop/mp3player/mp3/", "")
        song=song.replace(".mp3","")
        # Add to playlist
        playlist_box.insert(END, song)
##---------------------------------Add SONGS END---------------------------##

## -----------------------------DELETE SONGS  ----------------------------------###

# To delete one song from a playlist
def delete_song():
    # It will delete the selected songs from the playlist-- ANCHOR
    playlist_box.delete(ANCHOR)

# To delete all songs from a playlist
def delete_all_song():
    playlist_box.delete(0, END) # ahh like a list from index 0 to end


## -----------------------------DELETE SONGSEND ----------------------------------###

##-----------------------------BUTTONS FUNCTIONS------------------------##

# Create play button function
def play():
    # set stopped to false
    global stopped
    stopped=False 
    song=playlist_box.get(ACTIVE)
    song=f"C:/Users/Devansh/Desktop/mp3player/mp3/{song}.mp3"  #-- get directory
    # my_label.config(text=song)

    # Load song with pygame
    pygame.mixer.music.load(song)
    # Load song with pygame
    pygame.mixer.music.play(loops=0)

    # GET SONG TIME
    play_time()
# Create a global stopped variable
global stopped
stopped= False

def stop():
    # Stop song
    pygame.mixer.music.stop()

    # Clear that song from playlist

    playlist_box.selection_clear(ACTIVE)

    status_bar.config(text="")
    # Set slider to zero
    song_slider.config(value=0)

    # Set stopped variable to true
    global stopped
    stopped= True

# Create paused variable

global paused 
paused = False 

def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        #Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        #pause
        pygame.mixer.music.pause()
        paused=True
#Next song function
def next_song():
    # Reset solder position and status bar
    status_bar.config(text="")
    song_slider.config(value=0)

    #get current song in number
    next_one = playlist_box.curselection()
    # Add one to the current song
    next_one = next_one[0]+ 1

    # Grab the song title from the playlist
    song = playlist_box.get(next_one)
    # Add directory structure to the song
    song=f'C:/Users/Devansh/Desktop/mp3player/mp3/{song}.mp3'
    # Load song with pygame
    pygame.mixer.music.load(song)
    # Load song with pygame
    pygame.mixer.music.play(loops=0)

    # Clear active bar in playlist
    playlist_box.selection_clear(0,END)
    # Move Active bar to the next song
    playlist_box.activate(next_one)
    # set active bar to the next song
    playlist_box.select_set(next_one,last=None)

#Previous song function

def previous_song():
    # Reset solder position and status bar
    status_bar.config(text="")
    song_slider.config(value=0)
    #get current song in number
    next_one = playlist_box.curselection()
    # Add one to the current song
    next_one = next_one[0]- 1

    # Grab the song title from the playlist
    song = playlist_box.get(next_one)
    # Add directory structure to the song
    song=f'C:/Users/Devansh/Desktop/mp3player/mp3/{song}.mp3'
    # Load song with pygame
    pygame.mixer.music.load(song)
    # Load song with pygame
    pygame.mixer.music.play(loops=0)

    # Clear active bar in playlist
    playlist_box.selection_clear(0,END)
    # Move Active bar to the next song
    playlist_box.activate(next_one)
    # set active bar to the next song
    playlist_box.select_set(next_one,last=None)

# Create Volume Function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

# slide function
def slide(x):
    song=playlist_box.get(ACTIVE)
    song=f"C:/Users/Devansh/Desktop/mp3player/mp3/{song}.mp3"  #-- get directory
    # my_label.config(text=song)

    # Load song with pygame mixer
    pygame.mixer.music.load(song)
    # Load song with pygame mixer
    pygame.mixer.music.play(loops=0, start=song_slider.get())

# Create main frame
main_frame= Frame(root)
main_frame.pack(pady=20)

# Volume slider frame
volume_frame=LabelFrame(main_frame, text="Volume")
volume_frame.grid(row=0, column=1)

# Create volume slider 
volume_slider= ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, length=125, value=1 ,command= volume)
volume_slider.pack(pady=10)

# Create song slider
song_slider= ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, length=360, value=0 ,command= slide)
song_slider.grid(row=2, column=0,pady=20)
# Playlist Box
playlist_box =Listbox(main_frame, bg="black", fg="green", width =60, selectbackground="green", selectforeground="black")
playlist_box.grid(row=0, column=0)



# Create buttons frame 
control_frame =Frame(main_frame)
control_frame.grid(row=1, column=0,pady=20)


# Defining button images
back_button_img = PhotoImage(file="images/rewind.png")
play_button_img = PhotoImage(file="images/play.png")
pause_button_img = PhotoImage(file="images/pause.png")
stop_button_img = PhotoImage(file="images/stop2.png")
forward_button_img = PhotoImage(file="images/forward.png")


# Buttons in frame
back_button =Button(control_frame, image=back_button_img, borderwidth=0, command=previous_song)
forward_button=Button(control_frame, image=forward_button_img, borderwidth=0,command=next_song)
play_button =Button(control_frame, image=play_button_img, borderwidth=0, command=play)
pause_button=Button(control_frame, image=pause_button_img, borderwidth=0,command=lambda: pause(paused))
stop_button=Button(control_frame, image=stop_button_img, borderwidth=0, command=stop)

# Putting button in GUI
back_button.grid(row=0, column=0,padx=10)
forward_button.grid(row=0, column=1,padx=10)
play_button.grid(row=0, column=2,padx=10)
pause_button.grid(row=0, column=3,padx=10)
stop_button.grid(row=0, column=4,padx=10)

# Create Menu

my_menu= Menu(root)
root.config(menu=my_menu)

# Create Add song menu dropdowns
add_song_menu= Menu(my_menu, tearoff=0) # tearoff removes that fucking dotted thing
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)

#ADD one song to playlist
add_song_menu.add_command(label="Add one song to a playlist", command=add_song)

#add many songs to playlist
add_song_menu.add_command(label="Add many songs to a playlist", command=add_many_song)

# Create Delete Song Menu Dropdowns

remove_song_menu= Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)

# Remove a single song from playlist
remove_song_menu.add_command(label="Delete a song from a Playlist", command= delete_song)
# remove all songs from playlist
remove_song_menu.add_command(label="Delete all songs from a Playlist", command= delete_all_song)

# Create STATUS BAR

status_bar= Label(root, text="Time", bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Temporary label

# my_label= Label(root, text="", bg="black", fg="green")
# my_label.pack(pady=20)


root.mainloop()
