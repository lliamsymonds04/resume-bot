import json


def get_skills() -> list[str]:
    with open("data/skills.json") as f:
        base_skills = json.load(f)

    with open("data/projects.json") as f:
        projects = json.load(f)
        
    with open("data/coursework.json") as f:
        coursework = json.load(f)
        
    with open("data/experience.json") as f:
        experience = json.load(f)

    with open("data/me.json") as f:
        me = json.load(f)

    #use ai to add to skills list
