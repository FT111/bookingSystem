
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

const newError = (message) => {
  console.log(message);
  document.body.innerHTML += `
  <div class="toast" id="warningToast">
    <div class="alert alert-error text-base-200">
      <span>${message}</span>
    </div>
  </div>

  `;
};

const formatter = new Intl.NumberFormat('en-GB', {
  style: 'currency',
  currency: 'GBP',

  // These options are needed to round to whole numbers if that's what you want.
  //minimumFractionDigits: 0, // (this suffices for whole numbers, but will print 2500.10 as $2,500.1)
  //maximumFractionDigits: 0, // (causes 2500.99 to be printed as $2,501)
});
