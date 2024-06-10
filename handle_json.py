import json


def get_project_names_and_previous_project() -> (list[str], str):
    with open("time_tracker_times.json", "r") as json_file:
        try:
            data = json.load(json_file)
        except Exception as exc:
            # file is empty (or other error which cleans the file now :))
            print(exc)
            data = {
                "project_names": [],
                "previous_project": "Add Project"
            }
        project_names = []
        if "project_names" in data.keys():
            project_names = data["project_names"]
        previous_project = "Add Project"
        if "previous_project" in data.keys():
            previous_project = data["previous_project"]
        return project_names, previous_project


def store_new_entry(project_name: str, start_time: str, end_time: str, duration: str, notes: str = "") -> None:
    with open("time_tracker_times.json", "r") as json_file:
        try:
            data = json.load(json_file)
        except Exception as exc:
            # file is empty (or other error which cleans the file now :))
            print(exc)
            return
    with open("time_tracker_times.json", "w") as json_file:
        if project_name not in data.keys():
            data[project_name] = {}
        data[project_name][start_time] = {
            "end_time": end_time,
            "duration": duration,
            "notes": notes,
        }
        data["previous_project"] = project_name
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
        project_names = []
        if "project_names" in data.keys():
            project_names = data["project_names"]
        if project_name in project_names:
            project_names.remove(project_name)
        else:
            project_names.append(project_name)

    with open("time_tracker_times.json", "w") as json_file:
        data["project_names"] = project_names
        as_json = json.dumps(data, indent=4)
        json_file.write(as_json)


if __name__ == '__main__':
    pass
