<?php
    $server = 'fdb31.125mb.com';
    $username = '3949963_usuariostrop';
    $password = 'TROPBOT5479_IoT';
    $database = '3949963_usuariostrop';
    
    try {
      $conn = new PDO("mysql:host=$server;dbname=$database;", $username, $password);
    } catch (PDOException $e) {
      die('Connection Failed: ' . $e->getMessage());
    }

?>

