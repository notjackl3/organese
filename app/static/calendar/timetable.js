async function POST(day, hour, content, timetable_id) {
    try {
        const response = await fetch(`/entries/`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCookie("csrftoken"),
            },
            credentials: "include",
            body: JSON.stringify({
              day_of_week: day,
              hour: hour,
              content: content,
              timetable_id: parseInt(timetable_id)
            }),
        })
        if (!response.ok) throw new Error("Failed to save entry.");
        data = await response.json()
        console.log("Entry saved:", data);
    } catch (error) {
        console.error("Error:", error);
    }
}


async function DELETE(pk) {
    try {
        const response = await fetch(`/entries/change/${pk}/`, {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCookie("csrftoken"),
            },
            credentials: "include",
        });
        if (!response.ok) throw new Error("Failed to delete entry.");
    } catch (error) {
        console.error("Error:", error);
    }
}


async function LOOKUPDELETE(day, hour, timetable_id) {
    try {
        const response = await fetch(`/entries/lookup/`, { 
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCookie("csrftoken"),
            },
            credentials: "include",
            body: JSON.stringify({
              day_of_week: day,
              hour: hour,
              timetable_id: timetable_id
            }),
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Failed to find entry.");
        }
        const data = await response.json();
        if (data.multiple) {
            for (const entry of data.pk) {
                DELETE(entry.id);
            }
            return false
        }
        else {
            DELETE(data.pk);
        };
    } catch (error) {
        console.error("Error:", error);
        return null; 
    }
}


async function CREATETABLE(timetable_name, user_id) {
    try {
        const response = await fetch("/table/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCookie("csrftoken"),
            },
            credentials: "include",
            body: JSON.stringify({
                name: timetable_name,
                is_public: false,
                user_id: user_id
            }),
        })
        if (!response.ok) throw new Error("Failed to save entry.");
        data = await response.json()
        console.log("Entry saved:", data);
    } catch (error) {
        console.error("Error:", error);
    }
}


async function BOOK(guest_name, guest_email, day, hour, content, timetable_id) {
    try {
        const response = await fetch(`/booking/create/`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({
                guest_name: guest_name,
                guest_email: guest_email,
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

