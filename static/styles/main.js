// Show Result Rating
let ratingText = document.querySelector('#rating-user');
let rating = document.querySelector('.star-ratings.mutable');
let ratingTop = document.querySelector('.star-ratings.top.mutable');
let latestRatingStr = "0%";
let latestRating = 0; 
let realTimeRatingStr = "0%";
let realTimeRating = 0;
if (rating != null) {
    rating.addEventListener("mousemove", ratingMoveHandler);
    rating.addEventListener("mouseout", ratingOutHandler);
    rating.addEventListener("click", ratingClickHandler);
}

let abslft = absoluteLeft(rating);
console.log("absolute left:", abslft);

let ratingPosLeft = rating.offsetLeft;
// console.log("rating left:", ratingPosLeft);
function ratingMoveHandler(e) {
    realTimeRating = Math.round(((e.clientX - ratingPosLeft)/rating.clientWidth)*10);
    console.log("data: mouse", e.clientX, "rating position left:", ratingPosLeft, "rating client width", rating.clientWidth);
    console.log("rating data:", realTimeRating);
    realTimeRatingStr = String(realTimeRating*10) + '%';

    // ratingData = ratingData / rating.width
    ratingTop.style.width = realTimeRatingStr;
    // ratingText.innerHTML = "My Rating: " + realTimeRating;
    ratingText.value = realTimeRating;
}
function ratingOutHandler() {
    ratingTop.style.width = latestRatingStr;
    realTimeRating = latestRating;
    ratingText.value = latestRating;
    // ratingText.innerHTML = "My Rating: " + realTimeRating;
}
function ratingClickHandler() {
    latestRating = realTimeRating;
    latestRatingStr = String(latestRating*10) + '%';
}

function absoluteLeft(element) {
    let left = 0;
    while (element) {
        console.log("I am ", element, ".my left is ", element.offsetLeft);
        left += element.offsetLeft;
        console.log("My style:", element.style);
        console.log("Which is why my parent is", element.offsetParent);
        element = element.offsetParent;
    }
    return left;
}

let modalLinks = document.querySelectorAll("#modal-link");
console.log(modalLinks.length);
modalLinks.forEach(function(curr, index) {
    curr.addEventListener("click", function(event) {
        let link = curr.getAttribute("href");
        console.log("opening modal "+link);
        let modal = document.querySelector(link);
        console.log(modal);
        if (modal != null) {
            modal.classList.add("active");
        } else {console.log("No such element")}
    })
});

let modalClose = document.querySelectorAll(".close");
console.log("Close buttons:"+modalClose.length);
modalClose.forEach(function(curr, index) {
    curr.addEventListener("click", function(event) {
        console.log("closing all modals");
        let modals = document.querySelectorAll(".modal");
        modals.forEach(function(curr, index) {
            curr.classList.remove("active");
        })
    })
});

