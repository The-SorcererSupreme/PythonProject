<div class="content-display-right content-display-height scrollable-table">
    <table id="device_table">
        <thead>
            <tr>
                <th>Hostname</th>
                <th>IP</th>
                <th>MAC</th>
                <th>Status</th>
                <th>Scan for Ports</th>
                <th>Available Ports</th>
                <th>Launch DDOS</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
            </tr>
        </tbody>
    </table>
</div>

<script>
function fetchDataAndUpdateTable() {
    $.getJSON('php/get_network_devices.php', function (data) {
        if (data.length > 0) {
            // Assuming the tbody has the ID 'device_table_body'
            var tableBody = $('#device_table tbody');

            // Clear existing rows
            tableBody.empty();

            // Append new rows based on fetched data
            data.forEach(function (row) {
                var newRow = $('<tr>');
                newRow.append('<td>' + row.dtHostname + '</td>');
                newRow.append('<td>' + row.dtIP + '</td>');
                newRow.append('<td>' + row.dtMAC + '</td>');

                // Conditionally append green or red LED based on Status
                if (row.dtStatus === 'Online') {
                    newRow.append('<td><div class="led-green"></div></td>');
                } else {
                    newRow.append('<td><div class="led-red"></div></td>');
                }

                // Add "Scan" button with an event listener
                newRow.append('<td><button class="scan-button">Scan</button></td>');
                newRow.find('.scan-button').on('click', function () {
                    // Trigger Nmap scan when the button is clicked
                    performNmapScan(row.dtIP);
                });

                // Add select box and "Play" button
                newRow.append('<td><select class="port-select"></select></td>');
                newRow.append('<td><button class="play-button">Play</button></td>');
                // Append the new row to the table body
                tableBody.append(newRow);
            });
            <?php $_SESSION["ready"] = "Yes"; ?>
        }
    });
}

function performNmapScan(ip) {
    // Assuming you have a PHP script to handle the execution of the Python script
    $.ajax({
        url: 'php/get_ports.php',
        method: 'POST',
        data: { ip: ip },
        success: function (scanResults) {
            // Display the scan results in the select box
            displayScanResults(ip, scanResults);
        },
        error: function () {
            alert('Error executing Nmap scan.');
        }
    });
}

function displayScanResults(ip, scanResults) {
    // Find the select box associated with the given IP
    var selectBox = $('tr').filter(function () {
        return $(this).find('td:eq(1)').text() == ip;
    }).find('.port-select');

    // Clear existing options
    selectBox.empty();

    // Parse the JSON-encoded response
    console.log('Raw Response:', scanResults);
    var response = JSON.parse(scanResults);
    console.log('Extracted Open Ports:', response);
    // Extract the open ports array
    var openPorts = response;
    // Create options based on openPorts
    if (openPorts.length > 0) {
        openPorts.sort(function (a, b) { return b - a; });  // Sort in descending order
        openPorts.forEach(function (port) {
            selectBox.append('<option value="' + port + '">' + port + '</option>');
        });
    } else {
        selectBox.append('<option>No ports available</option>');
    }
}

// Add event listener for "Play" button
$(document).on('click', '.play-button', function () {
    var ip = $(this).closest('tr').find('td:eq(1)').text(); // Get the IP address from the row

    // Get the selected port from the dropdown list
    var selectedPort = $(this).closest('tr').find('.port-select').val();

    // Prompt the user for the duration
    var enteredDuration = prompt("Enter the duration in seconds (default is 1 minute):") || 1;

    // Execute the Python script with the selected port and entered duration
    $.ajax({
        url: 'php/execute_ddos.php',
        method: 'POST',
        data: { ip: ip, port: selectedPort, duration: enteredDuration },
        success: function (response) {
            //alert("DDos success"); // Display the response from the server
        },
        error: function () {
            alert('Error executing play script.');
        }
    });
});


// Call fetchDataAndUpdateTable on page load
$(document).ready(function () {
    fetchDataAndUpdateTable();
});
</script>
