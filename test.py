import tkinter as tk
from tkinter import ttk


class MyApp:
    def __init__(self, root):
        self.root = root
        self.selected_st = tk.StringVar()
        self.selected_st.set("початкова година")

        start_hours_f = ttk.Frame(master=root)
        start_h = ttk.OptionMenu(
            master=start_hours_f,
            variable=self.selected_st,
            style="info.Outline.TMenubutton",
            command=self.update_title,
        )
        start_menu = tk.Menu(start_h)
        for option in [f"{i}:00" for i in range(6, 23)]:
            start_menu.add_radiobutton(
                label=option, value=option, variable=self.selected_st
            )
        start_h["menu"] = start_menu
        start_h.pack()
        start_hours_f.pack()

    def update_title(self, selected_option):
        self.selected_st.set(selected_option)


if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
