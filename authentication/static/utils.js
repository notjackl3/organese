// const navbarCollapse = document.getElementById('navbarNav');
// const navItems = navbarCollapse.querySelectorAll('.nav-item');
// navItems.forEach(item => item.classList.add('mx-4'));

document.addEventListener("DOMContentLoaded", function () {
const dropdown = document.querySelector(".nav-item.dropdown");
const toggle = dropdown.querySelector('[data-bs-toggle="dropdown"]');
const menuElement = dropdown.querySelector(".dropdown-menu");

let hideTimeout;

dropdown.addEventListener("mouseenter", function () {
    clearTimeout(hideTimeout);
    const dropdownInstance = bootstrap.Dropdown.getOrCreateInstance(toggle);
    dropdownInstance.show();
});

dropdown.addEventListener("mouseleave", function () {
    hideTimeout = setTimeout(() => {
    const dropdownInstance = bootstrap.Dropdown.getInstance(toggle);
    dropdownInstance.hide();
    }, 200); // Delay to allow cursor movement
});

menuElement.addEventListener("mouseenter", function () {
    clearTimeout(hideTimeout);
});

menuElement.addEventListener("mouseleave", function () {
    hideTimeout = setTimeout(() => {
    const dropdownInstance = bootstrap.Dropdown.getInstance(toggle);
    dropdownInstance.hide();
    }, 200);
});
});
