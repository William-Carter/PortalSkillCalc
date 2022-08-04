import requests
import json
portalID = "4pd0n31e"

noslaID = "n2yq98ko"
inboundsID = "7wkp6v2r"
oobID = "lvdowokp"
glitchlessID = "wk6pexd1"

legUnVar = "ql61qmv8"
unresVal = "21g5r9xl"
legacyVal = "jqz97g41"

def getRuns() -> None:
    """
    Requests the leaderboard for each category and dumps it to a json file.
    Will place 5 json files in the program directory.
    """
    inboundsLB = requests.get(f"https://speedrun.com/api/v1/leaderboards/{portalID}/category/{inboundsID}").json()
    with open("inboundsDL.json", "w") as f:
        json.dump(inboundsLB, f)


    oobLB = requests.get(f"https://speedrun.com/api/v1/leaderboards/{portalID}/category/{oobID}").json()
    with open("oobDL.json", "w") as f:
        json.dump(oobLB, f)

    glitchlessLB = requests.get(f"https://speedrun.com/api/v1/leaderboards/{portalID}/category/{glitchlessID}").json()
    with open("glitchlessDL.json", "w") as f:
        json.dump(glitchlessLB, f)

    legacyLB = requests.get(f"https://speedrun.com/api/v1/leaderboards/{portalID}/category/{noslaID}?var-{legUnVar}={legacyVal}").json()
    with open("legacyDL.json", "w") as f:
        json.dump(legacyLB, f)

    unrestrictedLB = requests.get(f"https://speedrun.com/api/v1/leaderboards/{portalID}/category/{noslaID}?var-{legUnVar}={unresVal}").json()
    with open("unrestrictedDL.json", "w") as f:
        json.dump(unrestrictedLB, f)

if __name__ == "__main__":
    getRuns()