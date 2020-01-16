/**
 * Developed by UTA Developer Team
 * URL : https://utama.tech
 */

function graph_single_line(chart_id, chart_data){
 let sales_line_chart = document.getElementById(chart_id);
 let data = {
     labels: spread_data(chart_data)[0],
     datasets: [{
         data: spread_data(chart_data)[1],
         backgroundColor: 'transparent',
         backgroundColor: 'rgba(13, 60, 129, .5)',
         borderColor: 'rgba(13, 60, 129, 1)',
         borderWidth: 2
     }]
 };
 let myLineChart = new Chart(sales_line_chart, {
 type: 'line',
 data: data,
 options: {
   legend: {
      display: false
    },
    scales: {
       yAxes: [{
           ticks: {
            beginAtZero:true,
            callback: function(value, index, values) {
              return 'Rp ' + formatNumber(value);
            }
           }
       }],
     }
 }
 });
}

function graph_bar(chart_id, chart_data){
  var ctx = document.getElementById(chart_id);
  var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: spread_data(chart_data)[0],
      datasets: [{
          data: spread_data(chart_data)[1],
          backgroundColor: 'rgba(13, 60, 129, .5)',
          borderColor: 'rgba(13, 60, 129, 1)',
          borderWidth: 1
      }]
    },
    options: {
      legend: {
         display: false
       },
      scales: {
          yAxes: [{
              ticks: {
                  beginAtZero:true,
                  callback: function(value, index, values) {
                    return formatNumber(value);
                  }
              },
          }],
          xAxes: [{
              ticks: {
                  beginAtZero:true
              },
          }]
      }
    }
  });
}

function spread_data(data){
  let chart_labels = [], chart_data= [], result= [];

  for (i=0; i < data.length; i++){
    chart_labels.push(data[i][0])
    chart_data.push(data[i][1])
  }

  result.push(chart_labels)
  result.push(chart_data)

  return result
}

function formatNumber(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
