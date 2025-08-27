from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routers import events, analytics, eda_router, dashboard, realtime, games, home, quiz_api, tutorial

app = FastAPI(
    title="🚀 User Engagement Analytics Platform",
    description="Interactive platform with real-time analytics, EDA insights, and gamified learning",
    version="2.0.0"
)

app.include_router(home.router)
app.include_router(tutorial.router)
app.include_router(events.router)
app.include_router(analytics.router)
app.include_router(eda_router.router)
app.include_router(dashboard.router)
app.include_router(realtime.router)
app.include_router(games.router)
app.include_router(quiz_api.router)

@app.get("/")
async def root():
    """Redirect to unified homepage"""
    return RedirectResponse(url="/home/")
