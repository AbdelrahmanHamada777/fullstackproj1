var signInBtn = document.querySelector(".sign_in");
var userBox = document.querySelector(".userBox");
var welcomeText = document.getElementById("welcome");
var logoutBtn = document.getElementById("logout");

var username = localStorage.getItem("Username");

if (username && signInBtn && userBox && welcomeText) {
    signInBtn.style.display = "none";
    userBox.style.display = "flex";
    welcomeText.textContent = `Welcome, ${username}`;
}

if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
        localStorage.removeItem("Username");
        window.location.reload();
    });
}
