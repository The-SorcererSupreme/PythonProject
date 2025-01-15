<div id="throughput_chart" class="content-display-left content-display-height">
<h2 style="text-align: center;">Throughput Monitor</h2>
<canvas id="lineChart"></canvas>
</div>
<script>
    $(document).ready(function () {
        // Function to fetch and update data
        <?php 
        //session_start();
        $_SESSION['latestId'] = 0;
        ?>
  // Function to fetch and update data
  function fetchDataAndUpdateChart() {
            $.getJSON('php/get_throughput_data.php', function (data) {
                if (data.length > 0) {
                    var dtTimestamp = data.map(function (row) {
                        return row.dtTimestamp;
                    });

                    var dtIncoming = data.map(function (row) {
                        return row.dtIncoming;
                    });

                    var dtOutgoing = data.map(function (row) {
                        return row.dtOutgoing;
                    });


                    // Limit x-axis to 30 entries
                    if (lineChart.data.labels.length > 30) {
                        lineChart.data.labels.shift();
                        lineChart.data.datasets[0].data.shift();
                        lineChart.data.datasets[1].data.shift();
                    }
                    // Cut y-axis data 30 entries to prevent loading the enitre fetch
                    if (lineChart.data.labels.length > 30) {
                        lineChart.data.labels = lineChart.data.labels.slice(-30);
                        lineChart.data.datasets[0].data = lineChart.data.datasets[0].data.slice(-30);
                        lineChart.data.datasets[1].data = lineChart.data.datasets[1].data.slice(-30);
                    }
                    // Append new data to the existing chart data
                    lineChart.data.labels.push(...dtTimestamp);
                    lineChart.data.datasets[0].data.push(...dtIncoming);
                    lineChart.data.datasets[1].data.push(...dtOutgoing);
                    // Update the chart
                    lineChart.update();
                }
            });
        }

        // Create a line chart
        var ctx = document.getElementById('lineChart').getContext('2d');
        var lineChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [
                    {
                        label: 'Incoming',
                        data: [],
                        borderColor: 'blue',
                        fill: false
                    },
                    {
                        label: 'Outgoing',
                        data: [],
                        borderColor: 'orange',
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: [{
                        type: 'linear',
                        position: 'bottom'
                    }]
                }
            }
        });

        // Fetch and update data every 5 seconds (adjust the interval as needed)
        setInterval(fetchDataAndUpdateChart, 100);
    });
</script>