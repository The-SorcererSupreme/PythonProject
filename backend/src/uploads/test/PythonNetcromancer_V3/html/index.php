<!DOCTYPE html>
<html>
<head>
    <?php
    include('php/head.php');
    session_start();
    if (isset($_GET['page'])) {
        // Update the session variable based on the 'page' parameter
        $_SESSION['page'] = $_GET['page'];
    }
    ?>
</head>

<body>
    <div class="container">
        <?php include('php/header.php')?>
        <?php include('php/nav.php'); ?>
        <div id="content"  class="grid-content">
            <!-- Always include the loading screen -->
            <?php include('php/loading_screen.php'); ?>
            <?php
            // Redirect to login page if not authenticated
            if (!isset($_SESSION['authenticated'])) {
                $_SESSION['latestIdPacket']="";
                include("php/login.php");
            } else{
            // Load content based on the 'page' parameter
            switch ($_SESSION['page']) {
                case 'dashboard':
                    $_SESSION['latestIdPacket']="";
                    include('php/dashboard.php');
                    break;
                case 'sniffer':
                    $_SESSION['latestIdPacket']="";
                    include('php/sniffer.php');
                    break;
                case 'capturer':
                    $_SESSION['latestIdPacket']="";
                    include('php/capturer.php');
                    break;
                case 'special':
                    $_SESSION['latestIdPacket']="";
                    include('php/special.php');
                    break;
                default:
                    // Default to the dashboard if the page is not recognized
                    include('php/dashboard.php');
                    break;
            }
        }
            ?>
        </div>

        <script>
        document.addEventListener('DOMContentLoaded', function() {
            var checkReadyInterval = setInterval(function() {
                if ('<?php echo $_SESSION["ready"]; ?>' === 'Yes') {
                    clearInterval(checkReadyInterval);
                    document.getElementById('loadingScreen').style.display = 'none';
                    document.getElementById('loadedContent').style.display = 'grid';
                    <?php $_SESSION["ready"] = ""; ?>
                }
            }, 1000);
        });
        </script>
        <footer class="grid-footer">
        </footer>
    </div>
</body>
</html>
