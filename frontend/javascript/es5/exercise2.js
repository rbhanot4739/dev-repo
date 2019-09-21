const fname = prompt("Enter your first name");
const lname = prompt("Enter your last name");
const age = prompt("Enter your age");
const height = prompt("Enter your height");
const pet_name = prompt("Enter your pet name");

if (
  fname[0] === lname[0] &&
  age >= 25 &&
  age <= 35 &&
  height >= 160 &&
  pet_name[pet_name.length - 1] === "y"
) {
  console.log("You are a spy");
} else {
  console.log("Nothing for you!!");
}
