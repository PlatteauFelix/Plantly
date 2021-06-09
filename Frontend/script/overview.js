'use strict';

const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

//#region ***  DOM references                           ***********
let htmlOverview;
//#endregion

//#region ***  Callback-Visualisation - show___         ***********
const showHistory = function (jsonObject) {
  document.querySelector('.js-search').classList.remove('u-hidden');

  let html = `<tr>
                    <th>History ID</th>
                    <th>Action date</th>
                    <th>Value</th>
                    <th>Device ID</th>
                    <th>Action ID</th>
                </tr>`;

  for (const data of jsonObject.data) {
    html += ` <tr>
                    <td>${data.HistoryID}</td>
                    <td>${data.ActionDate}</td>
                    <td>${data.Value}</td>
                    <td>${data.DeviceID}</td>
                    <td>${data.ActionID}</td>
                </tr>`;
  }

  document.querySelector('.js-table').innerHTML = html;
};

const showActions = function (jsonObject) {
  document.querySelector('.js-search').classList.add('u-hidden');
  let html = `<tr>
                    <th>Action ID</th>
                    <th>Action description</th>
                </tr>`;

  for (const data of jsonObject.data) {
    html += ` <tr>
                    <td>${data.ActionID}</td>
                    <td>${data.Description}</td>
                </tr>`;
  }

  document.querySelector('.js-table').innerHTML = html;
};

const showDevices = function (jsonObject) {
  document.querySelector('.js-search').classList.add('u-hidden');
  let html = `<tr>
                    <th>Device ID</th>
                    <th>Name</th>
                    <th>Description</th>
                    <th>Type</th>
                    <th>Minimum Value</th>
                    <th>Maximum Value</th>
                    <th>Unit</th>
                </tr>`;

  for (const data of jsonObject.data) {
    html += ` <tr>
                    <td>${data.DeviceID}</td>
                    <td>${data.Name}</td>
                    <td>${data.Description}</td>
                    <td>${data.Type}</td>
                    <td>${data.MinValue}</td>
                    <td>${data.MaxValue}</td>
                    <td>${data.Unit}</td>
                </tr>`;
  }

  document.querySelector('.js-table').innerHTML = html;
};
//#endregion

//#region ***  Callback-No Visualisation - callback___  ***********
//#endregion

//#region ***  Data Access - get___                     ***********
const getHistory = function () {
  handleData(`http://${lanIP}/api/v1/history`, showHistory);
};
const getActions = function () {
  handleData(`http://${lanIP}/api/v1/actions`, showActions);
};
const getDevices = function () {
  handleData(`http://${lanIP}/api/v1/devices`, showDevices);
};
//#endregion

//#region ***  Event Listeners - listenTo___            ***********
const listenToNav = function () {
  let buttonHistory = document.querySelector('.js-buttonHistory');
  let buttonActions = document.querySelector('.js-buttonActions');
  let buttonDevices = document.querySelector('.js-buttonDevices');

  buttonHistory.addEventListener('click', function () {
    getHistory();
  });
  buttonActions.addEventListener('click', function () {
    getActions();
  });
  buttonDevices.addEventListener('click', function () {
    getDevices();
  });
};
//#endregion

//#region ***  Init / DOMContentLoaded                  ***********
document.addEventListener('DOMContentLoaded', function () {
  console.log('DOM content loaded');
  htmlOverview = document.querySelector('.js-overview');
  document.querySelector('.js-logoLink').href = `http://${window.location.hostname}`

  getHistory();
  listenToNav();
});
//#endregion
