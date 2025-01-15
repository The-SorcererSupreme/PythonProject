<?php
session_start();
$_SESSION['capturing'] = false;
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get the input from the AJAX request
    $nmask = $_POST['nmask'];
    $proto = $_POST['proto'];

    // Check the session variable to determine the state
    if (!isset($_SESSION['capturing']) || $_SESSION['capturing'] === false) {
        // Connect to the Python script using a socket
        $socket = socket_create(AF_INET, SOCK_STREAM, 0);
        socket_connect($socket, '127.0.0.1', 12345);  // Use the same port number as in the Python script

        // Send network mask and protocol to the Python script
        $command = "$nmask $proto";
        socket_write($socket, $command, strlen($command));

        // Read the signal from the Python script
        $signal = socket_read($socket, 1024);

        if ($signal === "READY") {
            // Send the new payload to the Python script
            $newPayload = $_POST['newPayload'];
            socket_write($socket, $newPayload, strlen($newPayload));

            // Read and display the output from the Python script
            $output = socket_read($socket, 4096);  // Adjust buffer size as needed

            // Set the session variable to indicate capturing is in progress
            $_SESSION['capturing'] = true;
        } else {
            $output = "Failed to receive signal from Python script.";
        }

        // Close the socket
        socket_close($socket);
    } else {
        // If capturing is in progress, send a message to the client
        $output = "Capturing is already in progress.";
    }

    // Return the output to the client (your JavaScript function)
    echo "<pre>$output</pre>";
}
?>
