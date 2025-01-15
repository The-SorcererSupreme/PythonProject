<?php
// execute_nmap.php

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $ip = $_POST['ip'];

    // Use exec to execute the Python script with the IP address as a parameter
    exec("python3 ../nmap_scan.py $ip", $output, $returnCode);

    if ($returnCode === 0) {
        // If the execution was successful, parse the output as JSON
        $jsonOutput = json_decode($output[0]);

        if ($jsonOutput !== null) {
            // If the output is a valid JSON, send it back to JavaScript
            echo json_encode($jsonOutput);
        } else {
            // If the output is not valid JSON, treat it as a string and send as is
            echo $output[0];
        }
    } else {
        // If there was an error, return an error message
        echo json_encode(['error' => 'Error executing Nmap scan.']);
    }
} else {
    // Return an error if the request method is not POST
    echo json_encode(['error' => 'Invalid request method.']);
}
?>
