<?php

// Path to config file
include('database_config.php');

// Connect to database
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

try {
  // Search available conditions from database
  $student_query = "SELECT * FROM student_assignments_v2 WHERE completed=0 AND assigned=0 LIMIT 1";
  $result = $conn->query($student_query);
  $row = $result->fetch_assoc();

  // Mark entry as assigned
  $student_id = $row['student_id'];
  $worker_id = $data_array[0]['worker_id'];

  $assign_query="UPDATE student_assignments_v2 SET assigned = assigned + 1 WHERE student_id = " . $student_id;
  $assign_result=$conn->query($assign_query);

  // DATA TO BE SENT
  echo '{"success": true, "message": "", "data":'.json_encode($row).'}';

} catch (mysqli_sql_exception $e) {
  echo '{"success": false, "data": null, "message": ' . $e->getMessage();
}

// Close connection
$conn->close();
?>