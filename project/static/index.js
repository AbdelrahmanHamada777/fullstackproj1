document.querySelectorAll('.card-link').forEach(el => {
  el.addEventListener('click', () => {
    const url = el.getAttribute('data-url');
    if (url) window.location.href = url;
  });
});

var sign_in = document.querySelector(".sign_in");
if (sign_in) {
  sign_in.addEventListener("click", () => {
    const url = sign_in.getAttribute('data-url');
    if (url) window.location.href = url;
  });
}

document.addEventListener('DOMContentLoaded', function () {
  const chatbotIcon = document.querySelector(".chatbot");
  const chatbotSidebar = document.getElementById("chatbotSidebar");
  const closeChatbot = document.getElementById("closeChatbot");

  if (chatbotIcon && chatbotSidebar && closeChatbot) {
    chatbotIcon.addEventListener("click", () => {
      chatbotSidebar.classList.add("active");
    });

    closeChatbot.addEventListener("click", () => {
      chatbotSidebar.classList.remove("active");
    });
  }
});
