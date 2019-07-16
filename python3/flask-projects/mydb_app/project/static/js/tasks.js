const options = document.querySelectorAll('.hideme');
const submit_btn = document.querySelector('.js_button');

function toggle_options(state) {
  for (let i = 0; i < options.length; i++) {
    options[i].style.visibility = state;
  }
}

console.log('tasks page load');
// hide the options drop down list at page load
toggle_options('hidden');

submit_btn.addEventListener('click', function () {
  console.log('button clicked');
  toggle_options('visible');
  this.style.visibility = 'hidden';
});
