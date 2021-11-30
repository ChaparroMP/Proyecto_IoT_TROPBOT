<?php
// login.php

session_start();


if (isset($_SESSION['login_sess'])) {
    header('Location: /usersLogin/dashboard.php');
}

// Include config file
require_once "database.php";

if (!empty($_POST['email']) && !empty($_POST['password'])) {
    /*Consulta a la base de datos*/
    $records = $conn->prepare('SELECT id, firstName, lastName, email, password FROM prueba_login WHERE email = :email');
    /*Obtener y vincular parametro de email*/   
    $records->bindParam(':email', $_POST['email']);
    $records->execute();
    /*Se tienen los datos del usuario*/
    $results = $records->fetch(PDO::FETCH_ASSOC);
    
    if (($results!= 0) && password_verify($_POST['password'], $results['password'])) {
      /*variables de sesión*/
      $_SESSION['login_sess'] = $results['id'];
      echo '
         <script>
            alert("¡BIENVENIDO!");
            window.location = "http://tropbot-iot21.125mb.com/usersLogin/login.php";
         </script>';
      exit();
      
    } else {
       echo '
         <script>
            alert("Usuario no encontrado o contraseña incorrecta.");
            window.location = "http://tropbot-iot21.125mb.com/usersLogin/logout.php";
         </script>';
       exit();
    }
  }

?>


<!DOCTYPE html>
<html>
  <head>
  <meta charset="utf-8">
  <meta content="width=device-width, initial-scale=1.0" name="viewport">

  <title>TROPBOT &amp; Porque sabemos que amas tu cultivo  | Iniciar Sesión </title>
  <meta content="" name="descriptison">
  <meta content="" name="keywords">
  
   <!-- Favicon -->
  <link rel="icon" href="../img/core-img/favicon.png">
  
  
  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,300i,400,400i,600,600i,700,700i|Raleway:300,300i,400,400i,500,500i,600,600i,700,700i|Poppins:300,300i,400,400i,500,500i,600,600i,700,700i" rel="stylesheet">

    
  <!-- Custom styles -->
  <link rel="stylesheet" href="./css/style.min.css">

  </head>
  
  
  <body>

        <main class="page-center">
          <article class="sign-up">
            <h1 class="sign-up__title">¡Bienvenido de nuevo!</h1>
            <p class="sign-up__subtitle">Ingresa a tu cuenta para continuar</p>
            <!-- Formulario para ingresar las credenciales del usuario e iniciar sesión -->
            <form class="sign-up-form form" action="login.php" method="post">
            
              <label class="form-label-wrapper">
                <p class="form-label">Correo</p>
                <input class="form-input" type="email" placeholder="Ingresa tu correo electrónico" name="email" required>
              </label>
              <label class="form-label-wrapper">
                <p class="form-label">Contraseña</p>
                <input class="form-input" type="password" placeholder="Ingresa tu contraseña" name="password" required>
              </label>
              <!-- Hipervinculo para ir a la página de registro en caso que el usuario no haya realizado este paso -->
              <a class="link-info forget-link" href="signup.php">Registrarse</a>
              
              <!-- Botón para ingresar a la página de usuario -->
              <button class="form-btn primary-default-btn transparent-btn">Ingresar</button>
              <!-- Hipervinculo para regresar a la página principal -->
              <!-- se agrega el tipo y el nombre del botón -->
              <a type="submit" name="login-submit" class="link-info forget-link" href="../index.html">Volver a Inicio</a>
            </form>
          </article>
        </main>
        
                
<!-- Chart library -->
<script src="./plugins/chart.min.js"></script>
<!-- Icons library -->
<script src="plugins/feather.min.js"></script>
<!-- Custom scripts -->
<script src="js/script.js"></script>
</body>
   
</html>
