/* === Darkmode Implementation === */
let darkmode = localStorage.getItem('darkmode');
const themeSwitch = document.getElementById('theme-switch');

const enableDarkmode = () => {
  document.body.classList.add('darkmode');
  themeSwitch.checked = true;
  localStorage.setItem('darkmode', 'active');
};

const disableDarkmode = () => {
  document.body.classList.remove('darkmode');
  themeSwitch.checked = false;
  localStorage.setItem('darkmode', null);
};

if (darkmode === "active") enableDarkmode();

themeSwitch.addEventListener("click", () => {
  darkmode = localStorage.getItem('darkmode');
  darkmode !== "active" ? enableDarkmode() : disableDarkmode();
});

console.log(darkmode, themeSwitch)
