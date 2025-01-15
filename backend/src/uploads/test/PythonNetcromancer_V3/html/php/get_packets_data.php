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

// Check if the session variable exists
if ($_SESSION['latestIdPacket'] == "") {
    $sqlLatestId = "SELECT idPacket FROM tblPacket ORDER BY idPacket DESC LIMIT 1";
    $stmtLatestId = $conn->prepare($sqlLatestId);
    $stmtLatestId->execute();

    $resultLatestId = $stmtLatestId->get_result();

    // Fetch the result from the mysqli_result object
    $rowLatestId = $resultLatestId->fetch_assoc();
    $latestIdPacket = $rowLatestId['idPacket'];

    // Store the latest ID in the session
    $_SESSION['latestIdPacket'] = $latestIdPacket;
}
// Get the saved ID from the session or default to 0
$savedId = $_SESSION['latestIdPacket'];
// Use prepared statement to prevent SQL injection
$sql = "SELECT * FROM tblPacket WHERE idPacket > ? ORDER BY idPacket ASC";
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $savedId);
$stmt->execute();

$result = $stmt->get_result();

$data = array();

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $data[] = $row;
    // Update the saved ID with the ID of the newest entry
    //$_SESSION['latestIdPacket'] = end($data)['idPacket'];
    }
    echo json_encode($data);
}
?>