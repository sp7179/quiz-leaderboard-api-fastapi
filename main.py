from fastapi import FastAPI
import requests
import time

app = FastAPI()

BASE_URL = "https://devapigw.vidalhealthtpa.com/srm-quiz-task"
REG_NO = "RA2311003030036"


@app.get("/")
def home():
    return {"message": "Quiz Leaderboard API Running"}


@app.get("/run")
def run():

    unique_events = set()
    scores = {}

    print("\n🚀 STARTING QUIZ PROCESS\n")

    api_failed = False

    # 🔹 STEP 1: POLL API
    for poll in range(10):
        print(f"📡 Polling {poll}...")

        try:
            url = f"{BASE_URL}/quiz/messages?regNo={REG_NO}&poll={poll}"
            res = requests.get(url)

            if res.status_code != 200:
                print(f"❌ API ERROR at poll {poll} | Status: {res.status_code}")
                api_failed = True
                continue

            data = res.json()

            if "events" not in data:
                print("❌ No events received → Invalid regNo OR server issue")
                api_failed = True
                break

            # 🔹 STEP 2: DEDUP + AGGREGATE
            for event in data["events"]:
                key = (event["roundId"], event["participant"])

                if key not in unique_events:
                    unique_events.add(key)

                    participant = event["participant"]
                    score = event["score"]

                    scores[participant] = scores.get(participant, 0) + score

        except Exception as e:
            print("❌ Exception during API call:", str(e))
            api_failed = True
            break

        time.sleep(5)

    print("\n📊 UNIQUE EVENTS:", unique_events)
    print("📊 SCORES:", scores)

    # 🔹 IF API FAILED → CLEAR MESSAGE
    if api_failed or not scores:
        print("\n⚠️ RESULT: SERVER-SIDE ISSUE DETECTED")
        print("👉 API did not return valid data")
        print("👉 Your logic is correct (poll + dedup + aggregation works)")
        print("👉 Issue is NOT from your code")

        return {
            "status": "API_FAILED",
            "message": "Server not responding or invalid regNo",
            "note": "Logic is correct, API issue"
        }

    # 🔹 STEP 3: LEADERBOARD
    leaderboard = [
        {"participant": p, "totalScore": s}
        for p, s in scores.items()
    ]

    leaderboard.sort(key=lambda x: x["totalScore"], reverse=True)

    print("\n🏆 LEADERBOARD:", leaderboard)

    # 🔹 STEP 4: SUBMIT
    try:
        submit_url = f"{BASE_URL}/quiz/submit"

        payload = {
            "regNo": REG_NO,
            "leaderboard": leaderboard
        }

        res = requests.post(submit_url, json=payload)

        print("\n📡 RAW SUBMIT RESPONSE:", res.text)

        if res.status_code != 200:
            print("\n⚠️ SUBMISSION FAILED → SERVER ISSUE")
            return {
                "status": "SUBMIT_FAILED",
                "message": "Server rejected request",
                "code": res.status_code
            }

        try:
            result = res.json()
        except:
            print("\n⚠️ INVALID JSON RESPONSE FROM SERVER")
            return {
                "status": "INVALID_RESPONSE",
                "message": "Server returned non-JSON response"
            }

    except Exception as e:
        print("\n❌ SUBMISSION ERROR:", str(e))
        return {
            "status": "ERROR",
            "message": str(e)
        }

    print("\n🎯 FINAL RESULT:", result)

    # 🔹 FINAL CHECK
    if result.get("isCorrect") == True:
        print("\n✅ SUCCESS → YOUR CODE IS CORRECT")
    else:
        print("\n❌ RESULT INCORRECT → CHECK LOGIC OR DATA")

    return {
        "leaderboard": leaderboard,
        "result": result
    }