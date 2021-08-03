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

    // Get links type
    var links_type = document.querySelector('#links-type').dataset.type

    if (links_type == 'premium') {
        $('#type-of-link').html('PREMIUM LINKS CLICKS')

        $('.link-dot').addClass('premium-link-dot')
        $('.link-dot').removeClass('link-dot')

        var chart_link_type = 'Premium Link Clicks'
        var chart_link_color = '#ffa600'

    } else {
        document.querySelector('#type-of-link').innerHTML = 'LINKS CLICKS'

        var chart_link_type = 'Link Clicks'
        var chart_link_color = '#36a2eb'
    }

    // Create a chart function
    const createChart = (ctx_id, link_title, profile_views, link_data, clicks_sum, dates) => {
        var ctx = document.getElementById(ctx_id).getContext('2d');

            window.myCharts = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: dates,
                    datasets: [{
                        label: chart_link_type,
                        fill: false,
                        data: link_data,
                        borderColor: chart_link_color,
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
                        text: [`${link_title}`, `Total Clicks: ${clicks_sum}`],
                        fontSize: 15,
                        padding: 16
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    },
                },
            });     
    }

    // Render links charts
    const renderChart = (sdate, edate) => {
        fetch('links_advanced_charts', {
            body: JSON.stringify({'sdate': sdate, 'edate': edate, 'links_type': links_type}),
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
                console.log(results['clicks_data'])
                const dates = results['dates_n_views']['datelist']
                const visitors = results['dates_n_views']['visitors']

                results['clicks_data'].forEach((link, index) => {
                    const ctx_id = `chart-${index}`
                    const chart_container_id = `chart-container-${index}`


                    if (!$(`#${ctx_id}`).length) {
                        var chart = $(`<div class="col-12 col-md-10 col-xxl-8 offset-md-1 offset-xxl-2 mt-4 card mb-4">
                        <div id='${chart_container_id}'>
                            <canvas id="${ctx_id}" style="position: relative; height: 40vh; width:80vw"></canvas>
                        </div></div>`)
    
                        $('#charts-container').append(chart)

                    } else {
                        $(`#${ctx_id}`).remove(); // this is my <canvas> element
                        $(`#${chart_container_id}`).append(`<canvas id="${ctx_id}" style="position: relative; height: 40vh; width:80vw"><canvas>`);
                    }

                    const link_data = link['clicks']
                    const clicks_sum = link['clicks_sum']
                    const title = link['title']

                    createChart(ctx_id, title, visitors, link_data, clicks_sum, dates)
                });
            }
        })
    }

    // Get summary tiles data
    const getSummary = (sdate, edate) => {
        fetch('dashboard_summary', {
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
                const data = results['data']
                $('#summary_visitors').html(data['visitors'])
                if (links_type == 'premium') {
                    $('#summary_links_clicks').html(data['premium_links_clicks'])
                    $('#summary_lcpr_percent').html(data['plcpr_percent']+ '%')
                } else {
                    $('#summary_links_clicks').html(data['links_clicks'])
                    $('#summary_lcpr_percent').html(data['lcpr_percent']+ '%')
                }

            }
        })
    }

$(function() {
    // Initial time period for the summary chart
    var start = moment().subtract(7, 'days');
    var end = moment();

    // Create default summary chart and location table
    renderChart(start, end)
    getSummary(start, end)

    function cb(start, end) {
        $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    }

    // Date picker options etc
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
        start = picker.startDate.format('YYYY-MM-DD');
        end = picker.endDate.format('YYYY-MM-DD');

        renderChart(start, end)
        getSummary(start, end)
    });
});


