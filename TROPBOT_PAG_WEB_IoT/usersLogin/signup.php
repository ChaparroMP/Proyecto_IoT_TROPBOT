<?php

 if (!empty($_POST['firstName']) && !empty($_POST['lastName']) && !empty($_POST['email']) && !empty($_POST['password']) && !empty($_POST['check_password'])) { /*Verificar que no este vacío*/
 
        //Verificación de no repetición de correo
        $conexion = mysqli_connect("fdb31.125mb.com", "3949963_usuariostrop", "TROPBOT5479_IoT", "3949963_usuariostrop");
        $Email = $_POST['email'];
        $verifyEmail= mysqli_query($conexion, "SELECT * FROM prueba_login WHERE email ='$Email'"); 
        
        
        if (!empty($verifyEmail) AND mysqli_num_rows($verifyEmail) > 0){
            echo '
              <script>
                 alert("La dirección de correo ya está registrada.");
                 window.location = "../usersLogin/signup.php";
              </script>';
              exit();
        }
        elseif(!filter_var($_POST['email'], FILTER_VALIDATE_EMAIL)) {
        
           // invalid emailaddress
           echo '
              <script>
                 alert("La dirección de correo es INVÁLIDA.");
                 window.location = "../usersLogin/signup.php";
              </script>';
              exit();
        }
        
        else{
           require 'database.php';
           
            if ($_POST['password'] != $_POST['check_password']) {
                 // error de coincidencia de contraseñas
                 echo '
                 <script>
                    alert("Confirmar contraseña y contraseña no coinciden. Por favor, escriba cuidadosamente.");
                    window.location = "../usersLogin/signup.php";
                 </script>';
                 exit();
            }
            
            // Validate password strength
            $uppercase = preg_match('@[A-Z]@', $_POST['password']);
            $lowercase = preg_match('@[a-z]@', $_POST['password']);
            $number    = preg_match('@[0-9]@', $_POST['password']);
            $specialChars = preg_match('@[^\w]@', $_POST['password']);
            
                
            if(!$uppercase || !$lowercase || !$number || !$specialChars || strlen($password) < 8) {
                 echo '
                 <script>
                    alert("La CONTRASEÑA debe tener al menos una longitud de 8 caracteres, incluir al menos una mayúscula, un número y un carácter especial (# @ $ !  % ^ & * - < > |  \).");
                    window.location = "../usersLogin/signup.php";
                 </script>';
                 exit();
            }
            
            
            else{
                $sql = "INSERT INTO prueba_login (firstName, lastName, email, password,check_password) VALUES (:firstName, :lastName, :email, :password,:check_password)";
                $stmt = $conn->prepare($sql);
                $stmt->bindParam(':firstName', $_POST['firstName']);
                $stmt->bindParam(':lastName', $_POST['lastName']);
                $stmt->bindParam(':email', $_POST['email']);
                /*Se hace cifrado de la contraseña que se recibe del formulario*/
                $password = password_hash($_POST['password'], PASSWORD_BCRYPT);
                $password_check = password_hash($_POST['check_password'], PASSWORD_BCRYPT);
                /*Alamacena en la base de datos la contraseña ya cifrada*/
                $stmt->bindParam(':password', $password);
                $stmt->bindParam(':check_password', $password_check);
                
                if ($stmt->execute()) {
                   echo '
                   <script>
                     alert("Usuario creado exitosamente.");
                     window.location = "../usersLogin/login.php";
                   </script>';
                   exit();
                        
                } else {
                   echo '
                   <script>
                      alert("Se ha presentado un problema al crear tu usuario, por favor inténtalo de nuevo.");
                      window.location = "../usersLogin/signup.php";
                   </script>';
                   exit();
                } 
                
            }

        }
 }

?>



<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta content="width=device-width, initial-scale=1.0" name="viewport">

  <title>TROPBOT &amp; Porque sabemos que amas tu cultivo | Registrarse  </title>
  <meta content="" name="descriptison">
  <meta content="" name="keywords">

   <!-- Favicon -->
  <link rel="shortcut icon" href="../img/core-img/logo.png" type="image/x-icon">
  <!-- Custom styles -->
  <link rel="stylesheet" href="./css/style.min.css">
  <!-- Favicon -->
  <link rel="icon" href="../img/core-img/favicon.png">
  
</head>

  <body>
    
    <div class="layer"></div>
    
    <main class="page-center">
          <article class="sign-up">
            <h1 class="sign-up__title">Inicia la aventura con TROPBOT</h1>
            <p class="sign-up__subtitle">Empieza monitoreando tus cultivos para evitar posibles afectaciones</p>
            

            <!-- Formulario para obtener los datos del registro de los usuarios nuevos -->
            <form class="sign-up-form form" action="signup.php" method="post">
            <!-- Espacios para ingresar la información que se solicita al usuario (Nombre, apellidos, email y contraseña) -->
              <label class="form-label-wrapper">
                <p class="form-label">Nombres</p>
                <input class="form-input" type="text" placeholder="Ingresa tus nombres" name="firstName" required>
              </label>
              <label class="form-label-wrapper">
                <p class="form-label">Apellidos</p>
                <input class="form-input" type="text" placeholder="Ingresa tus apellidos" name="lastName" required>
              </label>
              <label class="form-label-wrapper">
                <p class="form-label">Correo</p>
                <input class="form-input" type="email" placeholder="Ingresa tu correo electrónico" name="email" required>
              </label>
              <label class="form-label-wrapper">
                <p class="form-label">Contraseña</p>
                <input class="form-input" type="password" placeholder="Ingresa tu contraseña" name="password" required>
              </label>
              <label class="form-label-wrapper">
                <p class="form-label">Confirmar Contraseña</p>
                <input class="form-input" type="password" placeholder="Vuelve a escribir tu contraseña" name="check_password" required>
              </label>
              <!-- Hipervinculo para ir a la página de inicio de sesión -->
              <a class="link-info forget-link" href="login.php">Iniciar Sesión</a>
              <!-- Botón para registrar los datos del usurios -->
              <button class="form-btn primary-default-btn transparent-btn">Registrarse</button>
              <!-- Hipervinculo para regresar a la página principal -->
              <a class="link-info forget-link" href="../index.html">Volver a Inicio</a>
             
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