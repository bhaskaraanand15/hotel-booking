import json
import os
from typing import List

STATE_FILE = "state.json"


ALL_ROOMS = {
    floor: (
        [1000 + i for i in range(1, 8)] if floor == 10
        else [floor * 100 + i for i in range(1, 11)]
    )
    for floor in range(1, 11)
}

state = {
    "next_booking_id": 1,
    "bookings": []
}


def load_state():
    global state
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)


def save_state():
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def room_exists(room: int) -> bool:
    for rooms in ALL_ROOMS.values():
        if room in rooms:
            return True
    return False


def get_occupied_rooms() -> List[int]:
    occ = []
    for b in state["bookings"]:
        occ += b["rooms"]
    return occ


def is_occupied(room: int) -> bool:
    return room in get_occupied_rooms()


def commit_booking(room: int):
    bid = state["next_booking_id"]
    state["bookings"].append({"id": bid, "rooms": [room]})
    state["next_booking_id"] += 1
    save_state()
    return bid


def vacate_booking(bid: int):
    state["bookings"] = [b for b in state["bookings"] if b["id"] != bid]
    save_state()


def reset_hotel():
    state["bookings"] = []
    state["next_booking_id"] = 1
    save_state()


def get_available_rooms() -> List[int]:
    occupied = set(get_occupied_rooms())
    return [r for floor in ALL_ROOMS for r in ALL_ROOMS[floor] if r not in occupied]


def random_room() -> int:
    import random
    available = get_available_rooms()
    if not available:
        return None
    return random.choice(available)
