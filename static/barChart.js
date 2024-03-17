(async function() {
    const data = [
      { year: 2010, count: 10 },
      { year: 2011, count: 20 },
      { year: 2012, count: 15 },
      { year: 2013, count: 25 },
      { year: 2014, count: 22 },
      { year: 2015, count: 30 },
      { year: 2016, count: 28 },
    ];
    Chart.defaults.color = 'slategrey';
    new Chart(
      document.getElementById('barChart1'),
      {
        type: 'bar',
        data: {
          labels: data.map(row => row.year),
          datasets: [   
            {
                
              label: 'Tickets sales per performance',
              data: data.map(row => row.count),
            }
          ]
        },
        options: {
            elements: {
            bar: {
                    backgroundColor: '#5fcfa4',
                    borderRadius: 10,
                    hoverBackgroundColor: '#4ea880',
                }
            },
            plugins: {
                legend: {
                    labels: {
                        font: {
                            size: 16,
                            family: "'Inter','Helvetica Neue','Helvetica','Arial', sans-serif",
                            weight: 'bold'
                        }
                    }
                }
            }
        }
    
      }
    );
  })();