from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from booking_logic import (
    load_state, save_state, room_exists, is_occupied,
    commit_booking, vacate_booking, reset_hotel,
    state, ALL_ROOMS, random_room
)

app = FastAPI()

# CORS for frontend (GitHub Pages)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_state()

@app.get("/rooms/status")
def status():
    occupied_map = {}
    for b in state["bookings"]:
        r = b["rooms"][0]
        occupied_map[r] = b["id"]

    data = {}
    for floor in range(1, 11):
        floor_rooms = ALL_ROOMS[floor]
        data[floor] = [
            {
                "room": r,
                "occupied": r in occupied_map,
                "booking_id": occupied_map.get(r)
            }
            for r in floor_rooms
        ]
    return data


@app.post("/book")
def book(room: int):
    if not room_exists(room):
        raise HTTPException(400, f"Room {room} does not exist.")
    if is_occupied(room):
        raise HTTPException(400, f"Room {room} is already occupied.")

    bid = commit_booking(room)
    return {"status": "booked", "booking_id": bid, "room": room}


@app.post("/random")
def random_fill():
    room = random_room()
    if room is None:
        raise HTTPException(400, "No rooms available.")

    bid = commit_booking(room)
    return {"status": "booked", "booking_id": bid, "room": room}


@app.post("/vacate")
def vacate(bid: int):
    vacate_booking(bid)
    return {"status": "vacated", "booking_id": bid}


@app.post("/reset")
def reset():
    reset_hotel()
    return {"status": "reset"}


@app.get("/bookings")
def bookings():
    return state["bookings"]


@app.on_event("shutdown")
def shutdown_event():
    save_state()
