from fastapi import FastAPI, HTTPException
import httpx
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware
import logging
import re
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Movie Search API is running!"}

@app.get("/cookie")
async def fetch_cookie():
    url = "https://netmirror.8man.me/api/cookie"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()  # Raise an error for non-200 responses
            return response.json()  # Assuming the API returns JSON data
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

@app.route('/s', methods=['GET'])
def process_search():
    try:
        # Get the hash value from the query parameters
        s_value = request.args.get('q')
        h_value = request.args.get('h')

        
        url = f"https://iosmirror.cc/search.php?s={s_value}" 


        cookies = {
            "t_hash_t": h_value
        }

        
        # Make the POST request
        response = requests.get(url, cookies=cookies)

        # Check for errors in the response
        response.raise_for_status()
        # If the response is JSON, process it
        try:
            result = response.json()
            if result.get("status") == "y":
                search_result = result.get("searchResult", [])
                return jsonify({
                    "searchResult": search_result
                 
                })
            else:
                return jsonify({
                    "message": result
                         })
                
 
                
                    
               

        except ValueError:
            return jsonify({
                "status": "failure",
                "message": "Invalid JSON response from the server."
            }), 500
            
    except requests.exceptions.RequestException as e:
        # Handle network or HTTP errors
        return jsonify({
            "status": "failure",
            "message": f"Request error: {str(e)}"
        }), 500
    except Exception as e:
        # Catch any other exceptions
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
