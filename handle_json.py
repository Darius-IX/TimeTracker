import json


def get_project_names():
    return ["Praktikum", "Wizard", "Verwaltung"]


def store_new_entry(project_name: str, start_time: str, end_time: str, duration: str, notes: str = "") -> None:
    with open("time_tracker_times.json", "r") as json_file:
        try:
            data = json.load(json_file)
        except Exception as exc:
            # file is empty (or other error which cleans the file now :))
            print(exc)
            data = {}
    with open("time_tracker_times.json", "w") as json_file:
        if project_name not in data.keys():
            data[project_name] = {}
        data[project_name][start_time] = {
            "end_time": end_time,
            "duration": duration,
            "notes": notes,
        }
        as_json = json.dumps(data, indent=4)
        json_file.write(as_json)

    print("write done")


"""
json:

{
    all_projects: [A, B, C]
    previous_project: B
    projectA: {
        starttime: {
            notes
            duration
            endtime
        }
        starttime: {
            notes
            duration
            endtime
        }
    }
    projectB: {
        starttime: {
            notes:
            duration:
            endtime:
        }
        starttime: {
            notes:
            duration:
            endtime:
        }
    }
    
}
"""

if __name__ == '__main__':
    pass
