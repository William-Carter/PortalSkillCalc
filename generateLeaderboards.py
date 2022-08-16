import csv
import json


cats = ["glitchless", "legacy", "unrestricted", "inbounds", "oob"]

def addUnfilledCategories(runner: dict, propagate: bool = True) -> dict:
    """
    Adds categories to runner dict that aren't already there. 
    If it can reuse a lower hierarchy time it will (e.g. glitchless will be used for nosla), otherwise it will leave it blank.
    Parameters:
        runner - Runner dict with only the categories the player has competed in.
        propagate - whether to use lower hierarchy times 
    Returns:
        runner - Runner dict with all categories, with new categories either upfilled or blank.
    """
    containedCategories = []
    for cat in runner.keys():
        containedCategories.append(cats.index(cat))


    for cat in cats:
        if not cat in runner.keys():
            runner[cat] = ""    
            if propagate:
                if not cats.index(cat) > max(containedCategories):
                    for conCat in sorted(containedCategories):
                        if conCat < cats.index(cat):
                            runner[cat] = runner[cats[conCat]]

    return runner

def formatTime(seconds):
    ms = seconds - seconds//1
    seconds = seconds//1

    finalString = ""
    hours = seconds//3600
    if hours != 0:  
        finalString += str(int(hours))+":"
    seconds = seconds%3600

    minutes = seconds//60
    if minutes != 0:
        finalString += str(int(minutes))+":"

    seconds = seconds%60

    finalString += str(int(seconds)).zfill(2)+"."
    if not str(ms) == "0":
        finalString += (str(round(ms, 3)).split(".")[1])
    else:
        finalString += (str(round(ms, 3)))

    return finalString


if __name__ == "__main__":
    with open("runnersDL.json", "r") as f:
        runners = json.load(f)


    for cat in cats:
        leaderboard = []
        for runner in runners.keys():
            runnerValues = addUnfilledCategories(runners[runner])
            if runnerValues[cat]:
                leaderboard.append([runner, runnerValues[cat]])

        output = sorted(leaderboard, key=lambda k: k[1])



        with open(cat+"Leaderboard.csv", "w", newline="") as f:
            e = csv.writer(f, delimiter=",")
            for row in output:
                row[1] = formatTime(row[1])
                e.writerow(row)

