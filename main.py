from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.scrapper import ScraperService
from services.notification import Notification
from models.settings import ScraperSettings

# Initialize the app
app = FastAPI()

# Static token for authentication.
API_TOKEN = "STATIC_SECURE_TOKEN"


def authenticate(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")


# Endpoint to trigger scraping
@app.post("/scrape", dependencies=[Depends(authenticate)])
async def scrape(settings: ScraperSettings):
    scraper = ScraperService(settings)
    count = scraper.run_scraping()
    Notification.notify(f"Scraped and updated {count} products")
    return {"message": f"Successfully scraped and updated {count} products"}
