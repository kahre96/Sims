$(function () {
  let propFolder = "img/themes/seasons/summer/a/props/";
  // let props = getImgsFromFolder(propFolder);

  getImgsFromFolder(propFolder).then(props => {
    spawnProps("#propslist", props);
    spawnProps("#propslist2", props);
    setInterval(spawnProps, 12000, "#propslist", props);
    setTimeout(function () {
      setInterval(spawnProps, 12000, "#propslist2", props);
    }, 6000);
  });

  spawnCharacters();

});

function spawnProps(where = '', props) {
  for (let i = 0; i < $(where + " .prop").length; i++) {
    $(where + " .spawn" + i).find("img").remove();
    let tempImgUrl = props[Math.floor(Math.random() * props.length)];
    getMeta(tempImgUrl).done(function (imgSize) {
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
  let amount = 100;
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

  $('<img/>').attr('src', url).one("load", function () {
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
      success: function (data) {
        $(data).find("a").attr("href", function (i, val) {
          if (val.match(/\.(png|gif)$/)) {
            imgs.push(folderUrl + val);
          }
          resolve(imgs);
        });
      },
      error: function (error) {
        reject(error);
      }
    });
  });
}
