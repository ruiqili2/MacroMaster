console.log('hola')

let ratingText = document.querySelector('#rating-user');
let rating = document.querySelector('.star-ratings.mutable');
let ratingTop = document.querySelector('.star-ratings.top.mutable');
let latestRating = "0%";
let realTimeRating = "0%";
rating.addEventListener("mousemove", ratingMoveHandler);
rating.addEventListener("mouseout", ratingOutHandler);
rating.addEventListener("click", ratingMouseUpHandler);
let ratingPosLeft = rating.offsetLeft;
console.log("rating left:", ratingPosLeft);
function ratingMoveHandler(e) {
    //console.log("mouse location:", e.clientX, e.clientY);
    let ratingData = Math.round(((e.clientX - ratingPosLeft)/rating.clientWidth)*100);
    realTimeRating = String(ratingData) + '%';
    console.log("rating data:", realTimeRating);
    // ratingData = ratingData / rating.width
    ratingTop.style.width = realTimeRating;
    ratingText.innerHTML = "My Rating: " + realTimeRating;
}
function ratingOutHandler() {
    ratingTop.style.width = latestRating;
    realTimeRating = latestRating;
    ratingText.innerHTML = "My Rating: " + realTimeRating;
}
function ratingMouseUpHandler() {
    latestRating = realTimeRating;
}


