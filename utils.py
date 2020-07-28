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

def checkInName(part, full, firstWord=True): 
	part = part.lower()
	full = full.lower()
	if checkName(part, full):
		return True

	if firstWord:
		(part, *_) = part.split(maxsplit=1)

	if part in full:
		return True
	for word in full.split():
		if getMatchRatio(part, word) > NEEDED_MATCHING_RATIO:
			return True
	return False
		
