<?php
session_start();
//include('php/sql_link.php');
$servername = "localhost";
$username = "dbuser";
$password = "vv2j@&T2zax@HhApm2";
$dbname = "sqlinthesky";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Get the saved ID from the session or default to 0
$session = $_SESSION['latestId'];
$savedId = (int)$session;
// Use prepared statement to prevent SQL injection
$sql = "SELECT idData, dtIncoming, dtOutgoing, dtTimestamp FROM tblThroughput WHERE idData > ? ORDER BY idData ASC";
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $savedId);
$stmt->execute();

$result = $stmt->get_result();

$data = array();

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $data[] = $row;
    }

    // Update the saved ID with the ID of the newest entry
    $_SESSION['latestId'] = end($data)['idData'];
}

echo json_encode($data);
?>