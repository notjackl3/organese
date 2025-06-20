curr_clicked = "";
curr_day = "";
curr_hour = "";
curr_content = "";
curr_booking_id = "";
curr_timetable_id = "";

function getData(item) {
    curr_day = item.dataset.day;
    curr_hour = item.dataset.hour;
    curr_content = item.dataset.content;
    curr_timetable_id = item.dataset.timetable;
    curr_booking_id = item.dataset.booking;
    return curr_day, curr_hour, curr_content, curr_timetable_id
}

document.querySelectorAll(".accept-btn").forEach(button => {
    button.addEventListener("click", (event) => {
        const item = event.target.closest(".booking-item");
        getData(item);
        ADDTIMETABLE(curr_day, curr_hour, curr_content, curr_timetable_id);
        DELETEBOOKING(curr_booking_id);
        location.reload();
    });
});
document.querySelectorAll(".reject-btn").forEach(button => {
    button.addEventListener("click", (event) => {
        const item = event.target.closest(".booking-item");
        getData(item);
        ADDTIMETABLE(curr_day, curr_hour, curr_content, curr_timetable_id);
        DELETEBOOKING(curr_booking_id);
        location.reload();
    });
});
