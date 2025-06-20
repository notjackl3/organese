const guestTimetableId = document.body.dataset.timetable;
var curr_clicked = ""
var curr_day = ""
var curr_hour = ""


fetch(`/entries-guest/?timetable_id=${guestTimetableId}`, {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
    },
})
.then(response => {
    if (!response.ok) throw new Error("Failed to load entry.");
    return response.json();
})
.then(data => {
    data.forEach(item => {
        const selector = `.time-item[data-day="${item.day_of_week}"][data-hour="${item.hour}"]`;
        const cell = document.querySelector(selector);
        if (cell) {
            const paragraph = cell.querySelector("p");
            paragraph.textContent = "Busy";
            cell.classList.remove("bg-light");
            cell.classList.add("disabled");
            cell.classList.remove("hoverable");
            cell.style.cursor = "not-allowed";
            cell.style.backgroundColor = "silver";
        }
    });
})
.catch(error => {
    console.error("Error:", error);
});


document.querySelectorAll(".btn-custom.book").forEach(button => {
    button.addEventListener("click", (event) => {
        const item = event.target.closest(".time-item");
        curr_clicked = "book"
        curr_day = item.dataset.day;
        curr_hour = item.dataset.hour
    });
});
document.querySelectorAll(".btn-custom.cancel").forEach(button => {
    button.addEventListener("click", (event) => {
        const item = event.target.closest(".time-item");
        curr_clicked = "cancel"
        curr_day = item.dataset.day;
        curr_hour = item.dataset.hour
    });
});