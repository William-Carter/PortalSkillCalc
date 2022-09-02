import json
import csv
from addUnfilledCategories import addUnfilledCategories
records = {
    "glitchless": 871.845, 
    "legacy": 694.77,
    "unrestricted": 646.02,
    "inbounds": 515.5,
    "oob": 353.46
}
cats = ["glitchless", "legacy", "unrestricted", "inbounds", "oob"]




def calcKinch(runner: dict) -> dict:
    """
    Calculates kinchranks (wr/pb*100) for a given player dict
    Parameters:
        player - standard player dict

    Returns:
        ret - Player dict with run times replaced with kinch ranks
    """
    ret = {}
    for cat in cats:
        if runner[cat]:
            kinch = (records[cat]/runner[cat]*100)

            ret[cat] = kinch
        else:
            ret[cat] = 0

    return ret

def adjustNosla(playerKinches: dict) -> dict:
    """
    Applies weighting to nosla legacy and nosla unrestricted
    Parameters:
        playerKinches - Player kinch dict
    Returns:
        mine - Player kinch dict with kinchranks adjusted based on weighting algorithm
    """
    # Both noslas are very similar, so the lower kinch one is multiplied by this to make it worth less
    # This is in order to stop nosla players from being able to be good at 1 category and reap the rewards of being good at 2
    duplicateMultiplier = 0.2 

    mine = playerKinches
    if mine["legacy"] == mine["unrestricted"]:
        mine["legacy"] += 0.01 # Small increment because legacy is more important than unrestricted :sunglasses:

    if mine["legacy"] > mine["unrestricted"]:
        mine["unrestricted"] *= duplicateMultiplier
    else:
        mine["legacy"] *= duplicateMultiplier

        
    return mine

def adjustGlitchless_Nosla(playerKinches):
    """
    Applies weighting to nosla legacy/unrestricted and glitchless
    Parameters:
        playerKinches - Player kinch dict (expects that noslas have already been adjusted)
    Returns:
        mine - Player kinch dict with kinchranks adjusted based on weighting algorithm
    """
    # Glitchless and nosla (both) are very similar in strategy.
    # To account for this overlap, the category with the lowest kinch between glitchless and the higher kinch nosla is reduced according to this amount
    balanceMultiplier = 0.8

    

    mine = playerKinches
    if mine["unrestricted"] > mine["legacy"]:
        nosla = "unrestricted"
    else:
        nosla = "legacy"

    if mine["glitchless"] == mine[nosla]:
        mine["glitchless"] += 0.01 # Small increment because glitchless is more important than nosla :sunglasses:

    if mine["glitchless"] > mine[nosla]:
        mine[nosla] *= balanceMultiplier
    else:
        mine["glitchless"] *= balanceMultiplier

    return mine

def adjustInbounds_Nosla(playerKinches, initialKinches):
    """
    Applies weighting to nosla legacy/unrestricted and inbounds
    Parameters:
        playerKinches - Player kinch dict (expects that noslas and glitchless have already been adjusted)
    Returns:
        mine - Player kinch dict with kinchranks adjusted based on weighting algorithm
    """
    # Inbounds and nosla (both) are very similar in strategy.
    # To account for this overlap, the category with the lowest kinch between inbounds and the higher kinch nosla is reduced according to this amount
    balanceMultiplier = 0.9

    

    mine = playerKinches
    if initialKinches["unrestricted"] > initialKinches["legacy"]:
        nosla = "unrestricted"
    else:
        nosla = "legacy"


    if initialKinches["inbounds"] == initialKinches[nosla]:
        initialKinches["inbounds"] += 0.01 # Small increment because inbounds is more important than nosla :sunglasses:


    if initialKinches["inbounds"] > initialKinches[nosla]:
        mine[nosla] *= balanceMultiplier
    else:
        mine["inbounds"] *= balanceMultiplier

    return mine

def catScaling(runner: dict) -> dict:
    """
    Scales all 5 categories by a fixed per-category value. Currently not used.
    """
    scaling = {
        "glitchless": 1,
        "legacy": 1,
        "unrestricted": 1,
        "inbounds": 1,
        "oob": 1
    }
    for cat in scaling.keys():
        runner[cat] *= scaling[cat]

    return runner


def calcSkill(player:dict, divide: bool = True, debug: bool = True) -> float:
    """
    Takes a standard player dict and finds the single number that represents their skill
    Parameters:
        player - the player dict
        divide - whether or not to normalise skill value, needed for initial pass to find normalisation factor
        debug - name of player to dump incremental kinch values for
    """

    if debug: print(player)
    player = addUnfilledCategories(player)
    if debug: print(player)


    kinches = calcKinch(player)
    if debug: print(kinches)


    kinches = catScaling(kinches)
    
    initialKinches = kinches.copy()

    kinches = adjustNosla(kinches)
    if debug: print(kinches)

    kinches = adjustGlitchless_Nosla(kinches)
    if debug: print(kinches)

    kinches = adjustInbounds_Nosla(kinches, initialKinches)
    if debug: print(kinches)
  

    kinches = list(kinches.values())
    kinches.sort(reverse=True)

    finalScore = sum(kinches)
    if divide:
        finalScore = finalScore/divisor

    return round(finalScore, 2)


divisor = calcSkill(records, divide=False, debug=False)/100


def getCatString(player):
    str = ""
    for cat in player.keys():
        if player[cat] != "":
            str+=cat[0]
            str+= ","
    str = str[:-1]
    return str

if __name__ == "__main__":
    with open("runnersDL.json", "r") as f:
        runners = json.load(f)

    output = []
    val = False
    for runner in runners.keys():
        
        skill = calcSkill(runners[runner], debug=val, divide=True)
        output.append([runner, skill])
        val = False


    output = sorted(output, key=lambda k: k[1], reverse=True)

    with open("result.csv", "w", newline="") as f:
        e = csv.writer(f, delimiter=",")
        for row in output:
            e.writerow(row)