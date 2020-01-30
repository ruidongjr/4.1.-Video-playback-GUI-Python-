"""
4. GUI and Web
    4.1. Video playback GUI (Python)
    This script designs a GUI where user can play/pause/reverse videos, with configurable arguments

    Note: require to install packages: tkinter, PIL(pillow), cv2

"""

import tkinter as tk
from tkinter import messagebox
import PIL.Image, PIL.ImageTk
import cv2


# define a class for video player
class videoGUI:

    def __init__(self, file_path, fps=None, display_resolution=None, monochrome=False):
        self.file_path = file_path
        self.cap = cv2.VideoCapture(self.file_path)
        self.display_resolution = display_resolution
        self.monochrome = monochrome

        # change fps
        if fps:
            self.cap.set(cv2.CAP_PROP_FPS, fps)

        # read video display resolution
        if self.display_resolution != None:
            self.width = self.display_resolution[0]
            self.height = self.display_resolution[1]
        else:
            self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # set up display window
        self.window = tk.Tk()
        self.window.title('Video GUI')
        top_frame = tk.Frame(self.window)
        top_frame.pack(side=tk.TOP, pady=5)
        bottom_frame = tk.Frame(self.window)
        bottom_frame.pack(side=tk.BOTTOM, pady=5)

        self.pause = False  # Parameter that controls pause button
        self.reverse = False  # Parameter that controls reverse button

        # set up canvas display size
        self.canvas = tk.Canvas(top_frame)
        self.canvas.pack()
        self.canvas.config(width=self.width, height=self.height)

        # Play Button
        self.btn_play = tk.Button(bottom_frame, text="Play", width=15, command=self.play_video)
        self.btn_play.grid(row=0, column=0)

        # Pause Button
        self.btn_pause = tk.Button(bottom_frame, text="Pause", width=15, command=self.pause_video)
        self.btn_pause.grid(row=0, column=1)

        # Reverse Button
        self.btn_pause = tk.Button(bottom_frame, text="Reverse Frame", width=15, command=self.reverse_video)
        self.btn_pause.grid(row=0, column=2)

        self.delay = 10  # ms
        self.frame = []

        self.window.mainloop()

    def play_video(self):
        # Get a frame from the video source, and go to the next frame automatically
        ret, frame = self.get_frame()
        self.frame.append(frame)
        if ret:
            # Process each frame by monochrome
            if self.monochrome:
                self.frame[-1] = cv2.cvtColor(self.frame[-1], cv2.COLOR_BGR2GRAY)

            # Process each frame by display_resolution
            if self.display_resolution != None:
                dim = (int(self.display_resolution[0]), int(self.display_resolution[1]))
                self.frame[-1] = cv2.resize(self.frame[-1], dim, interpolation=cv2.INTER_AREA)

            # display frame
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.frame[-1]))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            # react to pressed buttons
            if self.pause:
                self.window.after_cancel(self.after_id)
                self.pause = False  # reset
            elif self.reverse:
                print('Playback by one frame.')
                self.frame.pop(-1)
                self.reverse = False
                self.after_id = self.window.after(self.delay, self.play_video)
            else:
                self.after_id = self.window.after(self.delay, self.play_video)

    # capture only one frame
    def get_frame(self):
        # assure video file is open
        try:
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        except:
            messagebox.showerror(title='Video file not found',
                                 message='Error opening file, please check the availability of the video source.')

    def pause_video(self):
        self.pause = True

    def reverse_video(self):
        self.reverse = True

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()



if __name__ == '__main__':
    video_file_path = 'video_2.mp4'
    fps = 30
    display_resolution = [400, 400]
    monochrome = True

    print('Press Play to start.')
    video = videoGUI(video_file_path, fps, display_resolution, monochrome)

