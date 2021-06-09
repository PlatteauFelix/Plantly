const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

//#region ***  DOM references
let rangeValueMoisture, rangeSliderMoisture, rangeSliderMoistureOptimal, warningMoistureIcon, warningMoisture, warningMoistureText;
let rangeValueSunlight, rangeSliderSunlight, rangeSliderSunlightOptimal, warningSunlightIcon, warningSunlight, warningSunlightText;
let rangeValueTemperature, rangeSliderTemperature, rangeSliderTemperatureOptimal, warningTemperatureIcon, warningTemperature, warningTemperatureText;
let rangeValueHumidity, rangeSliderHumidity, rangeSliderHumidityOptimal, warningHumidityIcon, warningHumidity, warningHumidityText;
let rangeValueAir, rangeSliderAir, rangeSliderAirOptimal, warningAirIcon, warningAir, warningAirText;

let screenStatus, screenButton, screenFace;
let speakerStatus, speakerButton;
//#endregion

//#region ***  Callback-Visualisation - show___         ***********
const showWidth = function () {
  let widthMax = rangeSliderMoisture.offsetWidth;
  let elements = document.querySelectorAll('.c-rangeSliderOptimal');

  for (const element of elements) {
    element.style.maxWidth = widthMax + 'px';
  }

  showOptimal(rangeSliderMoisture, rangeSliderMoistureOptimal);
  showOptimal(rangeSliderSunlight, rangeSliderSunlightOptimal);
  showOptimal(rangeSliderTemperature, rangeSliderTemperatureOptimal);
  showOptimal(rangeSliderHumidity, rangeSliderHumidityOptimal);
  showOptimal(rangeSliderAir, rangeSliderAirOptimal);
};

const showOptimal = function (rangeSlider, rangeSliderOptimal) {
  let optimalMax = parseInt(rangeSliderOptimal.max);
  let max = parseInt(rangeSlider.max);
  let optimalMin = parseInt(rangeSliderOptimal.min);
  let min = parseInt(rangeSlider.min);
  let width = rangeSliderOptimal.offsetWidth;

  // set width
  let optimalWidth = width / ((max - min - 1) / (optimalMax - optimalMin));
  rangeSliderOptimal.style.width = optimalWidth + 'px';

  // set start point = min optimal value
  let shift = width / (max / optimalMin);
  rangeSliderOptimal.style.left = shift + 'px';
};

const showSlider = function (rangeValue, rangeSlider) {
  let value = rangeSlider.value; // value of slider itself
  let center = (parseInt(rangeSlider.max) + parseInt(rangeSlider.min)) / 2;
  let multiplier = (rangeSlider.clientWidth / (parseInt(rangeSlider.max) - parseInt(rangeSlider.min))) * 2;
  rangeValue.innerHTML = value; // update visual feedback of slider
  rangeValue.style.marginLeft = (value - center) * multiplier + 'px';

  listenToWarning();
  showFace();
};

const showWarning = function (slider, optimal, warning, icon, messageMin, messageMax) {
  let html = '';
  if (parseInt(slider.value) < parseInt(optimal.min)) {
    html = `<h3>Warning!</h3>
    <p>${messageMin}</p>
    <p>Keep it between the marked values for the optimal health of your plant.</p>`;
    warning.classList.remove('u-hidden');
    warning.innerHTML = html;
    icon.srcset = 'style/img/svg/close_black_48dp.svg';
  } else if (parseInt(slider.value) > parseInt(optimal.max)) {
    html = `<h3>Warning!</h3>
    <p>${messageMax}</p>
    <p>Keep it between the marked values for the optimal health of your plant.</p>`;
    warning.classList.remove('u-hidden');
    warning.innerHTML = html;
    icon.srcset = 'style/img/svg/close_black_48dp.svg';
  } else {
    warning.classList.add('u-hidden');
  }
};

const showFace = function () {
  if (screenStatus == true) {
    let moistValue = parseInt(rangeSliderMoisture.value);
    let moistMin = parseInt(rangeSliderMoistureOptimal.min);
    let moistMax = parseInt(rangeSliderMoistureOptimal.max);

    let sunValue = parseInt(rangeSliderSunlight.value);
    let sunMin = parseInt(rangeSliderSunlightOptimal.min);
    let sunMax = parseInt(rangeSliderSunlightOptimal.max);

    let tempValue = parseInt(rangeSliderTemperature.value);
    let tempMin = parseInt(rangeSliderTemperatureOptimal.min);
    let tempMax = parseInt(rangeSliderTemperatureOptimal.max);

    let humiValue = parseInt(rangeSliderHumidity.value);
    let humiMin = parseInt(rangeSliderHumidityOptimal.min);
    let humiMax = parseInt(rangeSliderHumidityOptimal.max);

    let airValue = parseInt(rangeSliderAir.value);
    let airMin = parseInt(rangeSliderAirOptimal.min);
    let airMax = parseInt(rangeSliderAirOptimal.max);

    if (moistValue < moistMin || humiValue < humiMin) {
      screenFace.srcset = 'style/img/svg/face_thirsty.svg';
      socket.emit('F2B_sendFace', { 'statusFace': 'thirsty', 'statusSpeaker': speakerStatus });
    } else if (moistValue > moistMax || humiValue > humiMax) {
      screenFace.srcset = 'style/img/svg/face_sick.svg';
      socket.emit('F2B_sendFace', { 'statusFace': 'sick', 'statusSpeaker': speakerStatus });
    } else if (sunValue < sunMin || tempValue < tempMin) {
      screenFace.srcset = 'style/img/svg/face_cold.svg';
      socket.emit('F2B_sendFace', { 'statusFace': 'cold', 'statusSpeaker': speakerStatus });
    } else if (sunValue > sunMax || tempValue > tempMax) {
      screenFace.srcset = 'style/img/svg/face_hot.svg';
      socket.emit('F2B_sendFace', { 'statusFace': 'hot', 'statusSpeaker': speakerStatus });
    } else if (airValue < airMin) {
      screenFace.srcset = 'style/img/svg/face_sad.svg';
      socket.emit('F2B_sendFace', { 'statusFace': 'sad', 'statusSpeaker': speakerStatus });
    } else if (airValue > airMax) {
      screenFace.srcset = 'style/img/svg/face_sad.svg';
      socket.emit('F2B_sendFace', { 'statusFace': 'sad', 'statusSpeaker': speakerStatus });
    } else {
      screenFace.srcset = 'style/img/svg/face_normal.svg';
      socket.emit('F2B_sendFace', { 'statusFace': 'normal', 'statusSpeaker': false });
    }
    screenFace.classList.remove('u-hidden');
    screenButton.innerHTML = 'Turn screens off';

  } else {
    screenFace.classList.add('u-hidden');
    screenButton.innerHTML = 'Turn screens on';
    socket.emit('F2B_sendFace', { 'statusFace': 'OFF', 'statusSpeaker': false });
  }
};
//#endregion

//#region ***  Callback-No Visualisation - callback___  ***********

//#endregion

//#region ***  Data Access - get___                     ***********

//#endregion

//#region ***  Event Listeners - listenTo___            ***********
const listenToResize = function () {
  window.onresize = function () {
    location.reload();
  };
  window.addEventListener('resize', showWidth);
};

const listenToRangeSlider = function () {
  rangeSliderMoisture.addEventListener('input', function () {
    showSlider(rangeValueMoisture, rangeSliderMoisture);
  });
  rangeSliderSunlight.addEventListener('input', function () {
    showSlider(rangeValueSunlight, rangeSliderSunlight);
  });
  rangeSliderTemperature.addEventListener('input', function () {
    showSlider(rangeValueTemperature, rangeSliderTemperature);
  });
  rangeSliderHumidity.addEventListener('input', function () {
    showSlider(rangeValueHumidity, rangeSliderHumidity);
  });
  rangeSliderAir.addEventListener('input', function () {
    showSlider(rangeValueAir, rangeSliderAir);
  });
};

const listenToWarning = function () {
  showWarning(rangeSliderMoisture, rangeSliderMoistureOptimal, warningMoisture, warningMoistureIcon, 'Plantly is thirsty.', 'Too much water can kill your plant.');

  showWarning(rangeSliderSunlight, rangeSliderSunlightOptimal, warningSunlight, warningSunlightIcon, 'Exposure to light is not sufficient.', 'Too much exposure to light can harm your plant.');

  showWarning(rangeSliderTemperature, rangeSliderTemperatureOptimal, warningTemperature, warningTemperatureIcon, 'Plantly is too cold.', 'Plantly is too hot.');

  showWarning(rangeSliderHumidity, rangeSliderHumidityOptimal, warningHumidity, warningHumidityIcon, 'Place your plant in a more humid place.', 'Place your plant in a less humid place.');

  showWarning(rangeSliderAir, rangeSliderAirOptimal, warningAir, warningAirIcon, 'More pollution??? WHAT?!', 'Search a place with less air pollution.');
};

const listenToUI = function () {
  screenButton.addEventListener('click', function () {
    screenStatus = !screenStatus;
    showFace()
  });

  speakerButton.addEventListener('click', function () {
    speakerStatus = !speakerStatus;
    if (speakerStatus == true){
      console.log('speakers on')
      speakerButton.innerHTML = 'Turn speakers off'
    }
    else {
      console.log('speakers off')
      speakerButton.innerHTML = 'Turn speakers on'
    }
    showFace()
  });
};

const listenToSocket = function () {
  socket.on('connect', function () {
    console.log('Connected with socket webserver');
  });

  socket.on('B2F_send_data', function (jsonObject) {
    console.log(jsonObject);

    rangeSliderMoisture.value = jsonObject.Moisture;
    showSlider(rangeValueMoisture, rangeSliderMoisture);

    rangeSliderSunlight.value = jsonObject.IR;
    showSlider(rangeValueSunlight, rangeSliderSunlight);

    rangeSliderTemperature.value = jsonObject.Temperature;
    showSlider(rangeValueTemperature, rangeSliderTemperature);

    rangeSliderHumidity.value = jsonObject.Humidity;
    showSlider(rangeValueHumidity, rangeSliderHumidity);

    rangeSliderAir.value = jsonObject.Air;
    showSlider(rangeValueAir, rangeSliderAir);
  });
};
//#endregion

//#region ***  Init / DOMContentLoaded                  ***********
const init = function () {
  rangeValueMoisture = document.querySelector('.js-rangeValueMoisture');
  rangeSliderMoisture = document.querySelector('.js-rangeSliderMoisture');
  rangeSliderMoistureOptimal = document.querySelector('.js-rangeSliderMoistureOptimal');
  warningMoistureIcon = document.querySelector('.js-warningMoistureIcon');
  warningMoisture = document.querySelector('.js-warningMoisture');
  warningMoistureText = document.querySelector('.js-warningMoistureText');

  rangeValueSunlight = document.querySelector('.js-rangeValueSunlight');
  rangeSliderSunlight = document.querySelector('.js-rangeSliderSunlight');
  rangeSliderSunlightOptimal = document.querySelector('.js-rangeSliderSunlightOptimal');
  warningSunlightIcon = document.querySelector('.js-warningSunlightIcon');
  warningSunlight = document.querySelector('.js-warningSunlight');
  warningSunlightText = document.querySelector('.js-warningSunlightText');

  rangeValueTemperature = document.querySelector('.js-rangeValueTemperature');
  rangeSliderTemperature = document.querySelector('.js-rangeSliderTemperature');
  rangeSliderTemperatureOptimal = document.querySelector('.js-rangeSliderTemperatureOptimal');
  warningTemperatureIcon = document.querySelector('.js-warningTemperatureIcon');
  warningTemperature = document.querySelector('.js-warningTemperature');
  warningTemperatureText = document.querySelector('.js-warningTemperatureText');

  rangeValueHumidity = document.querySelector('.js-rangeValueHumidity');
  rangeSliderHumidity = document.querySelector('.js-rangeSliderHumidity');
  rangeSliderHumidityOptimal = document.querySelector('.js-rangeSliderHumidityOptimal');
  warningHumidityIcon = document.querySelector('.js-warningHumidityIcon');
  warningHumidity = document.querySelector('.js-warningHumidity');
  warningHumidityText = document.querySelector('.js-warningHumidityText');

  rangeValueAir = document.querySelector('.js-rangeValueAir');
  rangeSliderAir = document.querySelector('.js-rangeSliderAir');
  rangeSliderAirOptimal = document.querySelector('.js-rangeSliderAirOptimal');
  warningAirIcon = document.querySelector('.js-warningAirIcon');
  warningAir = document.querySelector('.js-warningAir');
  warningAirText = document.querySelector('.js-warningAirText');

  screenStatus = true;
  screenButton = document.querySelector('.js-screenButton');
  screenFace = document.querySelector('.js-screenFace');

  speakerStatus = false;
  speakerButton = document.querySelector('.js-speakerButton');
};

document.addEventListener('DOMContentLoaded', function () {
  console.info('DOM geladen');
  document.querySelector('.js-logoLink').href = `http://${window.location.hostname}/overview.html`

  init();
  showWidth();
  listenToResize();
  listenToSocket();
  listenToRangeSlider();
  listenToUI();
  showFace()
});
//#endregion
