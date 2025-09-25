# bet-placer-bc-fun

This Python script allows programmatic bet placement on `bc.fun` via its API.  
It currently supports single bets (`1/1`) and combo/system bets (`2/2`, `2/3`, etc.) with proper error handling.

---

## 1. Environment Setup

The script uses environment variables for sensitive information:

- `TOKEN`: Bearer token for authentication.  
- `.env` file keeps sensitive information outside source code.  

---

## 2. Features

- **Multiple Bet Types:** Single (`1/1`) and combo/system (`2/2`, `2/3`, etc.).  
- **Input Validation:** Ensures required fields (`event_id`, `market_id`, `outcome_id`, `stake_amount`, `odds`, `specifier`) are provided.  
- **Error Handling:** Handles HTTP errors, timeouts, connection issues, and invalid JSON responses.  
- **Bearer Token Authentication:** No session management required.  

---

## 3. Function: `place_bet(bet_data)`

Accepts a dictionary containing bet details, builds the appropriate JSON payload depending on bet type, sends a `POST` request to the bet placement endpoint, and returns the API response.

- Validates required fields for single and combo/system bets.  
- Constructs `bet_request_id` dynamically for single or multiple selections.  
- Sends the request and returns the API response.  

---

## 4. API Request/Response Structure

### Endpoint
**POST**  
```
[https://api-k-c7818b61-623.sptpub.com/api/v2/coupon/brand/2103509236163162112/bet/place]

````

Authentication requires a **Bearer token (JWT)** in the request headers.

### Example Request Payload

```json
[
  {
    "type": "1/1",
    "sum": "150",
    "k": "6.6",
    "global_id": null,
    "bonus_id": null,
    "bet_request_id": "2578958162564616214-1--3",
    "odds_change": "higher",
    "selections": [
      {
        "event_id": "2578958162564616214",
        "market_id": "1",
        "specifiers": "",
        "outcome_id": "3",
        "k": "6.6",
        "source": {
          "layout": "tile",
          "page": "/:sportSlugAndId",
          "section": "Top",
          "extra": {
            "market": "Event Plate",
            "timeFilter": "",
            "banner_type": "BetbyAI",
            "tab": ""
          }
        },
        "promo_id": null,
        "bonus_id": null,
        "timestamp": 1758735643948
      }
    ]
  }
]
````

### Example Response (Success)

```json
{
  "accepted": [
    {
      "bet_request_id": "2578958162564616214-1--3",
      "bet_id": "2582690316226273885",
      "bonus_id": null
    }
  ],
  "error": []
}
```

---

## 5. Example Bet Data

### Single Bet (`1/1`)

Represents a single bet with event, market, outcome, stake, specfier and odds.
IDs are captured from **browser DevTools network requests**.

**Fields:**

* `event_id`: Unique identifier for the match/event.
* `market_id`: Identifier for the bet market.
* `outcome_id`: Identifier for the specific betting outcome.
* `bet_type`: Type of bet\wager.
* `stake_amount`: Amount wagered.
* `odds`: Odds applied to this bet.
* `specifier`: extra details that define this bet.

---

### Combo/System Bet (`2/2`, `3/3`)

Represents multiple selections combined into one bet.

* `selections`: Array of individual bets, each with `event_id`, `market_id`, `outcome_id`, `odds`, `specifiers`.
* `bet_type`: e.g. `"2/2"` for a two-selection combo bet.
* `stake_amount` and `odds`: Represent total stake and combined odds.
* `specifier`: e.g hcp

---

### Notes on Payload Fields
as seen on the Developer tools

* `sum`: Stake amount.
* `k`: Odds value.
* `type`: Bet type or wager type (e.g. `"1/1"` for single bets).
* `event_id`, `market_id`, `outcome_id`: Identify the bet selection.
* `bet_request_id`: Unique identifier for this bet (format: `<event_id>-<market_id>--<outcome_id>`).
* `specifier`: Extras you can bet on
* Response includes a unique `bet_id` if accepted.

---

## 6. Running the Script

* Call `place_bet(bet_data)` with either a **single bet** or a **combo/system bet**.
* Receives API response indicating success (`accepted`) or failure (`error`).
* Print or log the response for validation and debugging.

---

## 7. Tools & Methods Used

To discover the hidden API used for placing bets, the following approach was used:

* **Browser Developer Tools (Chrome DevTools):**

  * Opened the **Network** tab and filtered requests by **Fetch/XHR**.
  * Placed a test bet with the minimum stake.
  * Observed the outgoing request made to the bookmaker’s server (`place`).
  * Instead of placing bets, booked them down (`create`) to explore bet construction further.

---

## 8. Clarifications & Limitations

* **Token Management:**
  The script does not perform login. It relies on a pre-obtained JWT token (extracted from browser storage). Since tokens may expire, you must manually update the environment variables with the new JWT token before running the script.

* **Manual Bet Data Input:**
  Currently, the `bet_data` dictionary must be manually provided for each bet. The script does not automatically fetch bet details.


---

