
function showNav() {
    var x = document.getElementById("header-ul");
    if (x.style.display === "flex") {
        x.style.display = "none";
    } else {
        x.style.display = "flex";
    }
}

document.getElementById('nav-bar-burger').addEventListener('click',showNav)