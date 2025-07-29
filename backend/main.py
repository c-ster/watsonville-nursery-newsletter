import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from backend.newsletter_generator import generate_newsletter_html
from pathlib import Path

app = FastAPI(
    title="Watsonville Nursery Newsletter API",
    description="API for managing newsletter content, subscribers, and sending.",
    version="1.0.0",
)

# --- CORS Middleware ---
# Allow all origins for now, but we'll restrict this in production.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

@app.get("/")
def read_root():
    """A simple health check endpoint."""
    return {"status": "ok", "message": "Welcome to the Watsonville Nursery Newsletter API"}



# --- Subscriber Management ---

class Subscriber(BaseModel):
    email: EmailStr

# This is a temporary in-memory database. We'll replace this later.
subscribers_db = []

@app.post("/subscribe")
def subscribe_newsletter(subscriber: Subscriber):
    """Subscribes a new user to the newsletter."""
    email = subscriber.email
    if email in subscribers_db:
        raise HTTPException(status_code=400, detail="Email already subscribed.")
    
    subscribers_db.append(email)
    print(f"New subscription: {email}") # Log to server console for now
    return {"message": f"Successfully subscribed {email}!"}


@app.post("/unsubscribe")
def unsubscribe_newsletter(subscriber: Subscriber):
    """Unsubscribes a user from the newsletter."""
    email = subscriber.email
    if email not in subscribers_db:
        raise HTTPException(status_code=404, detail="Email not found in subscribers list.")
    
    subscribers_db.remove(email)
    print(f"Unsubscribed: {email}") # Log to server console
    return {"message": f"Successfully unsubscribed {email}."}


@app.get("/content/{month}")
def get_monthly_content(month: str):
    """Retrieve the newsletter content for a specific month."""
    content = load_newsletter_content()
    month_lower = month.lower()
    if month_lower not in content:
        raise HTTPException(status_code=404, detail=f"Content for month '{month}' not found.")
    return content[month_lower]


@app.get("/preview/{month}", response_class=HTMLResponse)
async def preview_newsletter(month: str):
    """Generates and returns a preview of the monthly newsletter."""
    # For now, we'll use sample dynamic content.
    # In the future, this will come from a database or an admin input form.
    sample_dynamic_content = {
        "personalIntro": "There's a certain magic to the air this time of year on the coast. The morning fog rolls in like a soft blanket, giving the whole garden a drink and keeping the soil moist. It’s a peaceful time, perfect for a quiet morning walk with a cup of coffee, watching the world wake up. My family has always said this is the garden's 'breathing room' before the full heat of the day. It’s a great time to reflect on the season's successes and plan for the bounty still to come.",
        "subscriberQuestion": "My hydrangea leaves are turning yellow and crispy on the edges. What’s going on?",
        "subscriberAnswer": "That's a classic sign of 'leaf scorch' on hydrangeas, and it's very common in our area, especially on hot, windy afternoons. While it seems like a disease, it's actually a watering issue. The leaves are losing water faster than the roots can absorb it. To help, make sure you're watering deeply at the base of the plant in the morning. A 2-3 inch layer of mulch (like our premium fir bark) is also crucial to keep the roots cool and retain that precious moisture. For a long-term solution, consider moving it to a spot that gets more morning sun and afternoon shade.",
        "newArrivals": "You won't want to miss what just rolled in on the truck! We have a stunning selection of Salvia 'Hot Lips', with their unique red and white flowers that hummingbirds can't resist. We also have several new varieties of Heuchera (Coral Bells), whose colorful foliage can brighten up any shady spot in your garden.",
        "monthlySpecials": "Exclusively for our newsletter family: Take 20% off all 4-inch perennials this month! It's the perfect time to fill in those gaps in your flower beds with plants that will come back year after year.",
        "upcomingWorkshops": "Want to get more out of your small spaces? Join us for our 'Container Gardening Basics' workshop this Saturday at 10 AM. We'll cover soil selection, choosing the right plants, and proper watering techniques to ensure your pots and planters thrive all season long. Space is limited, so please call the nursery to sign up!"
    }

    html_content = generate_newsletter_html(month, sample_dynamic_content)
    if not html_content:
        raise HTTPException(status_code=404, detail=f"Could not generate newsletter for month '{month}'.")
    
    return HTMLResponse(content=html_content)


# Future endpoints will go here:
# - /subscribers
# - /send
