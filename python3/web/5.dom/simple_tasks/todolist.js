var lis = document.querySelectorAll("li")

for (li of lis) {

  li.addEventListener("mouseover", function () {
    this.classList.add("hovered")
  })

  li.addEventListener("mouseout", function () {
    this.classList.remove("hovered")
  })

  li.addEventListener("click", function () {
    this.classList.toggle("clicked")
  })


}