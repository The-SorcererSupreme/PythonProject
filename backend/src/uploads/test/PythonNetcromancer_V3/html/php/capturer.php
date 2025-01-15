<div id="loadedContent" style="display: none;">
  <div>
  <label for="nmask">Networkmask:</label>
  <input type="text" id="nmask" name="nmask" value="10.0.3.0/24">
  <label for="proto">Protocol:</label>
  <input type="text" id="proto" name="proto">
  <button onclick="runPythonScript()">Capture!</button>
</div>


<div id="output-container">
        <!-- Output from Python script will be displayed here -->
</div>

<script>
  function runPythonScript() {
    // Get the input from the textarea
    var nmask = $("#nmask").val();
    var proto = $("#proto").val();
    // Send an AJAX request to the server
    $.ajax({
        type: "POST",
        url: "php/run_python_script.php",
        data: { nmask: nmask, proto: proto },  // Include nmask and proto as parameters
        success: function(response) {
          // Update the output container with the response from the server
          $("#output-container").html(response);
        }
      });
    }
</script>
</div>
<?php
session_start();
$_SESSION["ready"] = "Yes";
?>