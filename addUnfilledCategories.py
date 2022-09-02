from cgi import test


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
        runner = propagateTimes(runner)
    return runner


def propagateTimes(runner: dict):
    for category in runner:
        runTimes = []
        for cat in cats:
            runTimes.append(runner[cat])
        validTimes = runTimes[:cats.index(category)+1]
        validTimes = [i for i in validTimes if i != ""]
        if len(validTimes) == 0:
            runner[category] = ""
        else:
            runner[category] = min(validTimes)
        
    return runner


if __name__ == "__main__":
    testRunner = {"glitchless": 2323,
    "legacy": "",
    "unrestricted": 2425,
    "inbounds": 1234,
    "oob": 894
    }
    print(propagateTimes(testRunner))