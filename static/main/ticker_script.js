document.addEventListener("DOMContentLoaded", function(){

    // process data passed from django view(for chart usage)
    let last_30_trading_dates = JSON.parse(document.getElementById('last_30_trading_dates').textContent);
    let last_30_close_price = JSON.parse(document.getElementById('last_30_close_price').textContent);
    // chart construct and config
    const ctx = document.getElementById('myChart');
    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: last_30_trading_dates,
            datasets: [{
                label: 'last 30 trading day close price',
                data: last_30_close_price,
                backgroundColor: [
                    'rgba(255, 174, 74, 0.7)',

                ],
                borderColor: [
                    'rgba(178, 178, 178, 0.7)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive:true,
            scales: {
                y: {
                    suggestedMin:100,
                    suggestedMax:200,
                },
                x: {
                    // display: false
                }
            }
        }
    });

    // TODO: write fetch functions and follow view(what's api view?)
    followbtn = document.querySelector(".btn-follow")
    notifbtn = document.querySelector(".btn-notif")
    notif_testbtn = document.querySelector(".btn-notif-test")

    notif_testbtn.addEventListener('click',function(){
        var ticker = this.dataset.ticker
        test_notification(ticker)
    })

    followbtn.addEventListener('click',function(){
        var ticker = this.dataset.ticker
        update_follow(ticker)
    })
    notifbtn.addEventListener('click',function(){
        var ticker = this.dataset.ticker
        update_notification_list(ticker)
    })


    function test_notification(ticker){
        var url = '/test_notification/'
        fetch(url,{
            method:"POST",
            headers:{
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({'user': user,'ticker': ticker})
        })
        .then((response)=>{
            return response.json()
        })
        .then((data)=>{
            alert('Test email has been sent.')
        })
    }

    function update_follow(ticker){
        var followbtn = document.querySelector(".btn-follow")
        var notifbtn = document.querySelector(".btn-notif")
        var url = '/update_follow/'

        fetch(url,{
            method:"POST",
            headers:{
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({'user': user,'ticker': ticker})
        })
        .then((response)=>{
            return response.json()
        })
        .then((data)=>{
            if(data == 'added'){
                followbtn.innerHTML = 'Unfollow'
                alert('stock added to watchlist')
            }
            else if(data == 'removed'){
                followbtn.innerHTML = 'Follow'
                alert('stock removed from watchlist')
            }

        })
    }
    function update_notification_list(ticker){
        var followbtn = document.querySelector(".btn-follow")
        var notifbtn = document.querySelector(".btn-notif")
        var url = '/update_notification_list/'

        fetch(url,{
            method:"POST",
            headers:{
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({'user': user,'ticker': ticker})
        })
        .then((response)=>{
            return response.json()
        })
        .then((data)=>{
            if(data == 'added'){
                notifbtn.innerHTML = 'Cancel Notification'
                alert('stock added to notification list')
            }
            else if(data == 'removed'){
                notifbtn.innerHTML = 'Get Notification'
                alert('stock removed from notification list')
            }

        })
    }
});
  