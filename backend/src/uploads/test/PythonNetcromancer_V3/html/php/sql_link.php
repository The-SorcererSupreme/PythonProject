<?php
// Assuming you have a database connection established
$servername = "localhost";
$username = "dbuser";
$password = "vv2j@&T2zax@HhApm2";
$dbname = "sqlinthesky";

$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>