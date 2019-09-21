const resp = prompt('Would you like to use web-app y/n ?');
if (resp === 'y') {
  const users = [];
  while (action !== 'quit') {
    var action = prompt('Please select an action: ":add/display/remove/quit"');
    if (action === 'add') {
      var name = prompt('Enter a name to add');
      users.push(name);
    } else if (action === 'display') {
      console.log(users);
    } else if (action === 'remove') {
      name = prompt('Enter a name to remove');
      const index = users.indexOf(name);
      users.splice(index, 1);
    }
  }
  alert('Thank you for using the web-app !!');
} else {
  alert('Thank you for visiting !!');
}
