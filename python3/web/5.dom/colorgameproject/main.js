var squares = document.querySelectorAll(".square")
var colorDisplay = document.getElementById("colDisplay");
var header = document.getElementsByClassName("header")[0]
var resDisplay = document.getElementById('result')
var reset = document.getElementById('reset')
var levels = document.querySelectorAll(".level")

var numColumns = 6
setColors(numColumns)

// Event listener for playing level buttons
for (i = 0; i < levels.length; i++) {
  levels[i].addEventListener("click", function () {
    for (j = 0; j < levels.length; j++) {
      levels[j].classList.remove("selected")
    }
    this.classList.add('selected')

    if (this.textContent === "easy") {
      numColumns = 3
    }
    if (this.textContent === "hard") {
      numColumns = 6
    }
    setColors(numColumns)
    colorDisplay.textContent = correctColor.toUpperCase();
  })
}

// click event for reset button
reset.addEventListener("click", function () {
  setColors(numColumns)
  reset.textContent = "NEW COLORS"
  resDisplay.textContent = ""
  header.style.backgroundColor = 'steelblue'
})

// adding the click event for squares
for (i = 0; i < squares.length; i++) {
  squares[i].addEventListener("click", function () {
    matchColor(this)
  })
}


function setColors(num) {
  colors = randomColorGenerator(num);
  correctColor = colors[Math.floor(Math.random() * colors.length)]
  colorDisplay.textContent = correctColor.toUpperCase();
  // setting the bg colors for squares
  for (i = 0; i < squares.length; i++) {
    squares[i].style.display = "block"
    if (colors[i]) {
      squares[i].style.backgroundColor = colors[i]
    } else {
      squares[i].style.display = "none"
    }
  }
}

function randomColorGenerator(num) {
  randColors = []
  for (i = 0; i < num; i++) {
    var r = Math.floor(Math.random() * 256)
    var g = Math.floor(Math.random() * 256)
    var b = Math.floor(Math.random() * 256)
    randColors.push("rgb(" + r + ", " + g + ", " + b + ")")
  }
  return randColors
}

function matchColor(obj) {
  squareColor = obj.style.backgroundColor;

  if (squareColor === correctColor) {
    // change the h1 backgroundColor to match the correct color
    header.style.backgroundColor = correctColor;
    // change the backgroundColor of all the squares to match the correct color
    for (square of squares) {
      square.style.backgroundColor = correctColor
    }
    // chnage the result display
    resDisplay.textContent = "you won !"
    resDisplay.style.color = "steelblue"
    // change the lable of the New Colors button to Play Again
    reset.textContent = "PLAY AGAIN ?"


  } else {
    // set the backgroundColor of sqaure to match the body color
    obj.style.backgroundColor = "#232323"
    resDisplay.textContent = "TRY AGAIN !!"
    resDisplay.style.color = "red"
  }
}