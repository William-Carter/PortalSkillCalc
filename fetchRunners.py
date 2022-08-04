import json
import requests
# Defining constants


cats = ["glitchless", "legacy", "unrestricted", "inbounds", "oob"]

def pullRunners(places: int) -> None:
    """
    Generates a runnersDL.json file full of every runner and all their PBs
    """
    runners = {}

    for cat in cats:
        with open(f"{cat}DL.json", "r") as f:
            runs = json.load(f)["data"]["runs"]


        # Iterate as many times as requested, or for every run on the board, whichever is shorter.
        for i in range(min(places, len(runs))):
            if runs[i]["run"]["players"][0]["rel"] == "user":
                runner = runs[i]["run"]["players"][0]["id"]
                time = runs[i]["run"]["times"]["primary_t"]
                
                if not runner in runners:
                    runners[runner] = {}
                runners[runner][cat] = time

    # Replaced runner IDs with runner names.
    runners = getRunnerNames(runners)

    # Pull from a separate unsubmitted times file an overwrite if they are faster.
    with open("unsubmittedTimes.json", "r") as f:
        unsubmittedRuns = json.load(f)

    for runner in runners.keys():
        if runner in unsubmittedRuns.keys():
            for cat in cats:
                if cat in unsubmittedRuns[runner].keys():
                    if cat in runners[runner].keys():
                        runners[runner][cat] = min(unsubmittedRuns[runner][cat], runners[runner][cat])
                    else:
                        runners[runner][cat] = unsubmittedRuns[runner][cat]
        

    with open("runnersDL.json", "w") as f:
        json.dump(runners, f)


def getRunnerNames(runners: dict) -> dict:
    """
    Replaces all the IDs in a runners dict with names
    Parameters:
        runners - dict in {"id1": {"cat1": 100}, {"cat2": 200}} format
    Returns:
        newRunners - identical dict with the IDs replaced with runner names
    """
    with open("runnerNames.json", "r") as f:
        runnerNames = json.load(f)
    newRunners = {}
    count = 0
    length = len(runners)
    for runner in runners:
        count += 1

        # First check the runnerNames file to see if the name is cached
        print("Attempting to retrieve", runner)
        if runner in runnerNames.keys():
            print("Found name locally!")
            name = runnerNames[runner]
        else: 
            # If the name was not cached, ping srcom to retrieve it and add it to the runnerNames file
            print("Couldn't find name locally, asking speedrun.com")
            runnerJson = requests.get(f"https://speedrun.com/api/v1/users/{runner}").json()
            name = runnerJson["data"]["names"]["international"]
            runnerNames[runner] = name
        newRunners[name] = runners[runner]
        print(f"Got {name}! ({count}/{length})")

    with open("runnerNames.json", "w") as f:
        json.dump(runnerNames, f)
    return newRunners

if __name__ == "__main__":
    pullRunners(500)