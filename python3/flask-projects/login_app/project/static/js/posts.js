let delPost = document.querySelector(".delpost");

function deletePost() {
    console.log('test')
}

delPost.forEach(function (elem) {
    elem.addEventListener('click', function () {
        deletePost()
    })
});
