# bet-placer-bc-fun

This Python script allows programmatic bet placement on `bc.fun` via its API. It currently supports single bets (`1/1`) and combo/system bets (`2/2`, `2/3`) etc with proper error handling.

---

### 1. Environment Setup

Uses environment variables for sensitive information:

- `BRAND_ID`: Brand identifier, stored in environment variables.  
- `TOKEN`: Bearer token for authentication.  
- `.env` file keeps sensitive information outside source code.  

---

### 2. Features

- **Multiple Bet Types:** Single (`1/1`) and combo/system (`2/2`, `2/3`) bets etc.
- **Input Validation:** Checks required fields e.g (`event_id`, `market_id`, `outcome_id`, `stake_amount`, `odds`) for all bets.  
- **Error Handling:** Handles HTTP errors, timeouts, connection errors, and invalid JSON responses.  
- Uses Bearer token; no session management required.  

---

### 3. Function: `place_bet(bet_data)`

Accepts a dictionary containing bet details, builds the appropriate JSON payload depending on bet type, sends a `POST` request to the bet placement endpoint, and returns the API response.

- Validates required fields for single and combo/system bets.  
- Constructs `bet_request_id` dynamically for single or multiple selections.  
- Sends request 

---

### 4. Example Bet Data

#### Single Bet (`1/1`)

- Represents a single bet with event, market, outcome, stake, and odds.
- IDs captured from **browser DevTools network requests**.

Fields:

- `event_id`: Unique identifier for the match/event.  
- `market_id`: Identifier for the bet market.  
- `outcome_id`: Identifier for the specific betting outcome.  
- `bet_type_specifier`: Type of bet
- `stake_amount`: Amount wagered.  
- `odds`: Odds applied to this bet.

#### Combo/System Bet (`2/2`, `3/3`)

- Represents multiple selections combined into one bet.  
- `selections`: Array of individual bets, each with `event_id`, `market_id`, `outcome_id`, `odds`.  
- `bet_type_specifier`: e.g `"2/2"` for a two-selection combo bet.  
- `stake_amount` and `odds` represent total stake and combined odds.  

---

### 5. Running the Script

- Call `place_bet(bet_data)` with either a **single bet** or **combo/system bet**.  
- Receives API response indicating success (`accepted`) or failure (`error`).  
- Print or log response for validation and debugging.  

---


### 7. Clarifications/Limitations
**Token Management**: The script does not perform login and relies on a pre-obtained JWT token. Login is handled manually, and the JWT token is extracted from browser storage. Since tokens may expire, you must manually update the environment variables with the new JWT token before running the script.

**Manual Bet Data Input**: Currently, the `bet_data` dictionary must be manually provided for each bet. The script does not automatically fetch bet details.



