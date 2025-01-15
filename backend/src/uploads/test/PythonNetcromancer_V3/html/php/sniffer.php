<div id="loadedContent" style="display: none;">
<div class="table-container content-display-full content-display-height scrollable-table">
    <table id="traffic-container">
    <thead>
        <tr>
            <th>Source IP</th>
            <th>Destination IP</th>
            <th>n/a</th>
            <th>n/a</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
    </tbody>
</table>
<div>
    <label>
        <input type="checkbox" id="enableAutoscroll" checked> Enable Autoscroll
    </label>
</div>
</div>
</div>
<script>
        $(document).ready(function () {
        var enableAutoscrollCheckbox = $('#enableAutoscroll');
        var tableContainer = $('.table-container');

        // Function to fetch and update data
        function fetchDataAndUpdateTable() {
            $.getJSON('php/get_packets_data.php', function (data) {
                if (data.length > 0) {
                    var tableBody = $('#traffic-container tbody');
                    tableBody.empty();

                    data.forEach(function (row) {
                        var newRow = $('<tr>');
                        newRow.append('<td>' + row.dtSrcIP + '</td>');
                        newRow.append('<td>' + row.dtDestIP + '</td>');
                        newRow.append('<td></td>');
                        newRow.append('<td></td>');
                        tableBody.append(newRow);
                    });

                    // Check if autoscroll is enabled
                    if (enableAutoscrollCheckbox.prop('checked')) {
                        // Scroll to the bottom of the table
                        tableContainer.scrollTop(tableContainer[0].scrollHeight);
                    }
                }
                <?php $_SESSION["ready"] = "Yes";?>
            });
        }

        // Fetch and update data every 5 seconds (adjust the interval as needed)
        setInterval(fetchDataAndUpdateTable, 1000);
    });
</script>