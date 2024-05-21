from tkinter import *
from tkinter import ttk
import handle_json

FONT_SMALL = ("", 20)
FONT_MEDIUM = ("", 30)
FONT_LARGE = ("", 40)


class GraphicalUserInterface:
    def __init__(self):
        self.gui_win = Tk()
        self.project_names: list = handle_json.get_project_names()

    def get_current_time_passed(self):
        return 10

    def start_gui(self):
        def start_or_stop(event=None):
            if event:
                pass
            if start_stop_button_var.get() == "Start":
                start_stop_button_var.set("Stop")
                return
            start_stop_button_var.set("Start")

        def add_project():
            pass

        def escape_add_project_entry_focus():
            gw.focus()

        def search_project(event):
            value = event.widget.get()
            if value == "":
                combo_box["values"] = self.project_names
            else:

                data = []
                for item in self.project_names:
                    if value.lower() in item.lower():
                        data.append(item)
                combo_box["values"] = data

        gw = self.gui_win
        gw.title("Time Tracker")
        gw.minsize(width=500, height=500)

        left_side = Frame(gw, padx=10, pady=10, bg="blue")
        left_side.grid(row=1, column=0)
        col0_left = Frame(left_side, padx=5, pady=5, bg="lightblue")
        col0_left.grid(row=2, column=0)
        col1_left = Frame(left_side, padx=5, pady=5, bg="lightgreen")
        col1_left.grid(row=2, column=1)

        bottom = Frame(gw, padx=10, pady=10, bg="red")
        bottom.grid(row=3, column=0, sticky="s")
        bottom.rowconfigure(3, weight=1)
        """bottom.columnconfigure(0, weight=1)
        bottom.columnconfigure(1, weight=1)"""

        """search combobox"""
        combo_box = ttk.Combobox(gw, values=self.project_names, font=FONT_MEDIUM)
        combo_box.set("Search Project")
        combo_box.grid(row=0, columnspan=2)

        """Button for Start/Stop"""
        start_stop_button_var = StringVar(value="Start")
        start_stop_button = Button(
            left_side, textvariable=start_stop_button_var, command=start_or_stop, font=FONT_LARGE, width=15
        )
        start_stop_button.grid(row=1, columnspan=2)

        """Label current time"""
        time_passed_label = Label(col0_left, text="Time Passed:", font=FONT_MEDIUM)
        time_passed_label.grid(row=2)
        time_passed_value_var = StringVar(value="______")
        time_passed_value = Label(col1_left, textvariable=time_passed_value_var, font=FONT_MEDIUM)
        time_passed_value.grid(row=2)

        """Label total time"""
        total_time_label = Label(col0_left, text="Total Time:", font=FONT_MEDIUM)
        total_time_label.grid(row=3)
        total_time_value_var = StringVar(value="______")
        total_time_value = Label(col1_left, textvariable=total_time_value_var, font=FONT_MEDIUM)
        total_time_value.grid(row=3)

        """Textfield for add project"""
        add_project_entry = Entry(bottom, font=FONT_MEDIUM)
        add_project_entry.grid(row=1, columnspan=2, sticky="s")
        add_project_button = Button(bottom, text="Add Project", font=FONT_MEDIUM, command=add_project, width=19)
        add_project_button.grid(row=2, columnspan=2, sticky="s", pady=10)

        """Bind Hotkeys"""
        gw.bind("<Escape>", escape_add_project_entry_focus)
        gw.bind("<Return>", start_or_stop)
        combo_box.bind("<KeyRelease>", search_project)

        if gw:
            gw.mainloop()
