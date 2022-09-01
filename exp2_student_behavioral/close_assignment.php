<?php

// Path to config file
include('database_config.php');

try {
    // $conn = new mysqli($servername, $username, $password, $dbname);
    $conn = new PDO("mysql:host=$servername;port=$port;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // read params from post
    $student_id = $_POST['student_id'];
    $worker_id = $_POST['worker_id'];

    // remove participant from 'assigned' column, regardless of outcome
    $update_query = "UPDATE student_assignments_v2 SET assigned = assigned - 1 WHERE student_id = " . $student_id;
    $updated_result=$conn->query($update_query);

    // if task completed successfully, add to 'completed' column
    if (isset($_POST["completed"])) {
        $complete_query = "UPDATE student_assignments_v2 SET completed = completed + 1 WHERE student_id = " . $student_id;
        $complete_result=$conn->query($complete_query);
    }

    echo '{"success": true, "completed":' . $completed . '}';
} catch(PDOException $e) {
    echo '{"success": false, "message": ' . $e->getMessage();
}
  
// Close connection
$conn = null;

?>