document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.getElementById("public-toggle");

    toggle.addEventListener("change", function () {
        fetch(`/update-settings/${timetableId}`, {
            method: "POST",
            headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken"),
            },
            body: `is_public=${toggle.checked ? "on" : ""}`,
            credentials: "include"
        })
        .then(response => {
            if (!response.ok) throw new Error("Failed to update settings.");
            console.log("Settings updated");
        })
        .catch(error => {
            console.error("Error:", error);
        });
        });
});


const timetableId = document.body.dataset.timetable;
fetch(`/entries/?timetable_id=${timetableId}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    credentials: "include",
})
.then(response => {
    if (!response.ok) throw new Error("Failed to save entry.");
    return response.json();
})
.then(data => {
    data.forEach(item => {
        const selector = `.time-item[data-day="${item.day_of_week}"][data-hour="${item.hour}"]`;
        const cell = document.querySelector(selector);
        if (cell) {
          const paragraph = cell.querySelector("p");
          paragraph.textContent = item.content;
        }
    });
})
.catch(error => {
    console.error("Error:", error);
});


document.querySelectorAll(".btn-custom.add").forEach(button => {
    button.addEventListener("click", (event) => {
        const item = event.target.closest(".time-item");
        curr_clicked = "add"
        curr_day = item.dataset.day;
        curr_hour = item.dataset.hour
    });
});
document.querySelectorAll(".btn-custom.edit").forEach(button => {
    button.addEventListener("click", (event) => {
        const item = event.target.closest(".time-item");
        curr_clicked = "edit"
        curr_day = item.dataset.day;
        curr_hour = item.dataset.hour
    });
});
document.querySelectorAll(".btn-custom.delete").forEach(button => {
    button.addEventListener("click", (event) => {
        const item = event.target.closest(".time-item");
        curr_clicked = "delete"
        curr_day = item.dataset.day;
        curr_hour = item.dataset.hour
    });
});


document.getElementById("copy-link-btn").addEventListener("click", function () {
    const baseUrl = window.location.origin;
    const username = this.getAttribute("data-username");
    const timetable = this.getAttribute("data-timetable");
    const fullUrl = `${baseUrl}/calendar-guest/${username}/${timetable}`;
    navigator.clipboard.writeText(fullUrl).then(function() {
        alert("Link copied to clipboard!");
    }, function(err) {
        alert("Failed to copy: " + err);
    });
});


document.getElementById("timetable-btn").addEventListener("click", function () {
    document.getElementById("timetable-btn").style.display = "none";
    document.getElementById("timetable-edit-btn").style.display = "none";
    document.getElementById("timetable-name-input").style.display = "block";
    document.getElementById("timetable-choose").style.display = "inline-block";
    document.getElementById("timetable-add").style.display = "inline-block";
    document.getElementById("timetable-delete").style.display = "inline-block";
    document.getElementById("timetable-cancel").style.display = "inline-block";
});


document.getElementById("timetable-cancel").addEventListener("click", function () {
document.getElementById("timetable-btn").style.display = "block";
document.getElementById("timetable-edit-btn").style.display = "block";
document.getElementById("timetable-name-input").style.display = "none";
document.getElementById("timetable-change").style.display = "none";
document.getElementById("timetable-choose").style.display = "none";
document.getElementById("timetable-add").style.display = "none";
document.getElementById("timetable-delete").style.display = "none";
document.getElementById("timetable-cancel").style.display = "none";
});

document.getElementById("timetable-edit-btn").addEventListener("click", async function () {
    document.getElementById("timetable-edit-btn").style.display = "none";
    document.getElementById("timetable-btn").style.display = "none";
    document.getElementById("timetable-name-input").style.display = "block";
    document.getElementById("timetable-change").style.display = "inline-block";
    document.getElementById("timetable-cancel").style.display = "inline-block";
});

document.getElementById("timetable-choose").addEventListener("click", async function () {
    query = document.getElementById("timetable-name-input").value;
    window.location.href = `http://127.0.0.1:8000/calendar/${query}`;
});

document.getElementById("timetable-change").addEventListener("click", async function () {
    query = document.getElementById("timetable-name-input").value;
    await CHANGETABLENAME(timetableId, curr_user_id, query);
    window.location.reload();
});

document.getElementById("timetable-add").addEventListener("click", function () {
    query = document.getElementById("timetable-name-input").value;
    CREATETABLE(query, curr_user_id);
});