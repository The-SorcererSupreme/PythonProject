<?php
session_start();
$_SESSION["ready"] = "Yes";

// Handle form submission
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST['login'])) {
        // Handle login button
        $username = $_POST['username'];
        $password = $_POST['password'];

        // Call Python script to authenticate via SSH
        $command = "python3 authenticate_user.py " . escapeshellarg($username) . " " . escapeshellarg($password);
        $output = shell_exec($command);
        // Check Python script output
        if (strpos($output, "Authentication successful") !== false) {
            // Extract hostname from the output
            if (preg_match('/Hostname: (.+)/', $output, $matches)) {
                $hostname = $matches[1];
                $_SESSION['host'] = $hostname;
            }
            $_SESSION['user'] = $username;
            $_SESSION['password'] = $password;
            $_SESSION['authenticated'] = true;
            $_SESSION['pwd'] = '/home/' . $username; // Adjust as per your system setup
            header("Location: index.php");
            exit();
        } else {
            $error = "SSH Authentication failed";
        }
    } elseif (isset($_POST['guest'])) {
        // Handle guest login button (if needed)
        // Example: You can handle guest login separately or remove this block
        $error = "Guest login is not supported in this example.";
    }
}
?>

<div id="loadedContent">
    <?php if (isset($error)) echo "<p>$error</p>"; ?>
    <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username"><br><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password"><br><br>
        <button type="submit" name="login" value="login">Login</button>
    </form>
</div>
