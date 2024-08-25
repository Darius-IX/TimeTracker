import json
import datetime
import shutil
import os
FILE_NAME: str = "time_tracker_times.json"


def get_project_info_previous_project_and_reminder_time() -> tuple[dict[str: bool], str, int]:
    if not os.path.isfile(FILE_NAME):
        with open(FILE_NAME, "x"):
            pass
    with open(FILE_NAME, "r") as json_file:
        try:
            data = json.load(json_file)
        except Exception as exc:
            # file is empty (or other error which cleans the file now :))
            if exc:
                pass
            data = {
                "project_info": {},
                "previous_project": "Add Project",
                "reminder_time": -1
            }
        project_info = {}
        if "project_info" in data.keys():
            project_info = data["project_info"]
        previous_project = "Add Project"
        if "previous_project" in data.keys():
            previous_project = data["previous_project"]
        reminder_time = -1
        if "reminder_time" in data.keys():
            reminder_time = data["reminder_time"]
        return project_info, previous_project, reminder_time


def store_new_entry(project_name: str, start_time: str, end_time: str, duration: str, notes: str, req_not: bool) -> None:
    with open(FILE_NAME, "r") as json_file:
        try:
            data = json.load(json_file)
        except Exception as exc:
            # file is empty (or other error), abort
            print(exc)
            return
        total_duration = data["project_info"][project_name]["total_duration"]
    with open(FILE_NAME, "w") as json_file:
        if project_name not in data.keys():
            data[project_name] = {}
        data[project_name][start_time] = {
            "end_time": end_time,
            "duration": duration,
            "notes": notes,
        }
        total_duration = str(string_to_time_delta(total_duration) + string_to_time_delta(duration))
        data["previous_project"] = project_name
        data["project_info"][project_name]["total_duration"] = total_duration
        data["project_info"][project_name]["requires_notes"] = req_not

        as_json = json.dumps(data, indent=4)
        json_file.write(as_json)

    print("write successful")


def store_reminder_time(reminder_minutes: int) -> None:
    with open(FILE_NAME, "r") as json_file:
        try:
            data = json.load(json_file)
        except Exception as exc:
            # file is empty (or other error which cleans the file now :))
            if exc:
                pass
            data = {}
        data["reminder_time"] = reminder_minutes

    with open(FILE_NAME, "w") as json_file:
        as_json = json.dumps(data, indent=4)
        json_file.write(as_json)



def add_or_remove_project_from_json(project_name: str) -> None:
    with open(FILE_NAME, "r") as json_file:
        try:
            data = json.load(json_file)
        except Exception as exc:
            # file is empty (or other error which cleans the file now :))
            if exc:
                pass
            data = {}
        if "project_info" not in data:
            data["project_info"] = {}
        if project_name in data["project_info"]:
            del data["project_info"][project_name]
        else:
            data["project_info"][project_name] = {"total_duration": "0:00:00", "requires_notes": True}

    with open(FILE_NAME, "w") as json_file:
        as_json = json.dumps(data, indent=4)
        json_file.write(as_json)


def clear_json():
    with open(FILE_NAME, "w") as json_file:
        json_file.truncate()


def backup_json():
    date = str(datetime.datetime.now())
    # format 2024-06-19 19:58:44.888948 to 2024_06_19__19_58_44
    date = date.replace("-", "_").replace(" ", "__").replace(":", "_").split(".")[0]
    shutil.copy2(FILE_NAME, f"backup_ttt_{date}.json")


def string_to_time_delta(duration: str) -> datetime.timedelta:
    duration_split = duration.split(" ")
    days = 0
    if len(duration_split) > 1:
        days = float(duration_split[0])
    h, mn, sec = duration_split[-1].split(":")
    h, mn, sec = float(h), float(mn), float(sec)
    return datetime.timedelta(days=days, hours=h, minutes=mn, seconds=sec)


def calc_total_duration_for_projects(projects: list[str]) -> dict[str: datetime.timedelta]:
    with open(FILE_NAME, "r") as json_file:
        try:
            data = json.load(json_file)
        except Exception as exc:
            print(exc)
            return
        if not projects:
            projects = list([key for key in data.keys() if key not in ["previous_project", "project_info"]])
        total_durations = {p: datetime.timedelta(seconds=0) for p in projects}
        for project in projects:
            if project not in data:
                continue
            durations = [string_to_time_delta(data[project][entry]["duration"]) for entry in data[project]]
            for duration in durations:
                total_durations[project] += duration
        return total_durations


def write_total_durations_of_projects():
    # TODO recalc duration of session by start and end time
    calculated_total_durations = calc_total_duration_for_projects([])
    with open(FILE_NAME, "r") as json_file:
        try:
            data = json.load(json_file)
        except Exception as exc:
            print(exc)
            return
    for project, total_duration in calculated_total_durations.items():
        data["project_info"][project]["total_duration"] = str(total_duration)
    with open(FILE_NAME, "w") as json_file:
        as_json = json.dumps(data, indent=4)
        json_file.write(as_json)


if __name__ == '__main__':
    pass
    # clear_json()
    # backup_json()
