(async function() {
    Chart.defaults.color = 'blue';
    window.revenueChart = new Chart(
        document.getElementById('pieChart1'),
        {
            type: 'pie',
            data: {
                labels: stats.statsPerViewing.map(row => row.viewingName),
                datasets: [
                    {
                        label: 'Viewing Revenue',
                        data: stats.statsPerViewing.map(row => row.revenue),
                        backgroundColor: ['#668dcc','#415d8a','#2e4a6f','#1d3a5b','#0f2c49','#0a1f36','#05132a','#000c1f','#00061a'],
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false,
                    }
                }
            }
        }
    );
})();