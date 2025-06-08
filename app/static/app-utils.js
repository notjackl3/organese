document.getElementById("logout-link").addEventListener("click", function(event) {
    event.preventDefault();
    document.getElementById("logout-form").submit(); 
    console.log("did it")
});

document.querySelectorAll(".time-item").forEach(item => {
    let clickCount = 0;
    const paragraph = item.querySelector("p");

    item.addEventListener("click", () => {
      clickCount++;
  
      if (clickCount === 1) {
        item.style.overflowY = "auto";
        item.style.cursor = "text";
      } else if (clickCount === 2) {
        paragraph.contentEditable = "true";
        paragraph.focus();
        item.classList.remove("hoverable");
      }
    });
  
    item.addEventListener("mouseleave", () => {
      item.style.overflowY = "hidden";
      paragraph.contentEditable = "false";
      item.style.cursor = "pointer";
      item.classList.add("hoverable");
      clickCount = 0;
    });
  });