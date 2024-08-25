import tkinter.font
import tkinter.messagebox
from tkinter import *
from handle_json import *

FONT_SMALL = ("", 20)
FONT_MEDIUM = ("", 30)
FONT_LARGE = ("", 40)
ADD_PROJECT = "Add Project"
FORBIDDEN_PROJECT_NAMES = ["", "project_info", ADD_PROJECT, "reminder_time"]


class GraphicalUserInterface:
    def __init__(self):
        self.gui_win = Tk()
        self.project_info, self.previous_project, self.reminder_interval_time_minutes = get_project_info_previous_project_and_reminder_time()
        if self.previous_project == "Add Project" and len(self.project_info) > 0:
            self.previous_project = list(self.project_info.keys())[0]
        self.start_time = None
        self.update_time_passed_timer = None
        self.project_drop_down = None
        self.reminder_timer = None

    def start_gui(self):
        def throw_error(title: str, message: str):
            tkinter.messagebox.showerror(title, message)

        def throw_empty_notes_box():
            return tkinter.messagebox.askyesnocancel("Empty Notes", "Yes: leave empty; ask again\n"
                                                                    "No: leave empty, don't ask again\n"
                                                                    "Cancel: Write Note now")

        def run_reminder_timer():
            if self.reminder_interval_time_minutes == -1:
                if self.reminder_timer is None:
                    return
                self.gui_win.after_cancel(self.reminder_timer)
            if self.reminder_timer:
                throw_error("Reminder", f"{self.reminder_interval_time_minutes} minutes passed")
            timer_msec = self.reminder_interval_time_minutes * 1000 * 60
            self.reminder_timer = gw.after(timer_msec, run_reminder_timer)

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
            run_reminder_timer()

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
            gw.after_cancel(self.reminder_timer)

            notes = notes_entry.get()
            notes_entry.delete(0, "end")
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
            # TODO move to stop timetracking or own function
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
                    self.project_drop_down["menu"].add_command(label=name, command=tkinter._setit(project_select_var, ADD_PROJECT))
                    add_project_entry.delete(0, "end")
                    return
                index = self.project_drop_down["menu"].index(name)
                self.project_drop_down["menu"].delete(index)
                if project_select_var.get() == name:
                    # print(project_drop_down.keys())
                    project_select_var.set(list(self.project_info.keys())[0])
            else:  # add project
                if project_select_var.get() == ADD_PROJECT:
                    index = self.project_drop_down["menu"].index(ADD_PROJECT)
                    self.project_drop_down["menu"].delete(index)
                tot_dur = str(calc_total_duration_for_projects([name])[name])
                total_time_value_var.set(tot_dur.split(".")[0])
                self.project_info[name] = {"total_duration": tot_dur, "requires_notes": True}
                self.project_drop_down.destroy()
                project_select_var.set(name)
                self.project_drop_down = OptionMenu(project_drop_down_frame, project_select_var,
                                                    *self.project_info.keys(), command=changed_project_selection)
                self.project_drop_down.config(font=FONT_LARGE)
                new_drop_down_options = self.project_drop_down["menu"]
                new_drop_down_options.config(font=FONT_MEDIUM)
                self.project_drop_down.pack(fill="x", pady=10)

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

        def recalculate_total_durations():
            write_total_durations_of_projects()

        def set_reminder_time(reminder_minutes):
            self.reminder_interval_time_minutes = reminder_minutes
            store_reminder_time(reminder_minutes)

        def print_info(event):
            return
            print(self.project_info)

        # TODO GUI marker
        gw = self.gui_win
        gw.title("Time Tracker")
        gw.geometry("500x680")
        # gw.minsize(width=520, height=None)
        gw.protocol("WM_DELETE_WINDOW", closing_window)

        menubar = Menu(gw)
        menu_options = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Options", menu=menu_options)
        menu_options.add_command(label="Clear JSON", command=ask_clear_json)
        menu_options.add_command(label="Backup JSON", command=backup_json)
        menu_options.add_command(label="Recalc", command=recalculate_total_durations)
        """Timer Options"""
        reminder_submenu = Menu(menu_options, tearoff=0)
        reminder_submenu.add_command(label="Off", command=lambda: set_reminder_time(-1))
        reminder_submenu.add_command(label="15 min", command=lambda: set_reminder_time(15))
        reminder_submenu.add_command(label="30 min", command=lambda: set_reminder_time(30))
        reminder_submenu.add_command(label="60 min", command=lambda: set_reminder_time(60))
        reminder_submenu.add_command(label="90 min", command=lambda: set_reminder_time(90))
        reminder_submenu.add_command(label="120 min", command=lambda: set_reminder_time(120))
        menu_options.add_cascade(label="Reminder", menu=reminder_submenu)


        top_frame = Frame(gw)
        top_frame.pack(padx=10, pady=10, side="top", fill="x")
        bottom_frame = Frame(gw)
        bottom_frame.pack(padx=10, pady=10, side="bottom", fill="x")
        project_drop_down_frame = Frame(top_frame)
        project_drop_down_frame.pack()

        """DropDown for projects"""
        project_select_var = StringVar(value=self.previous_project)
        if not self.project_info:
            self.project_drop_down = OptionMenu(project_drop_down_frame, project_select_var,
                                                "Add Project", command=changed_project_selection)
        else:
            self.project_drop_down = OptionMenu(project_drop_down_frame, project_select_var,
                                                *self.project_info.keys(), command=changed_project_selection)
        self.project_drop_down.config(font=FONT_LARGE)
        drop_down_options = self.project_drop_down["menu"]
        drop_down_options.config(font=FONT_MEDIUM)
        self.project_drop_down.pack(fill="x", pady=10)

        """Button for Start/Stop"""
        start_stop_button_var = StringVar(value="Start")
        start_stop_button = Button(top_frame, textvariable=start_stop_button_var, command=start_or_stop, font=FONT_LARGE)
        start_stop_button.pack(fill="x", pady=10)

        time_frame = Frame(top_frame)
        time_frame.pack(side="top", padx=20, pady=10)
        time_labels_frame = Frame(time_frame)
        time_labels_frame.pack(side="left", padx=10)
        time_values_frame = Frame(time_frame)
        time_values_frame.pack(side="left", padx=10)
        """Label current time"""
        time_passed_label = Label(time_labels_frame, text="Time Passed:", font=FONT_MEDIUM)
        time_passed_label.pack()
        time_passed_value_var = StringVar(value="______")
        time_passed_value = Label(time_values_frame, textvariable=time_passed_value_var, font=FONT_MEDIUM)
        time_passed_value.pack()

        """Label total time"""
        total_time_label = Label(time_labels_frame, text="Total Time:", font=FONT_MEDIUM)
        total_time_label.pack()
        total_duration = "0:00:00"
        if not project_select_var.get() == "Add Project":
            total_duration = self.project_info[project_select_var.get()]["total_duration"].split(".")[0]
        total_time_value_var = StringVar(value=total_duration)
        total_time_value = Label(time_values_frame, textvariable=total_time_value_var, font=FONT_MEDIUM)
        total_time_value.pack()

        """Textfield for Notes"""
        notes_label = Label(top_frame, text="Notes:", font=FONT_MEDIUM)
        notes_label.pack(fill="x")
        notes_entry = Entry(top_frame, font=FONT_MEDIUM)
        notes_entry.pack(fill="x")

        """Textfield for add/remove project"""
        add_project_button = Button(bottom_frame, text="Add or Remove Project:", font=FONT_MEDIUM,
                                    command=add_or_remove_project, width=19)
        add_project_button.pack(fill="x", pady=10)
        add_project_entry = Entry(bottom_frame, font=FONT_MEDIUM)
        add_project_entry.pack(fill="x", pady=10)

        """Bind Hotkeys"""
        gw.bind("<Escape>", escape_add_project_entry_focus)
        gw.bind("<Return>", start_or_stop)
        gw.bind("<i>", print_info)

        gw.config(menu=menubar)
        if gw:
            gw.mainloop()
