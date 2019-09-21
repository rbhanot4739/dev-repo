let resp = prompt('Are you there yet');

// while (resp.indexOf("yes") === -1) {
// 	resp = prompt('Are you there yet');
// }

while (true) {
  resp = prompt('Are you there yet ?');
  if (resp.indexOf('yes') !== -1) {
    break;
  }
}

alert('Congrats you are there !!');
