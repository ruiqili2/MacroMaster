console.log('hola')

let ratingText = document.querySelector('#rating-user');
let rating = document.querySelector('.star-ratings.mutable');
let ratingTop = document.querySelector('.star-ratings.top.mutable');
let latestRatingStr = "0%";
let latestRating = 0; 
let realTimeRatingStr = "0%";
let realTimeRating = 0;
rating.addEventListener("mousemove", ratingMoveHandler);
rating.addEventListener("mouseout", ratingOutHandler);
rating.addEventListener("click", ratingMouseUpHandler);
let ratingPosLeft = rating.offsetLeft;
console.log("rating left:", ratingPosLeft);
function ratingMoveHandler(e) {
    //console.log("mouse location:", e.clientX, e.clientY);
    realTimeRating = Math.round(((e.clientX - ratingPosLeft)/rating.clientWidth)*100);
    realTimeRatingStr = String(realTimeRating) + '%';
    console.log("rating data:", realTimeRating);
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
function ratingMouseUpHandler() {
    latestRating = realTimeRating;
    latestRatingStr = String(latestRating) + '%';
}


