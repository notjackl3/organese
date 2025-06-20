document.getElementById("logout-link").addEventListener("click", function(event) {
    event.preventDefault();
    document.getElementById("logout-form").submit(); 
});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
        }
    }
    return cookieValue;
}