
const themeCheck = () => {
  const theme = localStorage.getItem('theme');
  if (theme === 'dark') {
    document.getElementById('themeSwitch').checked = true;
    document.html.getAttribute('data-theme') = 'dark';
  } else {
    document.getElementById('themeSwitch').checked = false;
  }
};

window.onload = () => {
  themeCheck();
};

const toggleTheme = () => {
  const theme = localStorage.getItem('theme');
  if (theme === 'dark') {
    localStorage.setItem('theme', 'light');
  } else {
    localStorage.setItem('theme', 'dark');
  }
};