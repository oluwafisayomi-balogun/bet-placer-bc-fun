import requests
import time
import os
from dotenv import load_dotenv
load_dotenv()

BASE_URL = "https://api-k-c7818b61-623.sptpub.com"
BRAND_ID = os.getenv("BRAND_ID")
TOKEN = os.getenv("TOKEN")

def place_bet(bet_data):
    for key in ["bet_type_specifier", "stake_amount", "odds"]:
        if key not in bet_data:
            return {"error": f"Missing required field: {key}"}

    # Check based on bet type
    if bet_data["bet_type_specifier"] == "1/1":
        for key in ["event_id", "market_id", "outcome_id"]:
            if key not in bet_data:
                return {"error": f"Missing required field for single bet: {key}"}
    else:  # combo/system bets like 2/2, 3/3
        if "selections" not in bet_data or len(bet_data["selections"]) == 0:
            return {"error": "Missing 'selections' for combo/system bet"}
        #also check that each selection has event_id, market_id, outcome_id
        for sel in bet_data["selections"]:
            for field in ["event_id", "market_id", "outcome_id"]:
                if field not in sel:
                    return {"error": f"Missing '{field}' in one of the selections"}

    url = f"{BASE_URL}/api/v2/coupon/brand/{BRAND_ID}/bet/place"
    
    bet_type = bet_data['bet_type_specifier']
    try:
        if bet_type == "1/1":
            bet_request_id = f"{bet_data['event_id']}-{bet_data['market_id']}--{bet_data['outcome_id']}"
        else: #for combo & system bets
            if "selections" not in bet_data or not bet_data['selections']:
                raise ValueError("Missing selections for combo/system bet")
            bet_request_id = ":".join(f"{sel['event_id']}-{sel['market_id']}--{sel['outcome_id']}" for sel in bet_data['selections'])
    except Exception as e:
        print(f"Logic for {bet_type} hasn't been implemented yet: {e}")
            
    timestamp = int(time.time() * 1000)
    
    if bet_data["bet_type_specifier"] == "1/1":
        selections_payload = [
            {
                "event_id": bet_data["event_id"],
                "market_id": bet_data["market_id"],
                "specifiers": "",
                "outcome_id": bet_data["outcome_id"],
                "k": str(bet_data["odds"]),
                "source": {
                    "layout": "tile",
                    "page": "/:sportSlugAndId",
                    "section": "Top",
                    "extra": {"market": "Event Plate", "timeFilter": "", "banner_type": "BetbyAI", "tab": ""}
                },
                "promo_id": None,
                "bonus_id": None,
                "timestamp": timestamp
            }
        ]
    else:  # combo/system bets
        selections_payload = []
        for sel in bet_data["selections"]:
            selections_payload.append({
                "event_id": sel["event_id"],
                "market_id": sel["market_id"],
                "specifiers": "",
                "outcome_id": sel["outcome_id"],
                "k": str(sel["odds"]),
                "source": {
                    "layout": "tile",
                    "page": "/:sportSlugAndId",
                    "section": "Top",
                    "extra": {"market": "Event Plate", "timeFilter": "", "banner_type": "BetbyAI", "tab": ""}
                },
                "promo_id": None,
                "bonus_id": None,
                "timestamp": timestamp
            })

    payload = [
        {
            "type": bet_data["bet_type_specifier"],
            "sum": str(bet_data["stake_amount"]),
            "k": str(bet_data["odds"]),  # combined odds for combo bets
            "global_id": None,
            "bonus_id": None,
            "bet_request_id": bet_request_id,
            "odds_change": "higher",
            "selections": selections_payload
        }
    ]

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Origin": "https://bc.fun",
        "Referer": "https://bc.fun/"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()  

        try:
            return response.json()
        except ValueError:
            return {"error": "Invalid JSON response", "response_text": response.text}

    except requests.Timeout:
        return {"error": "Request timed out"}
    except requests.ConnectionError:
        return {"error": "Connection error"}
    except requests.HTTPError as e:
        return {"error": f"HTTP error {response.status_code}", "response_text": response.text}
    except Exception as e:
        return {"error": str(e)}


bet_data_1 = {
    "event_id": "2574931793602027558",
    "market_id": "1",
    "outcome_id": "2",
    "bet_type_specifier": "1/1", #this is the single betting
    "stake_amount": 150,
    "odds": 2.9
}

bet_data_2 = {
    "selections": [
        {
            "event_id": "2580300328788439079",
            "market_id": "1",
            "outcome_id": "1",
            "odds": 1.33
        },
        {
            "event_id": "2581503353842442276",
            "market_id": "1",
            "outcome_id": "1",
            "odds": 2.46
        }],
    "market_id": "1",
    "outcome_id": "1",
    "bet_type_specifier": "2/2", #this is the combo betting
    "stake_amount": 150,
    "odds": 3.272
}


# Test 1
result1 = place_bet(bet_data_1)
print("Test 1 result:", result1)

# Test 2
result2 = place_bet(bet_data_2)
print("Test 2 result:", result2)
