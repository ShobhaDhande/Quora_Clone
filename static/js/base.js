document.getElementById("logout").style.display = "none";
function openModal() {
    document.getElementById("questionModal").style.display = "block";
}

function closeModal() {
    document.getElementById("questionModal").style.display = "none";
}

function openlogout(){
    console.log(document.getElementById("logout").style.display)
    document.getElementById("logout").style.display = document.getElementById("logout").style.display != "none" ? "none":"block";
}