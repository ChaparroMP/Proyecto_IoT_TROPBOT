<?php
session_start();

session_unset();

session_destroy();

header('Location:http://tropbot-iot21.125mb.com/usersLogin/login.php');
?>