// Ina
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
      //document.getElementById("hours-text").innerHTML += "Torsdag: " + place.opening_hours.periods[3].open.time + " - " + place.opening_hours.periods[3].close.time + "<br/>" + "Fredag: " + place.opening_hours.periods[4].open.time + " - " + place.opening_hours.periods[4].close.time + "<br/>" + "Lördag: " + place.opening_hours.periods[5].open.time + " - " + place.opening_hours.periods[5].close.time + "<br/><br/>";
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
      //document.getElementById("hours-text").innerHTML += "Torsdag: " + place.opening_hours.periods[3].open.time + " - " + place.opening_hours.periods[3].close.time + "<br/>" + "Fredag: " + place.opening_hours.periods[4].open.time + " - " + place.opening_hours.periods[4].close.time + "<br/>" + "Lördag: " + place.opening_hours.periods[5].open.time + " - " + place.opening_hours.periods[5].close.time + "<br/>";
    }
  }


  const url = 'https://newsapi.org/v2/top-headlines?' +
    'country=se&' + 'language=sv&' +
    'apiKey=cd53af30e4fb4539b42e418cf5a0a384';
  fetch(url)
    .then((response) => {
      return response.json()
    }).then((data) => {
      document.getElementById("extern-head").innerHTML = data.articles[0].title;
      document.getElementById("extern-content").innerHTML = data.articles[0].description;
      let time = data.articles[0].publishedAt;
      time = time.split('');
      time[10] = ' ';
      time = time.join('');
      time = time.split('');
      time[19] = '';
      time = time.join('');
      document.getElementById("extern-time").innerHTML = time;
    }
  )
});

$(function () {

  // Nordin
  let runningIntervals = [];
  let ppl = [];
  let currentTheme = {};
  let animationContainer = $("#knw-bg-anim");
  let scrollingTipDiv = $(".scrolling-tip-div");
  let siteUrl = "http://localhost:5000/";

  let appConfig = getJson(siteUrl + 'admin/theme?config=appConfig');
  let themesJson = getJson(siteUrl + 'admin/theme?config=themesJson');
  let quotes = getJson(siteUrl + 'admin/theme?config=quotes');
  let tips = getJson(siteUrl + 'admin/theme?config=tips');

  setTheme();
  spawnCharacters();
  setInterval(spawnCharacters, 4000);
  setInterval(createPplsJson, 1000);
  setInterval(tipsFadeInFadeOut, 10000, scrollingTipDiv, 10000, tips);
  drawMonthlyHeroes();
  setInterval(drawMonthlyHeroes, 1000 * 60 * 60);
  settings();

  function setTheme() {
    clearAllIntervals();
    animationContainer.empty();
    if (appConfig.themeOverride.active) {
      currentTheme.themeCategory = appConfig.themeOverride.themeCategory;
      currentTheme.themeName = appConfig.themeOverride.themeName;
    } else {
      let currentSeason = "";
      let year = new Date().getFullYear();
      let seasons = {
        "autumn": new Date(year, 12, 20),
        "summer": new Date(year, 9, 20),
        "spring": new Date(year, 6, 20),
        "winter": new Date(year, 3, 20)
      };

      let currentDate = new Date();
      for (let key in seasons) {
        if (currentDate < seasons[key])
          currentSeason = key;
      }
      currentTheme.themeCategory = currentSeason;
      currentTheme.themeName = Object.keys(themesJson[currentSeason])[Math.floor(Object.keys(themesJson[currentSeason]).length * Math.random())];
    }
    initThemeAnimation();
  }

  function initThemeAnimation() {
    //Todo go through current theme layers and construct the animation
    $.each(themesJson[currentTheme.themeCategory][currentTheme.themeName].layers, function (index, layer) {
      let tempLayerDiv = $("<div id='anim-layer-" + index + "'>");
      let themeFolder = 'img/themes/' + currentTheme.themeCategory + '/' + currentTheme.themeName + '/';


      let signHtml = $(`<div class="display-sign pt-2"
        style="position: absolute; background: url('./img/digital-display.png') no-repeat; width: 192px; height: 400px;">
          <div id="display-buzz" class="fs-5">

          <div class="display-text text-danger text-center p-0 m-0">Nuvarande placeringar</div>
        <div class="display-text text-danger text-left px-3 pt-2 m-0">
          #01: Nordin S <br>
          #02: Fredrik K <br>
          #03: Ivan S <br>
          #04: Ouri Q <br>
          #05: Naru Q <br>
          ........... <br>
        </div>
      </div>
      </div>`);

      tempLayerDiv.addClass('container-fluid bg-scroll');
      tempLayerDiv.attr('id', 'anim-layer-' + index);
      if (layer.layerType === "bg-layer") {
        tempLayerDiv.css({
          'background': 'url(' + themeFolder + layer.bgImg + ')', 'background-size': '100%'
        });
        if (layer.options.speed > 0) {
          slideAnimateMaybeSpawn(tempLayerDiv, layer.options.speed, {'background-position-x': '0vw'}, {'background-position-x': '-=100vw'}, 0);
          var tempThisInterval = setInterval(slideAnimateMaybeSpawn, layer.options.speed, tempLayerDiv, layer.options.speed, {'background-position-x': '0vw'}, {'background-position-x': '-=100vw'}, 0);
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

        spawnContainerDivA.addClass('row spawn-slide position-absolute bottom-0');
        spawnContainerDivB.addClass('row spawn-slide position-absolute bottom-0');
        spawnContainerDivA.attr('id', 'spawn-layer-' + index + currentTheme.themeName + '-a');
        spawnContainerDivB.attr('id', 'spawn-layer-' + index + currentTheme.themeName + '-b');
        $(spawnContainerDivA).appendTo(tempLayerDiv);
        $(spawnContainerDivB).appendTo(tempLayerDiv);

        if (layer.layerType === "spawn-layer") {
          getImgsFromFolder(themeFolder + 'props/' + layer.spawnImgs + '/').then(props => {
            slideAnimateMaybeSpawn(spawnContainerDivA, layer.options.speed * 1, {'left': '100vw'}, {'left': '-100vw'}, 0, layer.options, props);
            slideAnimateMaybeSpawn(spawnContainerDivB, layer.options.speed * 1, {'left': '100vw'}, {'left': '-100vw'}, layer.options.speed * 1, layer.options, props);
            var slideOneInterval = setInterval(slideAnimateMaybeSpawn, layer.options.speed * 2, spawnContainerDivA, layer.options.speed * 2, {'left': '100vw'}, {'left': '-100vw'}, 0, layer.options, props);
            runningIntervals.push(slideOneInterval);
            setTimeout(() => {
              var slideTwoInterval = setInterval(slideAnimateMaybeSpawn, layer.options.speed * 2, spawnContainerDivB, layer.options.speed * 2, {'left': '100vw'}, {'left': '-100vw'}, 0, layer.options, props);
              runningIntervals.push(slideTwoInterval);
            }, layer.options.speed);
          });
        } else {
          $(signHtml).appendTo(spawnContainerDivA);
          $(signHtml).appendTo(spawnContainerDivB);
          slideAnimateMaybeSpawn(spawnContainerDivA, layer.options.speed * 1, {'left': '100vw'}, {'left': '-100vw'}, 0, layer.options);
          slideAnimateMaybeSpawn(spawnContainerDivB, layer.options.speed * 1, {'left': '100vw'}, {'left': '-100vw'}, layer.options.speed * 1, layer.options);
          var slideOneInterval = setInterval(slideAnimateMaybeSpawn, layer.options.speed * 2, spawnContainerDivA, layer.options.speed * 2, {'left': '100vw'}, {'left': '-100vw'}, 0, layer.options);
          runningIntervals.push(slideOneInterval);
          setTimeout(() => {
            var slideTwoInterval = setInterval(slideAnimateMaybeSpawn, layer.options.speed * 2, spawnContainerDivB, layer.options.speed * 2, {'left': '100vw'}, {'left': '-100vw'}, 0, layer.options);
            runningIntervals.push(slideTwoInterval);
          }, layer.options.speed);
        }
      }
      animationContainer.append(tempLayerDiv);
    });
  }

  function slideAnimateMaybeSpawn(element, speed, propertyStart, propertyEnd, delayTime, options, props = []) {
    $(element).delay(delayTime).animate(propertyEnd, speed, 'linear', () => {
      // go back to original state
      $(element).css(propertyStart);
      // spawn items
      if (props.length) {
        spawnProps(element, props, options);
      }
    });
  }

  function drawMonthlyHeroes() {
    let lastMonthTop3 = getJson(siteUrl + "player/getTop");
    let idleAvatarUrl = '../../backend/API/static/characters/idle_avatar/emp_';
    $.each(lastMonthTop3, (index, player) => {
      if (index === '1') {
        $("#avatar-gold").css({'background': 'url("' + idleAvatarUrl + player[1] + '.gif")'});
        $("#nameplate-gold").html(player[0]);
      }
      if (index === '2') {
        $("#avatar-silver").css({'background': 'url("' + idleAvatarUrl + player[1] + '.gif")'});
        $("#nameplate-silver").html(player[0]);
      }
      if (index === '3') {
        $("#avatar-bronze").css({'background': 'url("' + idleAvatarUrl + player[1] + '.gif")'});
        $("#nameplate-bronze").html(player[0]);
      }
    });
  }

  function createPplsJson() {
    $.ajax({
      url: siteUrl + 'player/getRecent',
      type: "GET",
      dataType: "json",
      success: function (data) {
        if (data === undefined) {
          return;
        }
        // spawnCharacters();
        let newPpl = data.filter(o1 => !ppl.some(o2 => o1.emp_id === o2.emp_id));
        if (!isNaN(newPpl.length) && newPpl.length > 0) {
          ppl = newPpl;
          let peopleDiv = $('#people-box');
          if ((peopleDiv.children().length + ppl.length) > 4) {
            for (let i = 0; i < newPpl.length; i++) {
              $('#people-box > div:last').remove();
            }
          }
          $.each(ppl, function (index, obj) {
            let cardStyleFirst = 'col first-card';
            let cardStyleRest = 'col rest-cards';
            let newElement = document.createElement('div');


            $(newElement).attr("class", cardStyleFirst);
            if (obj.emp_id === 0) {
              newElement.innerHTML = `
            <div class="card user-card bg-white" data-label="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Gäst &nbsp;&nbsp;&nbsp;">
                <div class="card-block position-relative">
                    <div class="user-image">
                        <img src="../../backend/API/static/characters/idle_avatar/guest_0.gif" class="img-radius" alt="User-Profile-Image">
                    </div>
                    <h4 class="f-w-600 m-b-10">Välkommen till Knowit</h4>
                    <p class="m-t-10 fs-4 text-muted text-start">Känner inte igen dig, om du är en gäst var vänlig och presentera dig i receptionen.</p>
                </div>
            </div>`;
            } else {
              newElement.innerHTML = `
            <div class="card user-card bg-white" data-label="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Lvl: ${obj.level}, rank: ${obj.ranking} &nbsp;&nbsp;&nbsp;">
                <div class="card-block position-relative">
                    <div class="user-image">
                        <img src="../../backend/API/static/characters/idle_avatar/emp_${obj.emp_id}.gif" class="img-radius" alt="User-Profile-Image">
                    </div>
                    <h4 class="f-w-600 m-b-10">${obj.displayName}</h4>
                    <p class="m-t-10 fs-4 text-muted text-start">${obj.greeting}</p>
                    <div class="start-0 w-100">
                        <p class="m-0 p-0 text-start fw-bold fs-6 text-uppercase .text-black">next level xp:</p>
                      <div class="progress position-relative bg-clay" style="height: 30px;">
                        <div class="m-0 py-auto my-auto pe-2 position-absolute text-end w-100 fw-bolder fs-5 text-white text-stroke-black">${obj.xpLevel} / ${obj.xpNextLevel}</div>
                        <div class="progress-bar bg-forest" role="progressbar" style="width: ${(obj.xpLevel / obj.xpNextLevel) * 100}%;" aria-valuenow="" aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                    <p class="m-t-25 fs-4 text-muted text-start">${quotes.quotes[Math.floor((Math.random() - 0.001) * quotes.quotes.length)].quote}</p>
                    </div>
                    <div class="knw-moodchart position-absolute bottom-0 start-50 translate-middle-x hide">
                        <canvas id="knw-moodchart-${obj.emp_id}"></canvas>
                    </div>
                </div>
            </div>`;
            }
            $(newElement).css({'margin-left': '-300px', 'opacity': '0.95'});
            $('#people-box > div').attr("class", cardStyleRest);
            peopleDiv.prepend(newElement);

            $(newElement).animate({
              marginLeft: "0px",
            }, 500);
          });
          $.each(peopleDiv.children(), function (index, child) {
            $(child).delay(12000 / (index + 1)).fadeOut(1000);
          });
        }
      }
    });
  }

  // clear all intervals for this theme
  function clearAllIntervals() {
    $.each(runningIntervals, (index, interval) => {
      clearInterval(interval);
    });
  }


  // handling settings menu
  function settings() {
    // populate override select field
    $.each(themesJson, (catIndex, themeCat) => {
      $.each(themeCat, (themeIndex, theme) => {
        $("#override-theme-select").append("<option value='{\"" + theme.category + "\":\"" + Object.keys(themeCat)[0] + "\"}'>" + Object.keys(themeCat)[0] + "</option>");
      })
    })
    // toggle seasonal theme or override theme
    $('input[name="set-theme"]').on('click change', function () {
      if ($(this).val() === "override") {
        $("#override-theme-select").prop('disabled', false);
      } else if ($(this).val() === "seasonal") {
        $("#override-theme-select").prop('disabled', true);
        appConfig.themeOverride.active = false;
        setTheme();
      }
    });
    $('select[id="override-theme-select"]').on('change', function () {
      if ($(this).val() !== "Override theme") {
        let tempThemeJson = $.parseJSON($(this).val().replace(/\\/g, ""));
        appConfig.themeOverride.active = true;
        appConfig.themeOverride.themeCategory = Object.keys(tempThemeJson)[0];
        appConfig.themeOverride.themeName = tempThemeJson[Object.keys(tempThemeJson)[0]];
        setTheme();
        // TODO save theme settings to db
      }
    });
  }

  // api call to get json from backend
  function getJson(url) {
    let json = null;
    $.ajax({
      'async': false,
      'global': false,
      'url': url,
      'dataType': "json",
      'success': function (data) {
        if (data !== undefined)
          json = data;
      }
    });
    return json;
  }

  // api call to save json to backend
  function saveJson(theUrl, myText) {
    $.ajax({
      type: 'POST',
      url: theUrl,
      data: JSON.stringify(myText),
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function (result) {
        console.log('success save json ' + result);
      }
    });
  }

  function tipsFadeInFadeOut(element, speed, tips) {
    element.html(tips[Math.floor(Math.random() * tips.length)]);
    element.hide().fadeIn(speed * 0.1).delay(speed * 0.7).fadeOut(speed * 0.1).delay(speed * 0.1);
  }

  function spawnProps(where, props, options) {
    // props are from current theme folder
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
        'transform': 'rotate(' + deg + 'deg)',
        'z-index': options.zIndex
      });
    }
  }

  function spawnCharacters() {
    let charactersFolder = "../../backend/API/static/characters/running_avatar/";
    let randTop = 0;
    $.ajax({
      url: siteUrl + 'player/getMonthlyXP',
      type: "GET",
      dataType: "json",
      success: function (data) {
        let maxValue = 0;
        let empCount = Object.keys(data).length;
        let previousEmpId = 0;

        $.each(data, (i, el) => {
          if (el > maxValue)
            maxValue = el;
        });

        $.each(data, function (index, person) {
          let tempImg = $("#emp-char-" + index);
          // let smokeSpawn = $("#smokeSpawn-" + index);
          if (!person) {
            tempImg.remove();
            $("#smokeSpawn-" + index).remove();
            // randTop -= (100 / empCount) * 0.70;
            --empCount;
            return true;
          }
          if (randTop === 0) {
            randTop = 1;
          } else {
            randTop += (100 / empCount) * 0.70;
          }
          let leftPos = person / maxValue * 70; // 70% the track is the front of the track

          // create running char if not created
          if (!tempImg.length) {
            tempImg = "<div id='emp-char-" +
              index + "' style='z-index:10000; " +
              "position: absolute; " +
              "left: 1%; top:" + randTop +
              "%;'><img class='spawnChars' alt='emp-char-avatar' src='" +
              charactersFolder + "emp_" +
              index + ".gif' width='150px'><img alt='spawnSmoke' class='smokeSpawn' id='spawnSmoke-" + index +
              "' src='./img/invisible-smoke.png' style='position:absolute; left: -40px; top: -80px;'></div>";
          }
          if (!$("#track-area").children().length) {
            $("#track-area").append(tempImg);
            $("#emp-char-" + index + " .spawnChars").delay(600).fadeIn(400);
            $("#spawnSmoke-" + index).attr("src", "./img/spawnSmoke.gif");
          } else {
            if ($("#emp-char-" + index).length) {
              $("#emp-char-" + index).insertAfter("#emp-char-" + previousEmpId);
              $("#spawnSmoke-" + index).attr("src", "./img/invisible-smoke.png");
            } else {
              $(tempImg).insertAfter("#emp-char-" + previousEmpId);
              $("#emp-char-" + index + " .spawnChars").delay(600).fadeIn(400);
              $("#spawnSmoke-" + index).attr("src", "./img/spawnSmoke.gif");
            }
          }
          previousEmpId = index;

          if ($("#emp-char-" + index).length) {
            $("#emp-char-" + index).stop().animate({left: leftPos + "%", top: randTop + "%"}, {
              duration: 2000,
              queue: false
            });
          }
          return true;
        });
      }
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

});
