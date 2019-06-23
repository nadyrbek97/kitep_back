let popular = document.getElementById("popular");
    popular.style.color = "#111";

    popular.addEventListener("onmouseover", function () {
        popular.style.color = "#898989";
    });

    popular.addEventListener('onmouseleave', function () {
        popular.style.color = "#111";

    });

function mouseOver() {
    popular.style.color = "#898989";
}

function mouseLeave() {
    popular.style.color = "#000000";
}


let jumboButton = document.getElementById("jumbo-Btn");
jumboButton.addEventListener('onclick', function () {
    console.log("1");
});


// function truncateText(selector, maxLength) {
//     var element = document.querySelector(selector),
//         truncated = element.innerText;
//
//     if (truncated.length > maxLength){
//         truncated = truncated.substr(0, maxLength) + "...";
//     }
//     return truncated;
// }
//
// document.querySelector('p').innerText = truncateText('p',50)
//
// var book = document.querySelector("#book-description")
//
// book.innerText = truncateText(book,50)