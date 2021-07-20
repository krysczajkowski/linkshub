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
                        label: 'Unique Profile Views',
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
        fetch('dashboard_main_chart', {
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
                $('#summary_links_clicks').html(data['links_clicks'])
                $('#summary_platforms_clicks').html(data['platforms_clicks'])
                $('#summary_lcpr_percent').html(data['lcpr_percent']+ '%')
            }
        })
    }

    // Get data for location table
    const getLocationTableData = (sdate, edate) => {

        return fetch('location_table', {
            body: JSON.stringify({'sdate': sdate, 'edate': edate}),
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json; charset=UTF-8',
                'X-CSRFToken': csrftoken
              },
        })
        .then(response => {
            return response.json() //Convert response to JSON
        }).then(function(json) {
            return json
        })
    }

    // Create a location table
    const getLocationTable = (sdate, edate, order, column, sort_obj) => {

        // Get data for location table from getLocationTableData func
        getLocationTableData(sdate, edate).then(data => {
            var fetch_data = Object.values(data)[0]

            // Empty previous table
            location_tbody = $('.location-tbody')
            location_tbody.empty()

            // Set ordering and arrow emoji
            if (order == 'desc') {
                if (sort_obj) {
                    sort_obj.data('order', 'asc')
                    $('#location-table-sort-emoji').remove()
                    sort_obj.append('<i class="fas fa-sort-amount-down-alt text-muted font-size-09" id="location-table-sort-emoji"></i>')
                }
            
                fetch_data = fetch_data.sort((a, b) => a[column] > b[column] ? 1 : -1)
            } else {
                if (sort_obj) {
                    sort_obj.data('order', 'desc')
                    $('#location-table-sort-emoji').remove()
                    sort_obj.append('<i class="fas fa-sort-amount-down text-muted font-size-09" id="location-table-sort-emoji"></i>')
                }

                fetch_data = fetch_data.sort((a, b) => a[column] < b[column] ? 1 : -1)
            }

            // Create HTML table
            for(let i = 0; i < fetch_data.length; i++) {
                location_tbody.append(`<tr>
                    <td><img src="/media/flags/${fetch_data[i]['country']}.svg" style='width: 20px; height: auto;' class='me-2' alt="">${fetch_data[i]['country']}</td>
                    <td>${fetch_data[i]['visitors']}</td>
                    <td>${fetch_data[i]['links_clicks']}</td>
                    <td>${fetch_data[i]['platforms_clicks']}</td>
                </tr>`)
            }

        })

    }
    

$(function() {
    // Initial time period for the summary chart
    var start = moment().subtract(7, 'days');
    var end = moment();

    // Create default summary chart and location table
    getSummaryChart(start, end)
    getSummary(start, end)
    getLocationTable(start, end, 'asc', 'visitors')

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
        const start = picker.startDate.format('YYYY-MM-DD');
        const end = picker.endDate.format('YYYY-MM-DD');

        getSummaryChart(start, end)
        getSummary(start, end)
        getLocationTable(start, end, 'asc', 'visitors')

        $('#location-table-sort-emoji').remove()
        $('#visitors-th').append('<i class="fas fa-sort-amount-down text-muted font-size-09" id="location-table-sort-emoji"></i>')
    });

    // Event listener for sorting location table
    $('#location-table th').on('click', function() {
        var column = $(this).data('column')
        var order = $(this).data('order')

        if (order == 'desc') {
            getLocationTable(start, end, 'desc', column, $(this))
        } else {
            getLocationTable(start, end, 'asc', column, $(this))
        }
    })
});


