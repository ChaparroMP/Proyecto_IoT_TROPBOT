<?php
        // El método de solicitud POST solicita que el servidor acepte los datos
	$firstName = $_POST['firstName'];
	$lastName = $_POST['lastName'];
	$email = $_POST['email'];
	$password = $_POST['password'];
        
        // Encriptación de la contraseña del usuario
        $password = hash('sha512', $password);
        
        

	// Database connection
	$conn = new mysqli('fdb31.125mb.com','3949963_signup','1234TROPBOT','3949963_signup');
	//query para asegurar que los datos se almacenan en el orden especificado
        $query = "INSERT INTO registration(firstName, lastName, email, password)
          VALUES('$firstName' , '$lastName', '$email', '$password')";
        // verificación del correo electronico  
        $verificacion_correo = mysqli_query($conn, "SELECT * FROM registrtion WHERE email = '$email'");
        
        // envio de mensaje en caso de que ya se haya usado un email
        if(mysqli_num_rows($verificacion_correo) > 0){ // 
            echo'
                <script>
                    alert("Este correo electronico ya está registrado, intenta con otro");
                    window.location = "signup.html";
                    </script>
            ';
            exit();
        }
        // se ejecuta el query
        $ejecutar = mysqli_query($conn, $query);
        
        // envio de mensaje en caso de que que el resgistro sea exitoso
        if($ejecutar){   // 
            echo '
                <script>
                    alert("Regístro exitoso");
                    window.location = "signin.html";
                </script>
            ';
        }
        // envio de mensaje en caso de que el registro haya fallado
        else{ // 
            echo '
                <script>
                    alert("Regístro fallido, intentalo de nuevo");
                    window.location = "signup.html";
                </script>
            ';    
        }
        
        // envio de mensaje en caso de que haya un fallo durante la conexión
        if($conn->connect_error){
		echo "$conn->connect_error";
		die("Connection Failed : ". $conn->connect_error);
	}
        // envio de mensaje en caso de que el registro sea exitoso
        else{
                $stmt = $conn->prepare("insert into registration(firstName, lastName, email, password) values(?, ?, ?, ?)");
                $stmt->bind_param("ssss", $firstName, $lastName, $email, $password);
                $execval = $stmt->execute();
                echo $execval;
                echo '
                        <script>
                            alert("Registro exitoso...");
                            window.location = "signin.html";
                        </script>
                    ';
                $stmt->close();
                // se cierra la conexión con la base de datos
                $conn->close();                
               
                   
	}
?>