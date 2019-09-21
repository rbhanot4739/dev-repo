// Turn the item to red color and strike through to mark it as completed

$("ul").on("click", "li", function () {
    $(this).toggleClass("completed")
});


// delete the item on clicking the delete button

$("ul").on("click", "span", function (event) {
    $(this).parent().fadeOut(400, function () {
        $(this).remove();
    });
    // this is necessary to stop the event bubbling from propagating to parent elements.
    event.stopPropagation();
});

// Add new item
$("#textinput").on("keypress", function (event) {
    if (event['which'] === 13) {
        var todoText = ($(this).val());
        $("ul").append("<li><span><i class='fas fa-trash'></i></span> " + todoText + "</li>");
        $(this).val("");
    }
});


$(".fa-plus").on("click", function () {
    $("#textinput").fadeToggle(350)
});