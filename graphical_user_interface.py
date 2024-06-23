import tkinter.font
import tkinter.messagebox
from tkinter import *
from handle_json import *

FONT_SMALL = ("", 20)
FONT_MEDIUM = ("", 30)
FONT_LARGE = ("", 40)
ADD_PROJECT = "Add Project"
FORBIDDEN_PROJECT_NAMES = ["", "project_info", ADD_PROJECT]


class GraphicalUserInterface:
    def __init__(self):
        self.gui_win = Tk()
        self.project_info, self.previous_project = get_project_info_and_previous_project()
        if self.previous_project == "Add Project" and len(self.project_info) > 0:
            self.previous_project = list(self.project_info.keys())[0]
        self.start_time = None
        self.update_time_passed_timer = None

    def start_gui(self):
        def throw_error(title: str, message: str):
            tkinter.messagebox.showerror(title, message)

        def throw_empty_notes_box():
            return tkinter.messagebox.askyesnocancel("Empty Notes", "Yes: leave empty; ask again\n"
                                                                    "No: leave empty, don't ask again\n"
                                                                    "Cancel: Write Note now")

        def update_time_passed():
            time_passed = str(datetime.datetime.now() - self.start_time)
            if not time_passed == "0:00:00":
                time_passed = time_passed[:time_passed.find(".")]
            time_passed_value_var.set(time_passed)
            self.update_time_passed_timer = gw.after(1000, update_time_passed)

        def start_time_tracking():
            self.start_time = datetime.datetime.now()
            time_passed_value_var.set(self.start_time.hour)
            update_time_passed()

        def stop_time_tracking(req_not):
            project_name = project_select_var.get()
            if project_name in FORBIDDEN_PROJECT_NAMES:
                throw_error("Invalid Name", "Probably forgot to choose project")
                return
            end_time = datetime.datetime.now()
            time_passed_precise = end_time - self.start_time
            prev_total_duration = string_to_time_delta(self.project_info[project_name]["total_duration"])
            new_total_duration = prev_total_duration + time_passed_precise
            self.project_info[project_name]["total_duration"] = str(new_total_duration)
            total_time_value_var.set(str(new_total_duration).split(".")[0])
            gw.after_cancel(self.update_time_passed_timer)

            notes = notes_entry.get()
            store_new_entry(project_name, str(self.start_time), str(end_time), str(time_passed_precise), notes, req_not)

        def start_or_stop(event=None):
            if event:
                pass
            selected_project = project_select_var.get()
            if selected_project in FORBIDDEN_PROJECT_NAMES:
                return
            if start_stop_button_var.get() == "Start":  # pressed start
                start_time_tracking()
                start_stop_button_var.set("Stop")
                return
            # pressed stop
            requires_notes = self.project_info[selected_project]["requires_notes"]
            if notes_entry.get() == "" and requires_notes:
                result = throw_empty_notes_box()
                if result is None:  # cancel: write note now
                    return
                if result:  # yes: leave empty; ask again
                    pass  # just proceed with empty note
                else:  # no: leave empty; don't ask again
                    self.project_info[selected_project]["requires_notes"] = False
                    requires_notes = False
            stop_time_tracking(requires_notes)
            start_stop_button_var.set("Start")

        def add_or_remove_project():
            gw.focus()
            name = add_project_entry.get()
            if name in FORBIDDEN_PROJECT_NAMES:
                return
            add_or_remove_project_from_json(name)
            if name in self.project_info:  # remove project
                if start_stop_button_var.get() == "Stop":
                    tkinter.messagebox.showerror("Remove", "Cannot remove a project, while the clock is running")
                    return
                del self.project_info[name]
                if len(self.project_info) == 0:
                    project_select_var.set(ADD_PROJECT)
                    project_drop_down["menu"].add_command(label=name, command=tkinter._setit(project_select_var, ADD_PROJECT))
                    add_project_entry.delete(0, "end")
                    return
                index = project_drop_down["menu"].index(name)
                project_drop_down["menu"].delete(index)
                if project_select_var.get() == name:
                    # print(project_drop_down.keys())
                    project_select_var.set(list(self.project_info.keys())[0])
            else:  # add project
                if project_select_var.get() == ADD_PROJECT:
                    index = project_drop_down["menu"].index(ADD_PROJECT)
                    project_drop_down["menu"].delete(index)
                tot_dur = str(calc_total_duration_for_projects([name])[name])
                project_select_var.set(name)
                self.project_info[name] = {"total_duration": tot_dur, "requires_notes": True}
                project_drop_down["menu"].add_command(label=name, command=tkinter._setit(project_select_var, name))
                # project_drop_down["menu"].add_command(label=name, command=changed_project_selection)
                # project_drop_down.bind(changed_project_selection)

            add_project_entry.delete(0, "end")

        def escape_add_project_entry_focus(event):
            if event:
                pass
            gw.focus()

        def changed_project_selection(project_name):
            total_time_value_var.set(self.project_info[project_name]["total_duration"].split(".")[0])

        def closing_window():
            if start_stop_button_var.get() == "Start":
                gw.destroy()
                return
            result = tkinter.messagebox.askyesnocancel("Closing Window", "Close window and save changes?")
            if result is None:  # cancel: don't close
                return
            if result:  # yes: close window and save
                start_or_stop(None)
                pass  # just proceed with empty note
            else:  # no: close window without saving
                pass
            gw.destroy()
            return

        def ask_clear_json():
            mes = "Are you sure you want to clear the JSON file?\n  This will also close the window."
            if tkinter.messagebox.askokcancel("Clear JSON?", mes):
                clear_json()
                gw.destroy()

        def print_info(event):
            return
            print(self.project_info)

        gw = self.gui_win
        gw.title("Time Tracker")
        gw.geometry("500x580")
        gw.resizable(0, 0)
        gw.protocol("WM_DELETE_WINDOW", closing_window)

        menubar = Menu(gw)
        menu_options = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Options", menu=menu_options)
        menu_options.add_command(label="Clear JSON", command=ask_clear_json)
        menu_options.add_command(label="Backup JSON", command=backup_json)

        left_side = Frame(gw, padx=10, pady=10)
        left_side.grid(row=1, column=0)
        col0_left = Frame(left_side, padx=5, pady=5)
        col0_left.grid(row=2, column=0)
        col1_left = Frame(left_side, padx=5, pady=5)
        col1_left.grid(row=2, column=1)

        bottom = Frame(gw, padx=10, pady=10)
        bottom.grid(row=3, column=0, sticky="s")
        bottom.rowconfigure(3, weight=1)
        """bottom.columnconfigure(0, weight=1)
        bottom.columnconfigure(1, weight=1)"""

        """DropDown for projects"""
        project_select_var = StringVar(value=self.previous_project)
        if not self.project_info:
            project_drop_down = OptionMenu(gw, project_select_var, "Add Project", command=changed_project_selection)
        else:
            project_drop_down = OptionMenu(gw, project_select_var, *self.project_info.keys(), command=changed_project_selection)
        project_drop_down.grid(row=0, columnspan=2)
        project_drop_down.config(font=FONT_LARGE)
        drop_down_options = project_drop_down["menu"]
        drop_down_options.config(font=FONT_MEDIUM)

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
        total_duration = "0:00:00"
        if not project_select_var.get() == "Add Project":
            total_duration = self.project_info[project_select_var.get()]["total_duration"].split(".")[0]
        total_time_value_var = StringVar(value=total_duration)
        total_time_value = Label(col1_left, textvariable=total_time_value_var, font=FONT_MEDIUM)
        total_time_value.grid(row=3)

        """Textfield for Notes"""
        notes_label = Label(bottom, text="Notes:", font=FONT_MEDIUM)
        notes_label.grid(row=1, columnspan=2, sticky="s")
        notes_entry = Entry(bottom, font=FONT_MEDIUM)
        notes_entry.grid(row=2, columnspan=2, sticky="s")

        """Textfield for add/remove project"""
        add_project_entry = Entry(bottom, font=FONT_MEDIUM)
        add_project_entry.grid(row=4, columnspan=2, sticky="s")
        add_project_button = Button(bottom, text="Add or Remove Project:", font=FONT_MEDIUM,
                                    command=add_or_remove_project, width=19)
        add_project_button.grid(row=3, columnspan=2, sticky="s", pady=5)

        """Bind Hotkeys"""
        gw.bind("<Escape>", escape_add_project_entry_focus)
        gw.bind("<Return>", start_or_stop)
        gw.bind("<i>", print_info)

        gw.config(menu=menubar)
        if gw:
            gw.mainloop()
