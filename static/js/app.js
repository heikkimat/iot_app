'use strict'
var LineGraph1;
var LineGraph2;
var LineGraph3;
var g1;
var g2;
var g3;
piirra('1');

function piirra(selectedValue){
  var options = {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json;charset=UTF-8'
    },
    body: JSON.stringify({
      range: selectedValue
    })
  };
  fetch('/data', options)
  .then(function (response) {
  return response.json();
  })
  .then(function (data) {
      console.log(data);
      //data to arrays
      var timestamp = [];
      var temp = [];
      var hum = [];
      var temp2 = [];
      var temp_max =-101.1;
      var temp_min = 101.1;
      var hum_max =-101.1;
      var hum_min = 101.1;
      var temp2_max =-101.1;
      var temp2_min = 101.1;
      for(var i=0; i < data.length; i++) {
        timestamp.push(data[i].timestamp);
        temp.push(data[i].temp);
        hum.push(data[i].hum);
        temp2.push(data[i].temp2);
        if(data[i].temp > temp_max) temp_max = data[i].temp;
        if(data[i].temp < temp_min) temp_min = data[i].temp;
        if(data[i].hum > hum_max) hum_max = data[i].hum;
        if(data[i].hum < hum_min) hum_min = data[i].hum;
        if(data[i].temp2 > temp2_max) temp2_max = data[i].temp2;
        if(data[i].temp2 < temp2_min) temp2_min = data[i].temp2;
      }

      // check if sql query has returned empty array
      if(timestamp.length == 0){
          console.log("ei mittaustuloksia");
          const chrts = ["#chart_temp","#chart_hum","#chart_temp2"];
          chrts.forEach(function(element){
          var canvas = $(element).get(0); //document.getElementById("temp1");
          var ctx = canvas.getContext("2d");
          ctx.clearRect(0,0,canvas.width, canvas.height);
          ctx.font = "30px Arial";
          ctx.strokeText("Ei mittaustuloksia",20,50);
          });
          return;
      }
      
      // define time units
      var uni = '';
      var start = new Date();
      start.setHours(0,0,0,0);
      var end = new Date();
      end.setHours(24,0,0,0);
      var uss = 2;
      switch(selectedValue) {
          case "30":
            uni = 'day';
            start.setDate(1);
            end.setDate(31);
          break;
          case "365":
            uni = 'month';
            start.setDate(1);
            start.setMonth(0);
            end.setDate(31);
            end.setMonth(12);
            uss = 1;
          break;
          default:
          uni = 'hour';
      }
      //Min and Max
      document.getElementById("temp_max").innerHTML = "Max: " + Math.round(temp_max*10)/10 + " C";
      document.getElementById("temp_min").innerHTML = "Min: " + Math.round(temp_min*10)/10 + " C";
      document.getElementById("hum_max").innerHTML = "Max: " + Math.round(hum_max*10)/10 + " %";
      document.getElementById("hum_min").innerHTML = "Min: " + Math.round(hum_min*10)/10 + " %";
      document.getElementById("temp2_max").innerHTML = "Max: " + Math.round(temp2_max*10)/10 + " C";
      document.getElementById("temp2_min").innerHTML = "Min: " + Math.round(temp2_min*10)/10 + " C";

      //charts 
      var ctx1 = document.getElementById('chart_temp').getContext('2d');
      var ctx2 = document.getElementById('chart_hum').getContext('2d');
      var ctx3 = document.getElementById('chart_temp2').getContext('2d');
     
      if(LineGraph1 != undefined) 
        LineGraph1.destroy(); 
      LineGraph1 = new Chart(ctx1, {
          type: 'line',
          data: {
          labels: timestamp,
          datasets: [
              {
              label: "Sisälämpötila [C]", //
              fill: false,
              lineTension: 0,
              backgroundColor: "rgba(59, 89, 152, 0.75)",
              borderColor: "rgba(59, 89, 152, 1)",
              pointHoverBackgroundColor: "rgba(59, 89, 152, 1)", //
              pointHoverBorderColor: "rgba(59, 89, 152, 1)",
              borderWidth: 1,
              pointRadius: 1.2,
              data: temp  //
              }
          ]
          },
          options: {
              legend: {
              display: false
              },
              scales: {
              yAxes: [{
              type: 'linear',
  /*             ticks: {
                  suggestedMax: 25,
                  suggestedMin: 15
              }
  */            }],
              xAxes: [{
              type: 'time',
              display: true,
              time: {
                minUnit: uni,
                unit: uni,
                displayFormats: {
                    'minute': 'MM',
                    'hour': 'HH',
                    'day': 'DD',
                    'month': 'MMM'
                },
                unitStepSize: uss,
                min: start,
                max: end
              },
              distribution: 'linear',
          }]
          }
          }
      }); //eof LineGraph1
      if(LineGraph2 != undefined) 
      LineGraph2.destroy(); 
      LineGraph2 = new Chart(ctx2, {
          type: 'line',
          data: {
          labels: timestamp,
          datasets: [
              {
              label: "Sisäilman kosteus [%]",
              fill: false,
              lineTension: 0,
              backgroundColor: "rgba(29, 202, 255, 0.75)",
              borderColor: "rgba(29, 202, 255, 1)",
              pointHoverBackgroundColor: "rgba(29, 202, 255, 1)",
              pointHoverBorderColor: "rgba(29, 202, 255, 1)",
              borderWidth: 1,
              pointRadius: 1.2,
              data: hum
              }
          ]
          },
          options: {
              legend: {
              display: false
              },
              scales: {
              yAxes: [{
              type: 'linear',
  /*             ticks: {
                  suggestedMax: 100,
                  suggestedMin: 0
              }
  */            }],
              xAxes: [{
              type: 'time',
              display: true,
              time: {
                minUnit: uni,
                unit: uni,
                displayFormats: {
                    'minute': 'MM',
                    'hour': 'HH',
                    'day': 'DD',
                    'month': 'MMM'
                },
                unitStepSize: uss,
                min: start,
                max: end                        
              },
              distribution: 'linear',
          }]
          }
          }
      }); //eof LineGraph2
      if(LineGraph3 != undefined) 
      LineGraph3.destroy(); 
      LineGraph3 = new Chart(ctx3, {
          type: 'line',
          data: {
          labels: timestamp,
          datasets: [
          {
              label: "Ulkolämpötila [C]",
              fill: false,
              lineTension: 0,
              backgroundColor: "rgba(255, 0, 0, 0.75)",
              borderColor: "rgba(255, 0, 0, 1)",
              pointHoverBackgroundColor: "rgba(255, 0, 0, 1)",
              pointHoverBorderColor: "rgba(255, 0, 0, 1)",
              borderWidth: 1,
              pointRadius: 1.2,
              data: temp2
              }
          ]
          },
          options: {
              legend: {
              display: false
              },
              scales: {
              yAxes: [{
              type: 'linear',
  /*             ticks: {
                  suggestedMax: 30,
                  suggestedMin: -30
              }
  */            }],
              xAxes: [{
              type: 'time',
              display: true,
              time: {
                minUnit: uni,
                unit: uni,
                displayFormats: {
                    'minute': 'MM',
                    'hour': 'HH',
                    'day': 'DD',
                    'month': 'MMM'
                },
                unitStepSize: uss,
                min: start,
                max: end                        
              },
              distribution: 'linear',
          }]
          }
          }
      }); //eof LineGraph3

      //Gauges
      if (!g1) {
        g1 = new JustGage({
            id: "gauge_temp",
            value: temp[temp.length-1],
            min: 15,
            max: 25,
            title: "Sisälämpötila",
            label: "C",
            relativeGaugeSize: true
        });
        g2 = new JustGage({
            id: "gauge_hum",
            value: hum[hum.length-1],
            min: 0,
            max: 100,
            title: "Sisäilman kosteus",
            label: "%",
            relativeGaugeSize: true
        });
        g3 = new JustGage({
            id: "gauge_temp2",
            value: temp2[temp2.length-1],
            min: -30,
            max: 30,
            title: "Ulkolämpötila",
            label: "C",
            relativeGaugeSize: true,
            levelColors : [  "#3498DB",  "#E74C3C" ],
            levelColorsGradient: false
        });
      } else {
        g1.refresh(temp[temp.length-1]);
        g2.refresh(hum[hum.length-1]);
        g3.refresh(temp2[temp2.length-1]);
      }
  }) //eof then
  .catch(function (err) {
  // There was an error
  console.warn('Something went wrong.', err);
  });
}

// gets value from dropdown list
function getSelectValue(){
  var selectedValue = document.getElementById("list").value;
  piirra(selectedValue);
}
