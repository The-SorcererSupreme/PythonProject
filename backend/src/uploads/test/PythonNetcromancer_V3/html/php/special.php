<?php
session_start();
$_SESSION["ready"] = "Yes";
?>
<div id="loadedContent">
<div id="shellContainer">
    <pre id="shellOutput"><?php
    // Display previous output if available
    $output_file = '/var/www/html/php/output.txt';
    if (file_exists($output_file)) {
        echo htmlspecialchars(file_get_contents($output_file));
    }
    ?></pre>
    <form id="shellForm">
        <span id="prompt"><?php echo $_SESSION["user"] . "@" . $_SESSION["host"] . ":" . $_SESSION["pwd"] . "$"; ?></span>
        <input type="text" id="command" name="command" autofocus>
        <input type="hidden" id="username" name="username" value="<?php echo $_SESSION['user']; ?>">
        <input type="hidden" id="password" name="password" value="<?php echo $_SESSION['password']; ?>">
        <input type="submit" value="Execute" style="display:none;">
    </form> 
</div>
</div>

<style>
#shellContainer {
    background-color: black;
    color: white;
    font-family: monospace;
    padding: 10px;
    height: 100%;
    overflow-y: scroll;
    grid-column-start: 1;
    grid-column-end: 3;
}

#shellOutput {
    white-space: pre-wrap;
    word-wrap: break-word;
}

#prompt {
    color: lightgreen;
}

#command {
    background-color: black;
    color: white;
    border: none;
    outline: none;
    width: 90%;
}
</style>

<script>
document.getElementById('shellForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var command = document.getElementById('command').value;
    if (command) {
        var username = document.getElementById('username').value;
        var password = document.getElementById('password').value;
        
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'execute_command.py', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onload = function() {
            if (xhr.status === 200) {
                var output = document.getElementById('shellOutput');
                var shellContainer = document.getElementById('shellContainer');
                output.innerHTML += document.getElementById('prompt').textContent + ' ' + command + '\n';
                output.innerHTML += xhr.responseText + '\n';
                document.getElementById('command').value = '';
                shellContainer.scrollTop = shellContainer.scrollHeight; // Scroll to the bottom
            }
        };
        xhr.send('command=' + encodeURIComponent(command) + '&username=' + encodeURIComponent(username) + '&password=' + encodeURIComponent(password));
    }
});
</script>
