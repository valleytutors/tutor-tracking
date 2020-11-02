from notion.client import NotionClient
from utils import checkInName
import config

client = NotionClient(token_v2=config.NOTION_AUTH_TOKEN)

tutorView = client.get_collection_view(config.NOTION_TUTOR_PAGE)
tutors = tutorView.collection

dataPage = client.get_block(config.NOTION_DATA_PAGE)
lastRowBlock = dataPage.children[1]

def lastRow(n=None):
    if n != None:
        lastRowBlock.title = n
    else:
        return int(lastRowBlock.title)

def getTutor(name):
    for t in tutors.get_rows():
        if checkInName(name, t.title):
            return t
    return None



