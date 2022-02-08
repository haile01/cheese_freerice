import requests
import json
import time
import random
import chem

# Decrease with yo own risks ;) (in seconds ofc)
MIN_DELAY = 2
MAX_DELAY = 4 

s = requests.Session()
s.get("https://freerice.com/profile-login")

def getLoginHeaders():
    return {"origin": "https://freerice.com", "authority": "accounts.freerice.com", "accept": "application/vnd.api+json;version=2"} 

# cred file format: <username>:<password>
def login():
    acc = open("account.txt", "r").read().strip().split(":")
    data = f'{{"username": "{acc[0]}", "password": "{acc[1]}"}}'
    headers = getLoginHeaders()
    r = s.post("https://accounts.freerice.com/auth/login?_format=json&_lang=en", data=data, headers=headers)
    res = json.loads(r.text)
    print(f"Signed in as {res['userData']['username']}")
    return res["token"], res["uuid"]

def extract(res):
    res = json.loads(res)

    if "errors" in res:
        # Shit, go backkkk
        print(res)
        # exit()
        # Nah, just do over ;)
    
    link = res["data"]["links"]["self"]
    res = res["data"]["attributes"]
    return res["question"]["text"].split(" =")[0], res["question_id"], res["question"]["options"], res["answer"]["correct"], res["user_rice_total"], link

def getPlayHeaders(token):
    return {"origin": "https://freerice.com", "authority": "engine.freerice.com", "accept": "application/vnd.api+json;version=2", "content-type": "application/json", "authorization": f"Bearer {token}"} 

def play(token, uuid):
    headers = getPlayHeaders(token)
    data = f'{{"category": "{chem.category}", "level": 1, "user": "{uuid}"}}'
    
    # Get initial question
    r = s.post("https://engine.freerice.com/games?lang=en", data=data, headers=headers)
    # print(r.text)
    try:
        question, qid, answers, correct, total, link = extract(r.text)
    except:
        return

    firstTime = True

    while True:
        if not firstTime:
            print("> Correct" if correct else "> False :(")
        firstTime = False

        if total % 100 == 0:
            print(f"Total: {total}")

        print(f"Question: {question}")
        # print(f"Options: {answers}")

        ans = chem.getAns(question, answers)

        print(f"Answered: {ans}")

        data = f'{{"question": "{qid}", "answer": "{ans}", "user": "{uuid}"}}'
        r = s.patch(f"{link}/answer?lang=en", data=data, headers=headers)

        # print(data, r.text)

        try:
            question, qid, answers, correct, total, link = extract(r.text)
        except:
            return
        time.sleep(random.randint(MIN_DELAY, MAX_DELAY))

def main():
    print("> Starting...")
    token, uuid = login()
    while True:
        play(token, uuid)

if __name__ == "__main__":
    main()

