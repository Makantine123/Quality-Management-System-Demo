// Script to manage index.html

const container = document.getElementById('container');
const registrationBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registrationBtn.addEventListener('click', () => {
  container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
  container.classList.remove("active");
});
