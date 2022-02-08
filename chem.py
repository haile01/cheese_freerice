import json
import random

def getTable():
    table = json.loads(open("table.json", "rb").read())
    res = []
    for elem in table["elements"]:
        res.append({"name": elem["name"].lower(), "symbol": elem["symbol"]})

    return res

def getAns(question, answers):
    question = question.lower()
    for elem in table:
        if elem["name"] == question:
            for ans in answers:
                if ans["text"] == elem["symbol"]:
                    return ans["id"]

            # in some weird case (maybe?), just take default
            return answers[random.randint(0, 3)]["id"]

    # Can't find the element, hmmp
    return answers[random.randint(0, 3)]["id"]

table = getTable()

# level 1
# category = "b4c85d38-2535-5aba-8e7e-17533fa298b5"
# level 2
category = "b67b50af-a735-536c-9532-ee26c05962eb"
