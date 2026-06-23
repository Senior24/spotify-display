import keyboard
import uvicorn

from fastapi import FastAPI

import winrt.windows.media.control as wmc

app = FastAPI()

@app.get("/")
async def music_data():

    manager = await wmc.GlobalSystemMediaTransportControlsSessionManager.request_async()
    session = manager.get_current_session()

    if not session:
        return {
            "title": "No title",
            "artist": "No artist",
        }

    props = await session.try_get_media_properties_async()

    title = props.title
    artist = props.artist

    if len(title) > 18: title = title[:15] + "..."
    if len(artist) > 18: artist = artist[:15] + "..."

    return {
        "title": title,
        "artist": artist,
    }

@app.get("/prev")
async def prev_track():
    keyboard.press_and_release('previous track')

@app.get("/play_pause")
async def play_pause():
    keyboard.press_and_release('play/pause')

@app.get("/next")
async def next_track():
    keyboard.press_and_release('next track')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
