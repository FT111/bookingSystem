
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
    document.documentElement.setAttribute('data-theme', 'business');
    localStorage.setItem('theme', 'dark');
  }
};

const newError = (message) => {
  console.log(message);
  document.body.innerHTML += `
  <div class="toast" id="warningToast">
    <div class="alert alert-error text-base-200">
      <span>${message}</span>
    </div>
  </div>

  `;

  setTimeout(() => {
    document.getElementById('warningToast').remove();
  }, 2000);
};

const newSuccessAlert = (message) => {
  console.log(message);
  document.body.innerHTML += `
  <div class="toast" id="warningToast">
    <div class="alert alert-success text-base-content">
      <span>${message}</span>
    </div>
  </div>
  `;

  setTimeout(() => {
    document.getElementById('warningToast').remove();
  }, 2000);
};

const formatter = new Intl.NumberFormat('en-GB', {
  style: 'currency',
  currency: 'GBP',
});
