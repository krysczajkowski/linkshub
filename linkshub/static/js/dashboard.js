    // CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');


    // Delete chart before creating a new one 
    var resetCanvas = function(){
        $('#profileViewsChart').remove(); // this is my <canvas> element
        $('#graphContainer').append('<canvas id="profileViewsChart" style="position: relative; height: 40vh; width:80vw"><canvas>');
    };

    // Create a chart function
    const renderChart = (profile_views, link_data, platform_data, dates) => {
        var ctx = document.getElementById('profileViewsChart').getContext('2d');

            window.myCharts = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [{
                        label: 'Link Clicks',
                        fill: false,
                        data: link_data,
                        borderColor: '#36a2eb',
                        borderWidth: 2
                    }, {
                        label: 'Platform Clicks',
                        type: 'line',
                        fill: false,
                        data: platform_data,
                        borderColor: 'rgba(204, 101, 254, 1)',
                        borderWidth: 2
                    }, {
                        label: 'Profile Views',
                        type: 'bar',
                        fill: false,
                        data: profile_views,
                        backgroundColor: 'rgba(255, 99, 132, 0.5)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 2
                    }]
                },
                options: {
                    aspectRatio: 1, 
                    responsive: true,
                    title: {
                        display: true,
                        text: 'Profile views and link clicks'
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
            
    }

    // Get data for the main dashboard chart
    const getSummaryChart = (sdate, edate) => {
        fetch('dashboard_summary_chart', {
            body: JSON.stringify({'sdate': sdate, 'edate': edate}),
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json; charset=UTF-8',
                'X-CSRFToken': csrftoken
              },
        })
        .then((res)=>res.json())
        .then((results)=>{
            if (results.error) {
                alert(results.error)
            } else {
                // Save data from django
                const profile_views = results.views_data
                const link_data = results.link_data
                const platform_data = results.platform_data
                const dates = results.datelist
        
                resetCanvas()
                renderChart(profile_views, link_data, platform_data, dates)
            }
        })
    }

$(function() {
    // Initial time period for the summary chart
    var start = moment().subtract(7, 'days');
    var end = moment();


    getSummaryChart(start, end)

    function cb(start, end) {
        $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    }

    $('#reportrange').daterangepicker({
        startDate: start,
        endDate: end,
        ranges: {
           'Today': [moment(), moment()],
           'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
           'Last 7 Days': [moment().subtract(6, 'days'), moment()],
           'Last 30 Days': [moment().subtract(29, 'days'), moment()],
           'This Month': [moment().startOf('month'), moment().endOf('month')],
           'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
    }, cb);

    cb(start, end);

    // The event listener for date input
    $('#reportrange').on('apply.daterangepicker', (e, picker) => {
        console.log('The value has changed.');
        const start = picker.startDate.format('YYYY-MM-DD');
        const end = picker.endDate.format('YYYY-MM-DD');

        getSummaryChart(start, end)
    });

});