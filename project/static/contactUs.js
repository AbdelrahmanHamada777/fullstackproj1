
const form = document.querySelector('form');

form.addEventListener('submit', function(event) {
    
    
    event.preventDefault();

    
    alert("Thank you! Your message has been sent successfully.");

    form.reset();
});
document.querySelectorAll('.card-link').forEach(el => {
    el.addEventListener('click', () => {
      const url = el.getAttribute('data-url');
      if (url) window.location.href = url;
    });
  });


var sign_in = document.querySelector(".sign_in");
sign_in.addEventListener("click", () => {
    const url = sign_in.getAttribute('data-url');
    if (url) window.location.href = url;
});


