document.getElementById('logout-link').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('logout-form').submit(); 
    console.log("did it")
});