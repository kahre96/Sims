document.addEventListener('DOMContentLoaded', () => {
  let date = new Date();
  const months = ["januari", "februari", "mars", "april", "maj", "juni", "juli", "augusti", "september", "oktober", "november", "december"];
  let monthText = months[date.getMonth()];
  let day = date.getDate();
  const days = ["Söndag", "Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag", "Lördag"];
  let weekday = days[date.getDay()];

  document.getElementById("date").innerHTML = weekday + " " + day + " " + monthText;

  let BirstaID = "ChIJ_zc5o4JgZEYR9MoQtnVmOKs";
  let GatanID = "ChIJRzq-RFxnZEYRcYtGa2wwq4Y";

  const request = {
    placeId: BirstaID, fields: ['name', 'opening_hours', 'utc_offset_minutes']
  };
  const service = new google.maps.places.PlacesService(document.createElement('div'));
  service.getDetails(request, callback);

  const request2 = {
    placeId: GatanID, fields: ['name', 'opening_hours', 'utc_offset_minutes']
  };
  const service2 = new google.maps.places.PlacesService(document.createElement('div'));
  service.getDetails(request2, callback2);

  function callback(place, status) {
    if (status !== google.maps.places.PlacesServiceStatus.OK) {
      document.getElementById("hours-text").innerHTML = "Nu var det någonting som gick fel. Skyll på Google!";
    }
    if (place.opening_hours && place.utc_offset_minutes) {
      const isOpenNow = place.opening_hours.isOpen();
      if (isOpenNow) {
        document.getElementById("hours-text").innerHTML = "Systembolaget i Birsta har öppet just nu!\n";
      } else {
        document.getElementById("hours-text").innerHTML += "Systembolaget i Birsta har stängt just nu!\n";
      }
      document.getElementById("hours-text").innerHTML += "Torsdag: " + place.opening_hours.periods[3].open.time + " - " + place.opening_hours.periods[3].close.time + "<br/>" + "Fredag: " + place.opening_hours.periods[4].open.time + " - " + place.opening_hours.periods[4].close.time + "<br/>" + "Lördag: " + place.opening_hours.periods[5].open.time + " - " + place.opening_hours.periods[5].close.time + "<br/><br/>";
    }
  }

  function callback2(place, status) {
    if (status !== google.maps.places.PlacesServiceStatus.OK) {
      document.getElementById("hours-text").innerHTML += "Nu var det någonting som gick fel. Skyll på Google!";
    }
    if (place.opening_hours && place.utc_offset_minutes) {
      const isOpenNow = place.opening_hours.isOpen();
      if (isOpenNow) {
        document.getElementById("hours-text").innerHTML += "Systembolaget på Sjögatan har öppet just nu!\n";
      } else {
        document.getElementById("hours-text").innerHTML += "Systembolaget på Sjögatan har stängt just nu!\n";
      }
      document.getElementById("hours-text").innerHTML += "Torsdag: " + place.opening_hours.periods[3].open.time + " - " + place.opening_hours.periods[3].close.time + "<br/>" + "Fredag: " + place.opening_hours.periods[4].open.time + " - " + place.opening_hours.periods[4].close.time + "<br/>" + "Lördag: " + place.opening_hours.periods[5].open.time + " - " + place.opening_hours.periods[5].close.time + "<br/>";
    }
  }
});


$(function (keyframes, options) {
  let runningIntervals = [];
  let ppl = [];
  let currentTheme = {};

  var themeConfig = (function () {
    var json = null;
    $.ajax({
        'async': false,
        'global': false,
        'url': 'img/themes/themes-config.json',
        'dataType': "json",
        'success': function (data) {
            json = data;
        }
    });
    return json;
})() ;
  var quotes = (function () {
    var json = null;
    $.ajax({
        'async': false,
        'global': false,
        'url': 'resources/quotes.json',
        'dataType': "json",
        'success': function (data) {
            json = data;
        }
    });
    return json;
})() ;
    console.log(themeConfig.override.active);
  // $.getJSON('img/themes/themes-config.json', function (jsonFromFile) {
  //   themeConfig = jsonFromFile;
  // });
  // $.getJSON('resources/quotes.json', function (jsonFromFile) {
  //   quotes = jsonFromFile;
  // });
  setTheme();
  initBgAnimation();
  setInterval(createPplsJson, 1000);
  spawnCharacters();

  function setTheme() {
    // pick random theme from season based on date if override is not set.
    if (themeConfig.override.active) {
      currentTheme.themeCategory = themeConfig.override.themeCategory;
      currentTheme.themeName = themeConfig.override.themeName;
    } else {
      //Todo grab random theme from season folder depending on date and time
      // currentTheme = themeConfig.themes["summer"]["city01"];
      currentTheme.themeCategory = themeConfig.override.themeCategory;
      currentTheme.themeName = themeConfig.override.themeName;
    }
  }

  function initBgAnimation() {
    //Todo go through current theme layers and construct the animation
    $.each(themeConfig.themes[currentTheme.themeCategory][currentTheme.themeName].layers, function (index, layer) {
      let tempLayerDiv = $("<div>");
      let themeFolder = 'img/themes/' + currentTheme.themeCategory + '/' + currentTheme.themeName + '/';
      tempLayerDiv.addClass('container-fluid bg-scroll');
      tempLayerDiv.attr('id', 'anim-layer-' + index);
      if (layer.layerType === "bg-layer") {
        tempLayerDiv.css({
          'background': 'url(' + themeFolder + layer.bgImg + ')', 'background-size': '100%'
        });
        if (layer.options.speed > 0) {
          loopAnimateBg(tempLayerDiv, layer.options.speed, {'background-position-x': '0vw'}, {'background-position-x': '-=100vw'}, 0);
          let tempThisInterval = setInterval(loopAnimateBg, layer.options.speed, tempLayerDiv, layer.options.speed, {'background-position-x': '0vw'}, {'background-position-x': '-=100vw'}, 0);
          runningIntervals.push(tempThisInterval);
        }
      } else {
        tempLayerDiv.css({
          'top': layer.options.spawnStartY + 'px', 'height': layer.options.randPosY + 'px',
        });
        let spawnContainerDivA = $("<div>");
        let spawnContainerDivB = $("<div>");
        // two empty divs to avoid spawn popping in beginning
        $('<div class="col-2"></div>').appendTo(spawnContainerDivA);
        $('<div class="col-2"></div>').appendTo(spawnContainerDivB);
        for (let i = 0; i < layer.options.spawnsPerLoop; i++) {
          $('<div class="col prop spawn' + i + '"></div>').appendTo(spawnContainerDivA);
          $('<div class="col prop spawn' + i + '"></div>').appendTo(spawnContainerDivB);
        }

        // Todo set slide bottom-0 from json
        spawnContainerDivA.addClass('row spawn-slide position-absolute bottom-0');
        spawnContainerDivB.addClass('row spawn-slide position-absolute bottom-0');
        spawnContainerDivA.attr('id', 'spawn-layer-' + index + '-a');
        spawnContainerDivB.attr('id', 'spawn-layer-' + index + '-b');
        $(spawnContainerDivA).appendTo(tempLayerDiv);
        $(spawnContainerDivB).appendTo(tempLayerDiv);


        getImgsFromFolder(themeFolder + 'props/' + layer.spawnImgs + '/').then(props => {
          loopAnimateBg(spawnContainerDivA, layer.options.speed * 1, {'left': '100vw'}, {'left': '-100vw'}, 0, props, layer.options);
          loopAnimateBg(spawnContainerDivB, layer.options.speed * 1, {'left': '100vw'}, {'left': '-100vw'}, layer.options.speed * 1, props, layer.options);
          var slideOneInterval = setInterval(loopAnimateBg, layer.options.speed * 2, spawnContainerDivA, layer.options.speed * 2, {'left': '100vw'}, {'left': '-100vw'}, 0, props, layer.options);
          runningIntervals.push(slideOneInterval);
          setTimeout(() => {
            var slideTwoInterval = setInterval(loopAnimateBg, layer.options.speed * 2, spawnContainerDivB, layer.options.speed * 2, {'left': '100vw'}, {'left': '-100vw'}, 0, props, layer.options);
            runningIntervals.push(slideTwoInterval);
          }, layer.options.speed);
        });
      }
      $("#knw-bg-anim").append(tempLayerDiv);
    });
  }

  function loopAnimateBg(element, speed, propertyStart, propertyEnd, delayTime, props = [], options) {
    $(element).delay(delayTime).animate(propertyEnd, speed, 'linear', () => {
      // go back to original state
      $(element).css(propertyStart);
      // spawn items
      if (props.length) {
        spawnProps(element, props, options);
      }
    });
  }

  function createPplsJson() {
    $.getJSON('http://localhost:5000/player/getRecent', function (data) {
      let newPpl = data.filter(o1 => !ppl.some(o2 => o1.emp_id === o2.emp_id));
      console.log(JSON.stringify(newPpl));
      // $.each(data, function (index, person) {
      //   // alert(JSON.stringify(person));
      // });
      if (!isNaN(newPpl.length) && newPpl.length > 0) {
        ppl = newPpl;
        // ppl = [...ppl, ...newPpl];
        // ppl = ppl.slice(Math.max(ppl.length - 4, 0));
        if (($('#people-box').children().length + ppl.length) > 4) {
          //   //   let tempNum = ppl.length - 4;
          //   $('#people-box').empty();
          for (let i = 0; i < newPpl.length; i++) {
            $('#people-box > div:last').remove();
          }
        }
        // $('#people-box').splice('-' + newPpl.length).remove();
      } else {
        return;
      }


      //Todo iterate and render each person once there is new persons in the card, make into a function
      $.each(ppl, function (index, obj) {
        let cardStyleFirst = 'col first-card';
        let cardStyleRest = 'col rest-cards';
        let newElement = document.createElement('div');
        $(newElement).attr("class", cardStyleFirst);
        newElement.innerHTML = `
            <div class="card user-card bg-white" data-label="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Lvl: ${obj.level}, rank: ${obj.ranking} &nbsp;&nbsp;&nbsp;">
                <div class="card-block position-relative">
                    <div class="user-image">
                        <img src="img/characters/avatars/${obj.emp_id}.png" class="img-radius" alt="User-Profile-Image">
                    </div>
                    <h4 class="f-w-600 m-b-10">${obj.displayName}</h4>
                    <p class="m-t-10 fs-4 text-muted text-start">${obj.greeting}</p>
                    <div class="start-0 w-100">
                        <p class="m-0 p-0 text-start fw-bold fs-6 text-uppercase .text-black">next level xp:</p>
                      <div class="progress position-relative bg-clay" style="height: 30px;">
                        <div class="m-0 py-auto my-auto pe-2 position-absolute text-end w-100 fw-bolder fs-5 text-white text-stroke-black">${obj.xpMonth} / ${obj.xpTotal}</div>
                        <div class="progress-bar bg-forest" role="progressbar" style="width: ${(obj.xpMonth / obj.xpTotal) * 100}%;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                    <p class="m-t-25 fs-4 text-muted text-start">${quotes.quotes[Math.floor((Math.random() - 0.001) * quotes.quotes.length)].quote}</p>
                    </div>
                    <div class="knw-moodchart position-absolute bottom-0 start-50 translate-middle-x hide">
                        <canvas id="knw-moodchart-${obj.emp_id}"></canvas>
                    </div>
                </div>
            </div>`;
        $(newElement).css({'margin-left': '-300px', 'opacity': '0.95'});
        $('#people-box > div').attr("class", cardStyleRest);
        $('#people-box').prepend(newElement);

        // let grumpy = Math.floor(Math.random() * 21);
        // let happy = Math.floor(Math.random() * 21);
        // let sad = Math.floor(Math.random() * 21);
        // let ambition = Math.floor(Math.random() * 21);
        // let curious = Math.floor(Math.random() * 21);
        // createPersonChart('knw-moodchart-' + obj.emp_id, grumpy, happy, sad, ambition, curious);

        $(newElement).animate({
          marginLeft: "0px",
        }, 500);
      });
      $.each($('#people-box').children(), function (index, child) {
        $(child).delay(12000 / (index + 1)).fadeOut(1000);
      });

    }).fail(function (jqXHR, textStatus, errorThrown) {
      // console.log('getJSON request failed! ' + textStatus);
    }).always(function () {
      // console.log("always: complete");
    });

    function createPersonChart(where, grumpy, happy, sad, ambition, curious) {
      const labels = ['Grumpiness', 'Happiness', 'Curiousity', 'Ambition', 'Sadness',];

      const data = {
        labels: labels, datasets: [{
          label: 'My First dataset',
          data: [grumpy, happy, sad, ambition, curious],
          fill: true,
          backgroundColor: 'rgba(255, 0, 255, 0.2)',
          borderColor: 'rgb(255, 0, 255)',
          pointBackgroundColor: 'rgb(255, 0, 255)',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgb(255, 0, 255)'
        }]
      };

      const config = {
        type: 'radar', data: data, options: {
          elements: {
            line: {
              borderWidth: 3
            }
          }, plugins: {
            legend: {
              display: false,
            }
          }, scales: {
            r: {
              pointLabels: {
                font: {
                  size: 16
                }
              }
            }
          }
        }
      };
      Chart.defaults.font.size = 14;
      const myChart = new Chart(document.getElementById(where), config);
    }
  }

  // clear all intervalls for this theme
  function clearAllIntervals() {
    $.each(runningIntervals, (index, interval) => {
      clearInterval(interval);
    });
  }

});


function spawnProps(where, props, options) {
  for (let i = 0; i < $('#' + where.attr('id') + " .prop").length; i++) {
    let currentSpawnImg;
    // create an img tag if one douse not exist already
    if (!(currentSpawnImg = $('#' + where.attr('id') + " .spawn" + i + ' img')).length) {
      currentSpawnImg = $('<img alt="spawn-item" src="" />');
      $('#' + where.attr('id') + " .spawn" + i).append(currentSpawnImg);
    }
    let tempImgUrl = props[Math.floor(Math.random() * props.length)];
    let posLeft = Math.floor(Math.random() * options.randPosX);
    posLeft *= Math.round(Math.random()) ? 1 : -1;

    let randMargin = Math.floor(Math.random() * options.randPosY * 0.85);
    let topMargin = options.topOrBot === 'top' ? randMargin + 'px' : 'auto';
    let btmMargin = options.topOrBot === 'bottom' ? randMargin + 'px' : 'auto';

    let hueRand = options.randHue ? Math.floor(Math.random() * (options.randHue / 100) * 360) : 0;
    let satRand = options.randSat ? Math.floor(Math.random() * options.randSat) + 100 - (options.randSat / 2) : 100;
    let deg = Math.floor(Math.random() * options.randRotation);
    deg *= Math.round(Math.random()) ? 1 : -1;
    currentSpawnImg.attr({'src': tempImgUrl});
    currentSpawnImg.addClass(options.topOrBot + '-0 end-50');
    currentSpawnImg.css({
      'position': 'absolute',
      'margin-left': posLeft + '%',
      'margin-top': topMargin,
      'margin-bottom': btmMargin,
      'filter': 'hue-rotate(' + hueRand + 'deg) saturate(' + satRand + '%)',
      'transform': 'rotate(' + deg + 'deg)'
    });
  }
}

function spawnCharacters() {
  let charactersFolder = "img/characters/";
  let randTop = 0;
  let amount = 10;
  getImgsFromFolder(charactersFolder).then(characters => {
    for (let i = 0; i < amount; i++) {
      let tempImgUrl = characters[Math.floor(Math.random() * characters.length)];
      randTop += (Math.random() * 100) / amount;
      let randLeft = Math.floor(Math.random() * 70);
      let hueRand = Math.floor(Math.random() * 360);
      let tempImg = "<img src='" + tempImgUrl + "' style='width: " + 150 + "px; z-index:10000; " + "position: absolute; " + "left:" + randLeft + "%; top:" + randTop + "%; filter:hue-rotate(" + hueRand + "deg)'>";
      $("#track-area").append(tempImg);
    }
  }).catch(error => {
    console.log(error)
  });
}


function getImgsFromFolder(folderUrl) {
  return new Promise((resolve, reject) => {
    let imgs = [];
    $.ajax({
      url: folderUrl, success: (data) => {
        $(data).find("a").attr("href", (i, val) => {
          if (val.match(/\.(png|gif)$/)) {
            imgs.push(folderUrl + val);
          }
          resolve(imgs);
        });
      }, error: (error) => {
        reject(error);
      }
    });
  });
}

// handeling settings menu
$(document).ready(function () {
  $('input[name="set-theme"]').on('click change', function () {
    if ($(this).val() === "override") {
      $("#override-theme-select").prop('disabled', false);
    } else if ($(this).val() === "seasonal") {
      $("#override-theme-select").prop('disabled', true);
    }
  });
  $('select[id="override-theme-select"]').on('change', function () {
    if ($(this).val() !== "Override theme") {
      // $("#override-theme-select").prop('disabled', false);
      alert($(this).val());
    }
  });

  var $tableBody = $('#sortable');
  $(document).on('click', '.add-bg-layer', function () {
    var htmlString = $('#rowTemplate').html();
    $tableBody.append(htmlString);
    return false;
  });

  $tableBody.on('click', '.del-layer', function (e) {
    var $el = $(e.currentTarget);
    var $row = $el.closest('li');
    $row.remove();
    return false;
  });
  $tableBody.sortable({
    placeholder: 'drop-shadow'
  });
});
