window.scroll(0, 0);
window.scrollLeft = 0;
let currentLocation = 'start-slide';
$(function () {
  $("#right-arrow").click(nextSlide);
  $("#left-arrow").click(previousSlide);

  document.onkeydown = function (e) {
    switch (e.keyCode) {
      case 37:
        previousSlide();
        break;
      case 38:
        break;
      case 39:
        nextSlide();
        break;
      case 40:
        break;
    }
  };
});

function nextSlide() {
  $('.characters').css("background-image", "url(img/running-boy-r.gif)");
  $('html, body').animate({
    scrollLeft: $('#' + document.getElementById(currentLocation).nextElementSibling.id).offset().left
  }, {
    duration: 3000,
  });
  currentLocation = document.getElementById(currentLocation).nextElementSibling.id;
  setTimeout(function () {
    $('.characters').css("background-image", "url(img/boy-state01.png)");
  }, 3000);
  toggleArrows(currentLocation);
  return true;
}

function previousSlide() {
  $('.characters').css("background-image", "url(img/running-boy-l.gif)");
  $('html, body').animate({
    scrollLeft: $('#' + document.getElementById(currentLocation).previousElementSibling.id).offset().left
  }, {
    duration: 3000,
  });
  currentLocation = document.getElementById(currentLocation).previousElementSibling.id;
  setTimeout(function () {
    $('.characters').css("background-image", "url(img/boy-state01.png)");
  }, 3000);
  toggleArrows(currentLocation);
  return true;
}

function toggleArrows(currentLocation) {
  if (currentLocation === "calculate-slide") {
    $("#right-arrow").hide();
  } else {
    $("#right-arrow").show();
  }
  if (currentLocation === "start-slide") {
    $("#left-arrow").hide();
  } else {
    $("#left-arrow").show();
  }
}
