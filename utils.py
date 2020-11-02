from config import NEEDED_MATCHING_RATIO
from difflib import SequenceMatcher

def getMatchRatio(s, ss):
    matcher = SequenceMatcher(None, s.lower(), ss.lower())
    return matcher.ratio()

def checkName(s, ss, ratio=NEEDED_MATCHING_RATIO): 
    if s.lower() == ss.lower():
        return True
    elif getMatchRatio(s, ss) > ratio:
        return True
    return False

def checkInName(one, two): 
    one = one.lower().split()
    two = two.lower().split()
    length = min(len(one), len(two))
    
    r = 0
    for i in range(length):
        if checkName(one[i], two[i]):
            r += 1

    return (r == length and r != 0)

def checkOne(one, full):
    for word in full.split():
        if checkName(one, word):
            return True
    return False


