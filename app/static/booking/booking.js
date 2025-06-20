async function ADDTIMETABLE(day, hour, content, timetable_id) {
    try {
        const response = await fetch(`/booking/add/`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                day_of_week: day,
                hour: hour,
                content: content,
                timetable_id: timetable_id
            }),
        })
        if (!response.ok) throw new Error("Failed to save entry.");
        data = await response.json()
        console.log("Booking saved:", data);
    } catch (error) {
        console.error("Error:", error);
    }
}


async function DELETEBOOKING(pk) {
    try {
        const response = await fetch(`/booking/change/`, {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCookie("csrftoken"),
            },
            credentials: "include",
            body: JSON.stringify({
                booking_id: pk,
            }),
        });
        if (!response.ok) throw new Error("Failed to delete entry.");
    } catch (error) {
        console.error("Error:", error);
    }
}