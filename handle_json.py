import json
import datetime
import shutil


def get_project_info_and_previous_project() -> (dict[str: bool], str):
    with open("time_tracker_times.json", "r") as json_file:
        try:
            data = json.load(json_file)
        except Exception as exc:
            # file is empty (or other error which cleans the file now :))
            if exc:
                pass
            data = {
                "project_info": {},
                "previous_project": "Add Project"
            }
        project_info = {}
        if "project_info" in data.keys():
            project_info = data["project_info"]
        previous_project = "Add Project"
        if "previous_project" in data.keys():
            previous_project = data["previous_project"]
        return project_info, previous_project


def store_new_entry(project_name: str, start_time: str, end_time: str, duration: str, notes: str, req_not: bool) -> None:
    with open("time_tracker_times.json", "r") as json_file:
        try:
            data = json.load(json_file)
        except Exception as exc:
            # file is empty (or other error), abort
            print(exc)
            return
        total_duration = data["project_info"][project_name]["total_duration"]
    with open("time_tracker_times.json", "w") as json_file:
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


def add_or_remove_project_from_json(project_name: str) -> None:
    with open("time_tracker_times.json", "r") as json_file:
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

    with open("time_tracker_times.json", "w") as json_file:
        as_json = json.dumps(data, indent=4)
        json_file.write(as_json)


def clear_json():
    with open("time_tracker_times.json", "w") as json_file:
        json_file.truncate()


def backup_json():
    date = str(datetime.datetime.now())
    # format 2024-06-19 19:58:44.888948 to 2024_06_19__19_58_44
    date = date.replace("-", "_").replace(" ", "__").replace(":", "_").split(".")[0]
    shutil.copy2("time_tracker_times.json", f"backup_ttt_{date}.json")


def string_to_time_delta(duration: str) -> datetime.timedelta:
    h, mn, sec = duration.split(":")
    h, mn, sec = float(h), float(mn), float(sec)
    return datetime.timedelta(hours=h, minutes=mn, seconds=sec)


if __name__ == '__main__':
    pass
    clear_json()
    # backup_json()
