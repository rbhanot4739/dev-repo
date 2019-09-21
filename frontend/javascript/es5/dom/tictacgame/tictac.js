console.log('Welcome !!');
var boxes = document.querySelectorAll("td")
var restart = document.querySelector(".btn")

// function to clear the box contents
function clearBox() {
	for (box of boxes) {
		box.textContent = ""
	}
}

// clear the boxes on clicking the restart button
restart.addEventListener("click", clearBox)

// checking the boxes
for (box of boxes) {
	box.addEventListener('click', function() {
		if (this.textContent === "") {
			this.textContent = 'X'
		} else if (this.textContent === 'X') {
			this.textContent = 'O'
		} else {
			this.textContent = ""
		}
	})
}
