import json
import csv
records = {
    "glitchless": 871.845, 
    "legacy": 694.77,
    "unrestricted": 646.02,
    "inbounds": 515.5,
    "oob": 355.32
}
cats = ["glitchless", "legacy", "unrestricted", "inbounds", "oob"]


def addUnfilledCategories(runner: dict) -> dict:
    """
    Adds categories to runner dict that aren't already there. 
    If it can reuse a lower hierarchy time it will (e.g. glitchless will be used for nosla), otherwise it will leave it blank.
    Parameters:
        runner - Runner dict with only the categories the player has competed in.
    Returns:
        runner - Runner dict with all categories, with new categories either upfilled or blank.
    """
    containedCategories = []
    for cat in runner.keys():
        containedCategories.append(cats.index(cat))
    
    for cat in cats:
        if not cat in runner.keys():
            runner[cat] = ""
            if cats.index(cat) > max(containedCategories):
                runner[cat] = runner[cats[max(containedCategories)]]

    return runner


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
        mine["legacy"] += 0.01 # Small increment because legacy is more important than nosla :sunglasses:

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

    if mine["glitchless"] > mine[nosla]:
        mine[nosla] *= balanceMultiplier
    else:
        mine["glitchless"] *= balanceMultiplier

    return mine

def adjustInbounds_Nosla(playerKinches):
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
    if mine["unrestricted"] > mine["legacy"]:
        nosla = "unrestricted"
    else:
        nosla = "legacy"

    if mine["inbounds"] > mine[nosla]:
        mine[nosla] *= balanceMultiplier
    else:
        mine["inbounds"] *= balanceMultiplier

    return mine


def calcSkill(player:dict, divide: bool = True) -> float:
    """
    Takes a standard player dict and finds the single number that represents their skill
    Parameters:
        player - the player dict
        divide - whether or not to normalise skill value, needed for initial pass to find normalisation factor
    """

    # The players best categories are weighted heavier than their bad ones.
    # Might remove this, it's tough to say if it matters that much atm
    skillDropoff = -0.5 
    player = addUnfilledCategories(player)

    kinches = calcKinch(player)

    kinches = adjustNosla(kinches)
    kinches = adjustGlitchless_Nosla(kinches)
    kinches = adjustInbounds_Nosla(kinches)

    finalScore = 0
    kinches = list(kinches.values())
    kinches.sort(reverse=True)
    for index, kinch in enumerate(kinches):
        kinches[index] = kinch*(2**(skillDropoff*index))

    finalScore += sum(kinches)
    if divide:
        finalScore = finalScore/divisor

    return round(finalScore, 2)


divisor = calcSkill(records, divide=False)/100


def getCatString(player):
    str = ""
    for cat in player.keys():
        if player[cat] != "":
            str+=cat[0]
            str+= ","
    str = str[:-1]
    return str
with open("runnersDL.json", "r") as f:
    runners = json.load(f)

output = []
for runner in runners.keys():
    skill = calcSkill(runners[runner])
    output.append([runner, skill])

# I haven't tested this, if it's broken don't @ me
# output = sorted(output, key=lambda k: k[1])

with open("result.csv", "w", newline="") as f:
    e = csv.writer(f, delimiter=",")
    for row in output:
        e.writerow(row)