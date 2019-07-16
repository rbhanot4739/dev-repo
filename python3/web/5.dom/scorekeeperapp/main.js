var p1show = document.querySelector("#s1")
var p2show = document.querySelector("#s2")
var shwlimit = document.querySelector("#shwlimit")

var p1btn = document.querySelector("#p1")
var p2btn = document.querySelector("#p2")
var reset = document.querySelector("#rst")
var limit = document.querySelector("#limit")

var p1score = 0
var p2score = 0
var gameOver = false;
var winScore = 5
var winScore = limit.value

p1btn.addEventListener("click", function () {
  if (!gameOver) {
    p1score += 1;
    p1show.textContent = p1score
    if (p1score === winScore) {
      gameOver = true;
      p1show.classList.add("winner")
    }
  }
})

p2btn.addEventListener("click", function () {
  if (!gameOver) {
    p2score += 1;
    p2show.textContent = p2score
    if (p2score === winScore) {
      gameOver = true;
      p2show.classList.add("winner")
    }
  }
})

limit.addEventListener("click", function () {
  winScore = Number(this.value);
  shwlimit.textContent = this.value;
  res()
})

reset.addEventListener("click", function () {
  res()
  limit.value = ""
  winScore = 5
  shwlimit.textContent = 5;
})

function res() {
  gameOver = false
  p1score = 0;
  p2score = 0;
  p1show.textContent = p1score;
  p2show.textContent = p2score;

  p1show.classList.remove("winner")
  p2show.classList.remove("winner")
}



// ---- Alternate solution in process ------ 
// var player1 = {
//   name: "Player1",
//   showScore: document.querySelector("#s1"),
//   score: 0,
//   btn: document.querySelector("#p1")
// }

// var player2 = {
//   name: "Player2",
//   showScore: document.querySelector("#s2"),
//   score: 0,
//   btn: document.querySelector("#p2")
// }

// function gameStatus() {
//   console.log(this)
//   // if (this.score != winScore) {
//   //   this.score += 1;
//   //   this.showScore.textContent = this.score
//   // } else {
//   //   console.log(this.name, "has won")
//   // }
// }

// // console.log(player1)

// player1.btn.addEventListener("click", gameStatus)