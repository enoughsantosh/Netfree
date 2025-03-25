from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import httpx
from fastapi.middleware.cors import CORSMiddleware
import logging
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
            raise HTTPException(status_code=e.response.status_code, detail=str(e.response.text))
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/s")
async def process_search(q: str, h: str):
    url = f"https://iosmirror.cc/search.php?s={q}"
    cookies = {"t_hash_t": h}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, cookies=cookies)
            response.raise_for_status()

            # Attempt to parse JSON
            try:
                result = response.json()
                if result.get("status") == "y":
                    return JSONResponse(content={"searchResult": result.get("searchResult", [])})
                else:
                    return JSONResponse(content={"message": result})
            except ValueError:
                return JSONResponse(status_code=500, content={"status": "failure", "message": "Invalid JSON response from the server."})
        
        except httpx.RequestError as e:
            return JSONResponse(status_code=500, content={"status": "failure", "message": f"Request error: {str(e)}"})
        except Exception as e:
            return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@app.get("/sp")
async def process_pvsearch(q: str, h: str):
    url = f"https://iosmirror.cc/pv/search.php?s={q}"
    cookies = {"t_hash_t": h}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, cookies=cookies)
            response.raise_for_status()

            # Attempt to parse JSON
            try:
                result = response.json()
                if result.get("status") == "y":
                    return JSONResponse(content={"searchResult": result.get("searchResult", [])})
                else:
                    return JSONResponse(content={"message": result})
            except ValueError:
                return JSONResponse(status_code=500, content={"status": "failure", "message": "Invalid JSON response from the server."})
        
        except httpx.RequestError as e:
            return JSONResponse(status_code=500, content={"status": "failure", "message": f"Request error: {str(e)}"})
        except Exception as e:
            return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
            
@app.get("/m")
async def process_ei(q: str, h: str):
    url = f"https://iosmirror.cc/playlist.php?id={q}"
    cookies = {
        "t_hash_t": h,
        "hd": "on",
        "lang": "hin"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, cookies=cookies)
            response.raise_for_status()

            # Attempt to parse JSON
            try:
                result = response.json()
                return JSONResponse(content={"searchResult": result})
            except ValueError:
                return JSONResponse(status_code=500, content={
                    "status": "failure", 
                    "message": "Invalid JSON response from the server."
                })
        
        except httpx.RequestError as e:
            return JSONResponse(status_code=500, content={
                "status": "failure", 
                "message": f"Request error: {str(e)}"
            })
        except Exception as e:
            return JSONResponse(status_code=500, content={
                "status": "error", 
                "message": str(e)
            })

@app.get("/p")
async def process_find(q: str, h: str):
    url = f"https://iosmirror.cc/post.php?id={q}"
    cookies = {"t_hash_t": h}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, cookies=cookies)
            response.raise_for_status()

            # Attempt to parse JSON
            try:
                result = response.json()
                if result.get("status") == "y":
                    return JSONResponse(content={"searchResult": result})
                else:
                    return JSONResponse(content={"message": result})
            except ValueError:
                return JSONResponse(status_code=500, content={
                    "status": "failure", 
                    "message": "Invalid JSON response from the server."
                })
        
        except httpx.RequestError as e:
            return JSONResponse(status_code=500, content={
                "status": "failure", 
                "message": f"Request error: {str(e)}"
            })
        except Exception as e:
            return JSONResponse(status_code=500, content={
                "status": "error", 
                "message": str(e)
            })

@app.get("/e")
async def process_epi(q: str, h: str, k: Optional[str] = None):
    url = f"https://iosmirror.cc/episodes.php?s={k}&series={q}"
    cookies = {"t_hash_t": h}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, cookies=cookies)
            response.raise_for_status()

            # Attempt to parse JSON
            try:
                result = response.json()
                if result.get("status") == "y":
                    return JSONResponse(content={"searchResult": result})
                else:
                    return JSONResponse(content={"message": result})
            except ValueError:
                return JSONResponse(status_code=500, content={
                    "status": "failure", 
                    "message": "Invalid JSON response from the server."
                })
        
        except httpx.RequestError as e:
            return JSONResponse(status_code=500, content={
                "status": "failure", 
                "message": f"Request error: {str(e)}"
            })
        except Exception as e:
            return JSONResponse(status_code=500, content={
                "status": "error", 
                "message": str(e)
            })
