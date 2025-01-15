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
$sql = "SELECT * FROM tblHosts";
$stmt = $conn->prepare($sql);
$stmt->execute();

$result = $stmt->get_result();

$data = array();

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
    echo json_encode($data);
}
?>
