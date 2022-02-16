document.addEventListener("DOMContentLoaded", function(){

    // process data passed from django view
    let last_30_trading_dates = JSON.parse(document.getElementById('last_30_trading_dates').textContent);
    let last_30_close_price = JSON.parse(document.getElementById('last_30_close_price').textContent);

    // chart construct and config
    const ctx = document.getElementById('myChart');
    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: last_30_trading_dates,
            datasets: [{
                label: 'last 30 close price',
                data: last_30_close_price,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive:true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
  