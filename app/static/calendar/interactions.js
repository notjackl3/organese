var old_content = ""
var click_count = 0
var curr_clicked = ""
var curr_day = ""
var curr_hour = ""
var curr_timetable_id = document.body.dataset.timetable;
var curr_user_id = document.body.dataset.id;


function getData(item, paragraph) {
    const day = item.getAttribute("data-day");
    const hour = parseInt(item.getAttribute("data-hour"));
    const content = paragraph.textContent.trim();
    return [day, hour, content];
}


document.querySelectorAll(".time-item").forEach(item => {
    const paragraph = item.querySelector("p");
    const overlay = item.querySelector(".overlay");
    item.addEventListener("click", async (e) => {
        if (item.classList.contains("disabled")) {
            e.preventDefault();
            e.stopPropagation();
            return;
        }
        click_count++;
        old_content = paragraph.textContent.trim();
        if (click_count === 1) {
            item.style.overflowY = "auto";
            item.style.cursor = "text";
            overlay.style.display = "flex";
        } else if (click_count === 2) {
            item.classList.remove("hoverable");
            overlay.style.display = "none";
            paragraph.contentEditable = "true";
            paragraph.focus();
            if (curr_clicked == "add") {
                paragraph.innerHTML = "";
                paragraph.classList.add("content")
            }
            else if (curr_clicked == "delete") {
                const [day, hour, content] = getData(item, paragraph);
                const pk = await LOOKUPDELETE(day, hour, curr_timetable_id);
                location.reload();
            }
            else if (curr_clicked == "book" && paragraph.innerHTML == "") {
                const [day, hour, content] = getData(item, paragraph);
            }
            // Flow:
            // Customer book a schedule
            // Booking will go to the user's requests
            // User will choose to accept the request or not
            // If they do then the request is added to their timetable
        }
    });

    item.addEventListener("mouseleave", () => {
        item.style.overflowY = "hidden";
        paragraph.contentEditable = "false";
        paragraph.classList.remove("content")

        if (!item.classList.contains("disabled")) {
            item.classList.add("hoverable");
            item.style.cursor = "pointer";
        }
        overlay.style.display = "none";
        if (click_count == 2) {
            const [day, hour, content] = getData(item, paragraph);
            if (curr_clicked == "book") {
                guest_name = document.getElementById("guest-name-input");
                guest_email = document.getElementById("guest-email-input");
                if (guest_name.value != "") {
                    BOOK(guest_name.value, guest_email.value, day, hour, content, curr_timetable_id);
                }
                else {
                    guest_name.placeholder = "Enter your booking name";
                    guest_name.style.background = "yellow";
                    const paragraph = item.querySelector("p");
                    paragraph.innerHTML = "";
                }
                curr_clicked = "";
                click_count = 0;
                return;
            }
            if (old_content != content) {
                if (old_content != "") {
                    LOOKUPDELETE(day, hour, curr_timetable_id)
                }
                if (content != "") {
                    POST(day, hour, content, curr_timetable_id);
                }
            }
        }
        click_count = 0;
    });
});
