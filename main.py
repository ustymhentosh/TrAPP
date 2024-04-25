import tkinter as tk
import ttkbootstrap as ttk
from ctypes import windll
from ttkbootstrap import Style

from pages.GPSLoader import GPSLoaderPG
from pages.MainPageT import MainPage
from pages.FrontDoor import FrontDoor

import tkinter.font as tkfont

windll.shcore.SetProcessDpiAwareness(1)


class MyApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        default_font = tkfont.nametofont("TkDefaultFont")
        default_font.configure(size=14)
        self.geometry("700x500")

        # ico = SavedImages.get_icon("main_icon")
        # photo = ImageTk.PhotoImage(ico)
        # self.wm_iconphoto(False, photo)

        self._frame = None
        self.title("UCUtil")

        self.style = Style(theme="cosmo")
        self.switch_frame("FrontDoor")

    def switch_frame(self, frame_class, arguments=None):
        """Destroys current frame and replaces it with a new one."""

        if frame_class == "GPSLoaderPG":
            frame_class = GPSLoaderPG
        elif frame_class == "MainPage":
            frame_class = MainPage
        elif frame_class == "FrontDoor":
            frame_class = FrontDoor

        new_frame = frame_class(self, arguments)

        if self._frame is not None:
            for child in self._frame.winfo_children():
                child.destroy()
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
