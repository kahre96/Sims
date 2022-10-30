/**
 * @AUTHOR: Nordin Suleimani <nordin.suleimani@email.com>
 * @AUTHOR2: Ina
 * @DATE: 9/14/2022
 *
 * @Description. Frontend main JS file, contains themes, animations for themes, employee cards, track characters
 * api calls to google and Knowit endpoints, api to backend to retrieve project data.
 */

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
  // service.getDetails(request, callback);

  const request2 = {
    placeId: GatanID, fields: ['name', 'opening_hours', 'utc_offset_minutes']
  };
  const service2 = new google.maps.places.PlacesService(document.createElement('div'));
  // service.getDetails(request2, callback2);

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
  let themeSelectOptions = $("#override-theme-select");

  let siteUrl = "http://localhost:5000/";

  let appConfig = getJson(siteUrl + 'admin/theme?config=appConfig');
  let themesJson = getJson(siteUrl + 'admin/theme?config=themesJson');
  let stMnts = getJson(siteUrl + 'admin/theme?config=statements');
  let tips = getJson(siteUrl + 'admin/theme?config=tips');

  setTheme();
  spawnCharacters();
  setInterval(spawnCharacters, 2500);
  setInterval(createPplsJson, 1000);
  setInterval(tipsFadeInFadeOut, 10000, scrollingTipDiv, 10000, tips);
  drawMonthlyHeroes();
  setInterval(drawMonthlyHeroes, 1000 * 60 * 60);

  goodToKnow();
  setInterval(goodToKnow, 1000 * 60);
  settings();

  // Event listener on keyup to toggle admin page or reload application
  document.addEventListener('keyup', (event) => {
    if ((event.altKey && event.shiftKey && (event.key === 'r' || event.key === 'R'))) {
      location.reload();
    }
    if ((event.altKey && event.shiftKey && (event.key === 'a' || event.key === 'A'))) {
      $("#adminModal").modal('toggle');
    }
  }, false);

  function setTheme() {
    // clear all theme animations and empty out animation container
    clearAllIntervals();
    animationContainer.empty();

    if (appConfig.themeOverride.active) {
      currentTheme.themeCategory = appConfig.themeOverride.themeCategory;
      currentTheme.themeName = appConfig.themeOverride.themeName;
    } else { // set theme based on date of year(season)
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
    //Goes through current theme layers and construct the animation
    $.each(themesJson[currentTheme.themeCategory][currentTheme.themeName].layers, function (index, layer) {
      let tempLayerDiv = $("<div id='anim-layer-" + index + "'>");
      let themeFolder = 'img/themes/' + currentTheme.themeCategory + '/' + currentTheme.themeName + '/';
      let signHtml = $(`<div class="col prop spawn0"><div class="display-sign pt-2 bottom-0">
          <div id="display-buzz" class="fs-4 lh-sm">
          <div class="display-text text-danger text-center p-0 m-0 fs-5">Nuvarande placeringar</div>
        <div id="display-placements" class="display-text text-danger text-left px-2 pt-2 m-0"></div>
      </div>
      </div></div>`);

      tempLayerDiv.addClass('container-fluid bg-scroll');
      tempLayerDiv.attr('id', 'anim-layer-' + index);
      if (layer.layerType === "bg-layer") {
        tempLayerDiv.css({
          'background': 'url(' + themeFolder + layer.bgImg + ')', 'background-size': '100%'
        });
        if (layer.options.speed > 0) {
          slideAnimateMaybeSpawn(tempLayerDiv, layer.options.speed, {'background-position-x': '0vw'}, {'background-position-x': '-=100vw'}, 0);
          const tempThisInterval = setInterval(slideAnimateMaybeSpawn, layer.options.speed, tempLayerDiv, layer.options.speed, {'background-position-x': '0vw'}, {'background-position-x': '-=100vw'}, 0);
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
            const slideOneInterval = setInterval(slideAnimateMaybeSpawn, layer.options.speed, spawnContainerDivA, layer.options.speed, {'left': '100vw'}, {'left': '-100vw'}, 0, layer.options, props);
            runningIntervals.push(slideOneInterval);
            setTimeout(() => {
              const slideTwoInterval = setInterval(slideAnimateMaybeSpawn, layer.options.speed, spawnContainerDivB, layer.options.speed, {'left': '100vw'}, {'left': '-100vw'}, 0, layer.options, props);
              runningIntervals.push(slideTwoInterval);
            }, layer.options.speed / 2);
          });
        } else {
          $(signHtml).appendTo(spawnContainerDivA);
          $(signHtml).appendTo(spawnContainerDivB);
          const slideOneInterval = setInterval(slideAnimateMaybeSpawn, layer.options.speed, spawnContainerDivA, layer.options.speed, {'left': '100vw'}, {'left': '-100vw'}, 0, layer.options);
          runningIntervals.push(slideOneInterval);
          setTimeout(() => {
            const slideTwoInterval = setInterval(slideAnimateMaybeSpawn, layer.options.speed, spawnContainerDivB, layer.options.speed, {'left': '100vw'}, {'left': '-100vw'}, 0, layer.options);
            runningIntervals.push(slideTwoInterval);
          }, layer.options.speed / 2);
        }
      }
      animationContainer.append(tempLayerDiv);
    });
  }

  /**
   * @param {*} element
   * @param {*} speed
   * @param {*} propertyStart
   * @param {Keyframe[] | PropertyIndexedKeyframes} propertyEnd
   * @param {*} delayTime
   * @param {*} options
   * @param {*} props
   */
  function slideAnimateMaybeSpawn(element = HTMLElement, speed = 0, propertyStart = {}, propertyEnd= {}, delayTime = 0, options = {}, props = []) {
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
    getJson(siteUrl + "player/getTop", (lastMonthTop3)=>{
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
    }, true);
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
            <div class="card user-card bg-white fw-bold" data-label="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Gäst &nbsp;&nbsp;&nbsp;">
                <div class="card-block position-relative">
                    <div class="user-image">
                        <img src="../../backend/API/static/characters/idle_avatar/guest_0.gif" class="img-radius" alt="User-Profile-Image">
                    </div>
                    <h4 class="f-w-600 m-b-10">Välkommen till Knowit</h4>
                    <p class="m-t-10 fs-4 text-muted text-start">Känner inte igen dig, om du är en gäst var vänlig och presentera dig i receptionen.</p>
                </div>
            </div>`;
            } else {
              let birthDayClass = obj.birthday_today ? 'birthday-gif': '';
              newElement.innerHTML = `
            <div class="card user-card bg-white fw-bold ${birthDayClass}" data-label="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Level: ${obj.level}">
                <div class="card-block position-relative">
                    <div class="user-image position-relative">
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
                     <!-- show gained xp if value is set -->
                    ${obj.xpGained ? '<p class="m-t-25 fs-4 text-muted text-start">Du fick precis ' + obj.xpGained + 'xp, bra jobbat!</p>' : ''}
                    </div>
                </div>
            </div>`;
              // trigger speech bubble for character
              if(obj.xpGained){
                $("#msg-emp-id-" + obj.emp_id).empty().append(stMnts.statements[Math.floor((Math.random() - 0.001) * stMnts.statements.length)].statement).fadeIn('slow').delay(4000).fadeOut('slow');
                $("#dust-img-" + obj.emp_id).attr('src','./img/run-dust.gif?'+Math.random());
              }
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

  function clearAllIntervals() {
    $.each(runningIntervals, (index, interval) => {
      clearInterval(interval);
    });
  }

  function goodToKnow(){
    getJson(siteUrl + 'admin/theme?config=localNews', (jsonGoodToKnow)=>{
      $("#good-to-know").html("");
      $.each(jsonGoodToKnow.news, (index, newsItem)=>{
        $("#good-to-know").append("<div class='list-group-item'>" + newsItem + "</div>");
      });
    }, true);
  }

  function settings() {
    // populate override select field
    $.each(themesJson, (catIndex, themeCat) => {
      $.each(themeCat, (themeIndex, theme) => {
        if(theme.category === appConfig.themeOverride.themeCategory && Object.keys(themeCat[0] === appConfig.themeOverride.themeName)){
          themeSelectOptions.children().removeAttr("selected");
          themeSelectOptions.append("<option value='{\"" + theme.category + "\":\"" + Object.keys(themeCat)[0] + "\"}' selected>" + Object.keys(themeCat)[0] + "</option>");
        }else{
          themeSelectOptions.append("<option value='{\"" + theme.category + "\":\"" + Object.keys(themeCat)[0] + "\"}'>" + Object.keys(themeCat)[0] + "</option>");
        }
      })
    })

   // set theme settings form based on saved data
    if(appConfig.themeOverride.active){
      $("#override-theme-radio").attr('checked', true);
      themeSelectOptions.prop('disabled', false);
    }else{
      $("#seasonal-theme-radio").attr('checked', true);
    }

    // toggle seasonal theme or override theme
    $('input[name="set-theme"]').on('click change', function () {
      if ($(this).val() === "override") {
        themeSelectOptions.prop('disabled', false);
        if(themeSelectOptions.children("option:selected").val() !== ""){
          appConfig.themeOverride.active = true;
        }else{
          return true;
        }
      } else if ($(this).val() === "seasonal") {
        themeSelectOptions.prop('disabled', true);
        appConfig.themeOverride.active = false;
      }
      // save theme settings and set theme
      let tempThemeJson = $.parseJSON(themeSelectOptions.val().replace(/\\/g, ""));
      appConfig.themeOverride.themeCategory = Object.keys(tempThemeJson)[0];
      appConfig.themeOverride.themeName = tempThemeJson[Object.keys(tempThemeJson)[0]];
      saveJson("admin/theme?config=appConfig", appConfig);
      setTheme();
    });

    $('select[id="override-theme-select"]').on('change', function () {
      if ($(this).val() !== "Override theme") {
        let tempThemeJson = $.parseJSON($(this).val().replace(/\\/g, ""));
        appConfig.themeOverride.active = true;
        appConfig.themeOverride.themeCategory = Object.keys(tempThemeJson)[0];
        appConfig.themeOverride.themeName = tempThemeJson[Object.keys(tempThemeJson)[0]];

        //save theme settings and set theme
        saveJson("admin/theme?config=appConfig", appConfig);
        setTheme();
      }
    });
  }

  /**
   * @param {string} url
   * @param callback
   * @param isAsync
   * @returns {Object|null}
   */
  function getJson(url, callback = null, isAsync = false){
    let json = null;
    $.ajax({
      'async': isAsync,
      'global': false,
      'url': url,
      'dataType': "json",
      'success': function (data) {
        if (data !== undefined)
          json = data;
        if (typeof callback === "function"){
          callback(data);
          return true;
        }
      }
    });
    return json;
  }

  /**
   * @param {string} theUrl
   * @param {*} myText
   */
  function saveJson(theUrl, myText = {}) {
    $.ajax({
      type: 'POST',
      url: siteUrl + theUrl,
      data: JSON.stringify(myText),
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function (result) {
        console.log('success save json ' + result);
      }
    });
  }

  /**
   * @param element
   * @param speed
   * @param tips
   */
  function tipsFadeInFadeOut(element = HTMLElement, speed = 0, tips = {}) {
    element.html(tips[Math.floor(Math.random() * tips.length)]);
    element.hide().fadeIn(speed * 0.1).delay(speed * 0.7).fadeOut(speed * 0.1).delay(speed * 0.1);
  }

  /**
   * @param where
   * @param {*[]} props
   * @param options
   */
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

  /**
   * @param {{[p: string]: T}} persons
   */
  function refreshDisplay(persons={}) {
    let counter = 1;
    let counterLimit = 5;
    let displayPlacement = $("#display-placements");
    displayPlacement.empty();

    let personsArry = Object.entries(persons);
    personsArry.sort(function (first, next){
      return next[1][0] - first[1][0];
    });

    $.each(personsArry, (index, person)=>{
      if(person[1][0] && counter <= counterLimit){
        displayPlacement.append('#' + counter + ': ' + person[1][1] + '<br>');
        counter++;
      }
    });
    displayPlacement.append('..........');
  }

  function spawnCharacters() {
    let charactersFolder = "../../backend/API/static/characters/running_avatar/";
    let randTop = 0;
    $.ajax({
      url: siteUrl + 'player/getMonthlyXP',
      type: "GET",
      dataType: "json",
      success: function (data) {
        refreshDisplay(data);

        let maxContainerHeight = 0.7;
        let maxContainerWidth = 70;

        let maxValue = 0;
        let empCount = Object.keys(data).length;
        let previousEmpId = 0;

        $.each(data, (i, el) => {
          if (el[0] > maxValue)
            maxValue = el[0];
        });

        $.each(data, function (index, person) {
          person = person[0];
          let tempImg = $("#emp-char-" + index);
          if (!person) {
            tempImg.remove();
            $("#smokeSpawn-" + index).remove();
            --empCount;
            return true;
          }
          if (randTop === 0) {
            randTop = 1;
          } else {
            randTop += (100 / empCount) * maxContainerHeight;
          }
          let leftPos = person / maxValue * maxContainerWidth; // 70% the track is the front of the track

          // create running char if not created
          if (!tempImg.length) {
            tempImg = "<div id='emp-char-" +
              index + "' style='z-index:10000; " +
              "position: absolute; " +
              "left: 1%; top:" + randTop +
              "%;'><img class='spawnChars' alt='emp-char-avatar' src='" +
              charactersFolder + "emp_" +
              index + ".gif' width='150'><img alt='spawn smoke' class='smokeSpawn' id='spawnSmoke-" + index +
              "' src='./img/invisible-smoke.png' style='position:absolute; left: -40px; top: -80px;'>" +
              "<div id='msg-emp-id-"+ index +"' " +
              "class='message position-absolute start-100 bottom-100 text-break text-white bg-digital-pop fw-bold'></div>" +
              "<img id='dust-img-" + index +"' src='./img/invisible-smoke.png?"+Math.random()+"' class='position-absolute start-0 bottom-0 translate-middle-x' width='164' alt='run dust'></div>";
          }
          if (!$("#track-area").children().length) {
            $("#track-area").append(tempImg);
            $("#emp-char-" + index + " .spawnChars").delay(600).fadeIn(400);
            $("#spawnSmoke-" + index).attr("src", "./img/spawnSmoke.gif?" + Math.random());
            $("#dust-img-" + index).delay(300).attr('src','./img/run-dust.gif?'+Math.random());
          } else {
            if ($("#emp-char-" + index).length) {
              $("#emp-char-" + index).insertAfter("#emp-char-" + previousEmpId);
              $("#spawnSmoke-" + index).attr("src", "./img/invisible-smoke.png");
            } else {
              $(tempImg).insertAfter("#emp-char-" + previousEmpId);
              $("#emp-char-" + index + " .spawnChars").delay(600).fadeIn(400);
              $("#spawnSmoke-" + index).attr("src", "./img/spawnSmoke.gif");
              $("#dust-img-" + index).delay(300).attr('src','./img/run-dust.gif?'+Math.random());
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
    return new Promise((res, rej) => {
      let imgs = [];
      $.ajax({
        url: folderUrl, success: (data) => {
          $(data).find("a").attr("href", (i, value) => {
            if (value.match(/\.(png|gif|webp)$/)) {
              imgs.push(folderUrl + value);
            }
          });
            res(imgs);
        }, error: (e) => {
          rej(e);
        }
      });
    });
  }

});
