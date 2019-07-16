var btn = document.querySelector("button")
var body = document.querySelector("body")


// Soltion 1
// body.style.background = "white"
// btn.addEventListener("click", function() {
//   if (body.style.background === "white") {body.style.background = "grey"}
//   else {body.style.background = "white"}
// }
// )

// Solution 2. Better way of doing the same.

btn.addEventListener("click", function(){
  document.body.classList.toggle("grey")
})
