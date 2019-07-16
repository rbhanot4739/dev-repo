function changeColor() {
	var h1 = document.querySelector("h1")
	var h2 = document.querySelector("h2")
	var h3 = document.querySelector("h3")
	h1.style.color = getcolor()
	h2.style.color = getcolor()
	h3.style.color = getcolor()
}

function getcolor() {
	var letters = '0123456789ABCDEF'
	var color = "#"
	for (i = 0; i < 6; i++) {
		color += letters[Math.floor(Math.random() * 16)]
	}
	return color;
}

setInterval("changeColor()", 1000)
