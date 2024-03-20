
const themeCheck = () => {
  const theme = localStorage.getItem('theme');
  if (theme === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dim');
    document.getElementById('themeSwitch').checked = true;
  } else {
    document.getElementById('themeSwitch').checked = false;
    document.documentElement.setAttribute('data-theme', 'nord');
  }
};

window.addEventListener("load",function(){
  themeCheck();
},false);

const toggleTheme = () => {
  const theme = localStorage.getItem('theme');
  if (theme === 'dark') {
    localStorage.setItem('theme', 'light');
    document.documentElement.setAttribute('data-theme', 'nord');

  } else {
    document.documentElement.setAttribute('data-theme', 'dim');
    localStorage.setItem('theme', 'dark');
  }
};