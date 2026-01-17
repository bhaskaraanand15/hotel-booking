// ===== Backend API URL =====
const API_URL = "https://hotel-booking-233l.onrender.com";

let selectedBooking = null;

// ===== Load hotel room status from backend =====
async function loadStatus() {
  try {
    const res = await fetch(`${API_URL}/rooms/status`);
    const data = await res.json();
    renderGrid(data);
  } catch (err) {
    console.error("Status fetch failed:", err);
    alert("Unable to load hotel status. Backend might be down.");
  }
}

// ===== Render room grid =====
function renderGrid(data) {
  const grid = document.getElementById("hotelGrid");
  grid.innerHTML = "";
  selectedBooking = null;

  for (let floor = 10; floor >= 1; floor--) {
    const row = document.createElement("div");
    row.classList.add("floor-row");

    const label = document.createElement("span");
    label.classList.add("floor-label");
    label.innerText = `Floor ${floor}`;
    row.appendChild(label);

    for (let r of data[floor]) {
      const div = document.createElement("div");
      div.classList.add("room");
      div.innerText = r.room;

      if (r.occupied) {
        div.classList.add("occupied");
        div.onclick = () => openVacateModal(r.booking_id, r.room);
      }

      row.appendChild(div);
    }

    grid.appendChild(row);
  }
}

// ===== Book specific room =====
async function bookRoom() {
  const room = parseInt(document.getElementById("roomInput").value);

  if (!room) {
    alert("Enter room number.");
    return;
  }

  const res = await fetch(`${API_URL}/book?room=${room}`, { method: "POST" });

  if (!res.ok) {
    const msg = await res.json();
    alert(msg.detail || "Booking failed");
    return;
  }

  await loadStatus();
}

// ===== Random booking =====
async function randomFill() {
  await fetch(`${API_URL}/random`, { method: "POST" });
  await loadStatus();
}

// ===== Reset hotel =====
async function resetHotel() {
  await fetch(`${API_URL}/reset`, { method: "POST" });
  await loadStatus();
}

// ===== Vacate Modal Logic =====
function openVacateModal(bid, room) {
  selectedBooking = bid;

  document.getElementById("modalTitle").innerText = `Vacate Booking #${bid}?`;
  document.getElementById("modalRoom").innerText = `Room: ${room}`;
  document.getElementById("vacateModal").style.display = "flex";

  document.getElementById("confirmVacateBtn").onclick = async () => {
    await fetch(`${API_URL}/vacate?bid=${bid}`, { method: "POST" });
    closeModal();
    await loadStatus();
  };

  document.getElementById("cancelVacateBtn").onclick = closeModal;
}

function closeModal() {
  document.getElementById("vacateModal").style.display = "none";
}

// ===== Initial load =====
loadStatus();
