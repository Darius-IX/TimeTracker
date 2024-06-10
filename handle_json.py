import json
import datetime
import time


def get_project_info_and_previous_project() -> (dict[str: bool], str):
    with open("time_tracker_times.json", "r") as json_file:
        try:
            data = json.load(json_file)
        except Exception as exc:
            # file is empty (or other error which cleans the file now :))
            print(exc)
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
            # file is empty (or other error which cleans the file now :))
            print(exc)
            return
        total_duration = data["project_names"][project_name]["total_duration"]
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
        data["project_names"][project_name]["total_duration"] = total_duration
        data["project_names"][project_name]["requires_notes"] = req_not

        as_json = json.dumps(data, indent=4)
        json_file.write(as_json)

    print("write done")


def add_or_remove_project_from_json(project_name: str) -> None:
    with open("time_tracker_times.json", "r") as json_file:
        try:
            data = json.load(json_file)
        except Exception as exc:
            # file is empty (or other error which cleans the file now :))
            print(exc)
            data = {}
        project_names = {}
        if "project_names" in data.keys():
            project_names = data["project_names"]
        if project_name in project_names:
            del project_names[project_name]
        else:
            project_names[project_name] = True

    with open("time_tracker_times.json", "w") as json_file:
        data["project_names"] = project_names
        as_json = json.dumps(data, indent=4)
        json_file.write(as_json)


def clear_json():
    with open("time_tracker_times.json", "w") as json_file:
        json_file.truncate()


def backup_json():
    # TODO
    with open("time_tracker_times.json", "w") as json_file:
        json_file.truncate()



def string_to_time_delta(duration: str) -> datetime.timedelta:
    h, min, sec = duration.split(":")
    h, min, sec = float(h), float(min), float(sec)
    return datetime.timedelta(hours=h, minutes=min, seconds=sec)


if __name__ == '__main__':
    pass
    # clear_json()
    # backup_json()
