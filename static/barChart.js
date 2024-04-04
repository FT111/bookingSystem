
(async function() {

    Chart.defaults.color = 'slategrey';
    window.ticketChart = new Chart(
      document.getElementById('barChart1'),
      {
        type: 'bar',
        data: {
          labels: stats.statsPerViewing.map(row => row.viewingName),
          datasets: [   
            {
                
              label: 'Tickets sales per performance',
              data: stats.statsPerViewing.map(row => row.tickets),
            }
          ]
        },
        options: {
            elements: {
            bar: {
                    backgroundColor: '#5f95cf',
                    borderRadius: 6,
                    hoverBackgroundColor: '#3673b5',
                }
            },
            plugins: {
                legend: {
                    display: false,
                }
            }
        }
    
      }
    );
  })();

// document.getElementById('timePeriodSelector').addEventListener('change', (e) => {
//     ticketChart.update();
// })