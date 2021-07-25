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
    var resetCanvas = function(chart_name){
        if(chart_name == 'summary') {
            $('#profileViewsChart').remove(); // this is my <canvas> element
            $('#SummaryGraphContainer').append('<canvas id="profileViewsChart" style="position: relative; height: 40vh; width:80vw"><canvas>');
        } else if(chart_name=='device'){
            $('#deviceChart').remove();
            $('#DeviceGraphContainer').append('<canvas id="deviceChart" style="position: relative; height: 40vh; width:80vw" data="dupa"><canvas>');
        }
    };

    // Create a chart function
    const createSummaryChart = (profile_views, link_data, platform_data, dates) => {
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
                        text: 'Profile views and link clicks',
                        fontSize: 14,
                        fontColor: '#6c757d'
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
    const renderSummaryChart = (sdate, edate) => {
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
        
                resetCanvas('summary')
                createSummaryChart(profile_views, link_data, platform_data, dates)
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
                $('#summary_pcpr_percent').html(data['pcpr_percent']+ '%')
            }
        })
    }

    // Create a chart function
    const createDeviceChart = (data) => {
        var ctx = document.getElementById('deviceChart').getContext('2d');

            window.myCharts = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['Desktop', 'Mobile'],
                    datasets: [{
                        label: 'Link Clicks',
                        fill: false,
                        data: data,
                        backgroundColor: ['#239AFF', '#ff4268'],
                        borderWidth: 2
                    }]
                },
                options: {
                    aspectRatio: 1, 
                    responsive: true,
                    title: {
                        display: true,
                        text: 'Device Analytics'
                    },
                }
            });     
    }

    const renderDevicesChart = (sdate, edate) => {
        fetch('device_chart', {
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
                const data = results
                var desktop = results['desktop']
                var mobile = results['mobile']

                resetCanvas('device')
                createDeviceChart([desktop, mobile])
            }
        })
    }

    // Get data for country table
    const getCountryData = (sdate, edate) => {

        return fetch('country_table', {
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

    // Get data for city table
    const getCityData = (sdate, edate) => {

        return fetch('city_table', {
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

    // Create a country table
    const getCountryTable = (sdate, edate, order, column, sort_obj) => {

        // Get data for location table from getCountryData func
        getCountryData(sdate, edate).then(data => {
            var fetch_data = Object.values(data)[0]

            // Empty previous table
            var country_tbody = $('.country-tbody')
            country_tbody.empty()

            // Set ordering and arrow emoji
            if (order == 'desc') {
                if (sort_obj) {
                    sort_obj.data('order', 'asc')
                    $('#country-sort-emoji').remove()
                    sort_obj.append('<i class="fas fa-sort-amount-down-alt text-muted font-size-09" id="country-sort-emoji"></i>')
                }
            
                fetch_data = fetch_data.sort((a, b) => a[column] > b[column] ? 1 : -1)
            } else {
                if (sort_obj) {
                    sort_obj.data('order', 'desc')
                    $('#country-sort-emoji').remove()
                    sort_obj.append('<i class="fas fa-sort-amount-down text-muted font-size-09" id="country-sort-emoji"></i>')
                }

                fetch_data = fetch_data.sort((a, b) => a[column] < b[column] ? 1 : -1)
            }

            // Create HTML table
            for(let i = 0; i < fetch_data.length; i++) {
                country_tbody.append(`<tr>
                    <td><img src="/media/flags/${fetch_data[i]['country']}.svg" style='width: 20px; height: auto;' class='me-2' alt="">${fetch_data[i]['country']}</td>
                    <td>${fetch_data[i]['visitors']}</td>
                    <td>${fetch_data[i]['links_clicks']}</td>
                    <td>${fetch_data[i]['platforms_clicks']}</td>
                </tr>`)
            }

        })

    }

    // Create city table
    const getCityTable = (sdate, edate, order, column, sort_obj) => {
        // Get data for location table from getCityData func
        getCityData(sdate, edate).then(data => {
            var fetch_data = Object.values(data)[0]

            // Empty previous table
            var city_tbody = $('.city-tbody')
            city_tbody.empty()

            // Set ordering and arrow emoji
            if (order == 'desc') {
                if (sort_obj) {
                    sort_obj.data('order', 'asc')
                    $('#city-sort-emoji').remove()
                    sort_obj.append('<i class="fas fa-sort-amount-down-alt text-muted font-size-09" id="city-sort-emoji"></i>')
                }
            
                fetch_data = fetch_data.sort((a, b) => a[column] > b[column] ? 1 : -1)
            } else {
                if (sort_obj) {
                    sort_obj.data('order', 'desc')
                    $('#city-sort-emoji').remove()
                    sort_obj.append('<i class="fas fa-sort-amount-down text-muted font-size-09" id="city-sort-emoji"></i>')
                }

                fetch_data = fetch_data.sort((a, b) => a[column] < b[column] ? 1 : -1)
            }

            // Create HTML table
            for(let i = 0; i < fetch_data.length; i++) {
                city_tbody.append(`<tr>
                    <td><img src="/media/flags/${fetch_data[i]['country']}.svg" style='width: 20px; height: auto;' class='me-2' alt="">${fetch_data[i]['city']}</td>
                    <td>${fetch_data[i]['visitors']}</td>
                    <td>${fetch_data[i]['links_clicks']}</td>
                    <td>${fetch_data[i]['platforms_clicks']}</td>
                </tr>`)
            }

        })
    }


$(function() {
    var location_table = 'country'

    // Initial time period for the summary chart
    var start = moment().subtract(7, 'days');
    var end = moment();

    // Create default summary chart and location table
    renderSummaryChart(start, end)
    getSummary(start, end)
    getCountryTable(start, end, 'asc', 'visitors')
    getCityTable(start, end, 'asc', 'visitors')
    renderDevicesChart(start, end)

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

        renderSummaryChart(start, end)
        getSummary(start, end)
        getCountryTable(start, end, 'asc', 'visitors')
        getCityTable(start, end, 'asc', 'visitors')
        renderDevicesChart(start, end)

        $('#country-sort-emoji').remove()
        $('#country-visitors-th').append('<i class="fas fa-sort-amount-down text-muted font-size-09" id="country-sort-emoji"></i>')

        $('#city-sort-emoji').remove()
        $('#city-visitors-th').append('<i class="fas fa-sort-amount-down text-muted font-size-09" id="city-sort-emoji"></i>')
    });

    // Event listener for sorting location table
    $('#country-table th').on('click', function() {
        var column = $(this).data('column')
        var order = $(this).data('order')

        if (order == 'desc') {
            getCountryTable(start, end, 'desc', column, $(this))
        } else {
            getCountryTable(start, end, 'asc', column, $(this))
        }
    })

    $('#city-table th').on('click', function() {
        var column = $(this).data('column')
        var order = $(this).data('order')

        if (order == 'desc') {
            getCityTable(start, end, 'desc', column, $(this))
        } else {
            getCityTable(start, end, 'asc', column, $(this))
        }
    })


    // Pick table - city or country
    var city_table = $('#city-table')
    var country_table = $('#country-table')

    var pick_country = $('#pick-country')
    var pick_city = $('#pick-city')

    pick_country.on('click', function() {
        location_table = 'country'

        country_table.removeClass('d-none')
        city_table.addClass('d-none')

        pick_country.addClass('fw-bold')
        pick_country.removeClass('text-muted')

        pick_city.removeClass('fw-bold')
        pick_city.addClass('text-muted')
    })

    pick_city.on('click', function() {
        location_table = 'city'

        city_table.removeClass('d-none')
        country_table.addClass('d-none')

        pick_city.addClass('fw-bold')
        pick_city.removeClass('text-muted')

        pick_country.removeClass('fw-bold')
        pick_country.addClass('text-muted')
    })
});


