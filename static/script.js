$(document).ready(function() {
  var carousel = $(".carousel");
  var storeWidth = $(".store").outerWidth(true);
  var carouselPosition = 0;

  $("#carousel-next").click(function() {
    if (carouselPosition > -((carousel.children().length - 1) * storeWidth)) {
      carouselPosition -= storeWidth;
      carousel.css("transform", "translateX(" + carouselPosition + "px)");
    }
  });

  $("#carousel-prev").click(function() {
    if (carouselPosition < 0) {
      carouselPosition += storeWidth;
      carousel.css("transform", "translateX(" + carouselPosition + "px)");
    }
  });
});
