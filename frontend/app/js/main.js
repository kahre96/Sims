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
    placeId: BirstaID,
    fields: ['name', 'opening_hours', 'utc_offset_minutes']
  };
  const service = new google.maps.places.PlacesService(document.createElement('div'));
  service.getDetails(request, callback);

  const request2 = {
    placeId: GatanID,
    fields: ['name', 'opening_hours', 'utc_offset_minutes']
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
      }
      else {
        document.getElementById("hours-text").innerHTML += "Systembolaget i Birsta har stängt just nu!\n";
      }
      document.getElementById("hours-text").innerHTML +=
        "Torsdag: " + place.opening_hours.periods[3].open.time + " - " + place.opening_hours.periods[3].close.time + "<br/>"
        + "Fredag: " + place.opening_hours.periods[4].open.time + " - " + place.opening_hours.periods[4].close.time + "<br/>"
        + "Lördag: " + place.opening_hours.periods[5].open.time + " - " + place.opening_hours.periods[5].close.time + "<br/><br/>";
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
      }
      else {
        document.getElementById("hours-text").innerHTML += "Systembolaget på Sjögatan har stängt just nu!\n";
      }
      document.getElementById("hours-text").innerHTML +=
        "Torsdag: " + place.opening_hours.periods[3].open.time + " - " + place.opening_hours.periods[3].close.time + "<br/>"
        + "Fredag: " + place.opening_hours.periods[4].open.time + " - " + place.opening_hours.periods[4].close.time + "<br/>"
        + "Lördag: " + place.opening_hours.periods[5].open.time + " - " + place.opening_hours.periods[5].close.time + "<br/>";
    }
  }
});



$(function () {
  let ppl = [];
  let propFolder = "img/themes/seasons/summer/a/props/";

  getImgsFromFolder(propFolder).then(props => {
    spawnProps("#propslist", props);
    spawnProps("#propslist2", props);
    setInterval(spawnProps, 12000, "#propslist", props);
    setTimeout(() => {
      setInterval(spawnProps, 12000, "#propslist2", props);
    }, 6000);
  });

  spawnCharacters();
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

  function createPplsJson(count) {
    let rand = Math.floor(Math.random() * count) + 1;

    $.getJSON('https://random-data-api.com/api/v2/users?size=' + rand, function (data) {
      if (!isNaN(data.length) && (ppl.length + data.length) > count) {
        let tempNum = ppl.length + data.length - count;
        ppl.splice(0, tempNum);
      }
      if (!isNaN(data.length) && data.length > 0) {
        for (let i = 0; i < data.length; i++) {
          ppl.push(data[i]);
        }
      }
      if (ppl.length >= count) {
        $('#people-box').empty();
      }
      $.each(ppl.reverse(), function (index, obj) {
        let cardStyle = 'col first-card';
        if (index >= 1) {
          cardStyle = 'col rest-cards';
        }
        let newElement = document.createElement('div');
        newElement.setAttribute("class", cardStyle);
        newElement.innerHTML = `
            <div class="card user-card bg-white" data-label="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Lvl. #, Rookie &nbsp;&nbsp;&nbsp;">
                <div class="card-block position-relative">
                    <div class="user-image">
                        <img src="${obj.avatar}" class="img-radius" alt="User-Profile-Image">
                    </div>
                    <h6 class="f-w-600 m-t-25 m-b-10">${obj.first_name} ${obj.last_name}</h6>
                    <p class="mt-15 text-muted text-start">Lorem Ipsum is simply dummy text of the printing and typesetting industry.</p>
                    <div class="start-0 w-100">
                        <p class="m-0 p-0 text-start fw-bold fs-6 text-uppercase .text-black">next level xp:</p>
                      <div class="progress position-relative bg-clay" style="height: 30px;">
                        <div class="m-0 py-auto my-auto pe-2 position-absolute text-end w-100 fw-bolder fs-5 text-white text-stroke-black">${Math.floor(obj.social_insurance_number * 0.5 / 10000)} / ${Math.floor(obj.social_insurance_number / 10000)}</div>
                        <div class="progress-bar bg-forest" role="progressbar" style="width: ${((obj.social_insurance_number * Math.random()) / obj.social_insurance_number) * 100}%;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                    </div>
                    <div class="knw-moodchart">
                        <canvas id="knw-moodchart-${index}"></canvas>
                    </div>
                </div>
            </div>`;
        $(newElement).css({'margin-left': '-300px', 'opacity': '0.95'});
        $('#people-box').append(newElement);

        let grumpy = Math.floor(Math.random() * 21);
        let happy = Math.floor(Math.random() * 21);
        let sad = Math.floor(Math.random() * 21);
        let ambition = Math.floor(Math.random() * 21);
        let curious = Math.floor(Math.random() * 21);
        createPersonChart('knw-moodchart-' + index, grumpy, happy, sad, ambition, curious);

        $(newElement).animate({
          marginLeft: "0px"
        }, 500);
      });
      $.each($('#people-box').children(), function (index, child) {
        $(child).delay(8000 + 1000 / (index + 1)).fadeOut(1000);
      });

    });

    function createPersonChart(where, grumpy, happy, sad,  ambition, curious) {
      const labels = [
        'Grumpiness',
        'Happiness',
        'Curiousity',
        'Ambition',
        'Sadness',
      ];

      const data = {
        labels: labels,
        datasets: [{
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
        type: 'radar',
        data: data,
        options: {
          elements: {
            line: {
              borderWidth: 3
            }
          },
          plugins: {
            legend: {
              display: false,
            }
          },
          scales: {
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
      // Chart.defaults.label.font.size = 20;
      const myChart = new Chart(
        document.getElementById(where),
        config
      );
    }
  }

  createPplsJson(4);
  setInterval(createPplsJson, 12000, 4);
});


function spawnProps(where = '', props) {
  for (let i = 0; i < $(where + " .prop").length; i++) {
    $(where + " .spawn" + i).find("img").remove();
    let tempImgUrl = props[Math.floor(Math.random() * props.length)];
    getMeta(tempImgUrl).done((imgSize) => {
      imgSize.w = imgSize.w * (1 + (Math.random()) / 5);
      imgSize.h = imgSize.h * (1 + (Math.random()) / 5);
      let tempImg = "<img src='" + tempImgUrl + "' style='width: " + imgSize.w + "px; height: " + imgSize.h + "px;' >";
      $(where + " .spawn" + i).append(tempImg);
      let deg = Math.floor(Math.random() * 3) + 1;
      deg *= Math.round(Math.random()) ? 1 : -1;
      $(where + " .spawn" + i).find("img").css("transform", "rotate(" + deg + "deg)");
      let posLeft = Math.floor(Math.random() * 20) + 5;
      let posBottom = Math.floor(Math.random() * 14) + 80;
      let hueRand = Math.floor(Math.random() * 10);
      let satRand = Math.floor(Math.random() * 0.5) + 1.5;
      $(where + " .spawn" + i + " img").css({
        'left': posLeft + "%",
        'bottom': posBottom + "%",
        'position': 'absolute',
        'filter': 'hue-rotate(' + hueRand + 'deg) saturate(' + satRand + ')'
      });
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
      let tempImg = "<img src='" + tempImgUrl +
        "' style='width: " + 150 +
        "px; z-index:10000; " +
        "position: absolute; " +
        "left:" + randLeft +
        "%; top:" + randTop +
        "%; filter:hue-rotate(" + hueRand + "deg)'>";
      $("#track-area").append(tempImg);
    }
  }).catch(error => {
    console.log(error)
  });
}

function getMeta(url) {
  let r = $.Deferred();

  $('<img/>').attr('src', url).one("load", () => {
    let s = {w: this.width, h: this.height};
    r.resolve(s)
  });
  return r;
}

function getImgsFromFolder(folderUrl) {
  return new Promise((resolve, reject) => {
    let imgs = [];
    $.ajax({
      url: folderUrl,
      success: (data) => {
        $(data).find("a").attr("href", (i, val) => {
          if (val.match(/\.(png|gif)$/)) {
            imgs.push(folderUrl + val);
          }
          resolve(imgs);
        });
      },
      error: (error) => {
        reject(error);
      }
    });
  });
}


$(document).ready(function () {
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
