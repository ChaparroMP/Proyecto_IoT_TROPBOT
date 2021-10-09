<?php
        // El método de solicitud POST solicita que el servidor acepte los datos
	$email = $_POST['email'];
	$password = $_POST['password'];
        
        $password = hash('sha512', $password);

	// Database connection
	$conn = new mysqli('fdb31.125mb.com','3949963_signup','1234TROPBOT','3949963_signup');
        // envio de mensaje en caso de que haya un fallo durante la conexión
        
        if($conn->connect_error){
		echo "$conn->connect_error";
		die("Connection Failed : ". $conn->connect_error);
	}
        // envio de mensaje en caso de que el ingreso sea exitoso
        else {
		$stmt = $conn->prepare("insert into sign_in(email, password) values(?, ?)");
		$stmt->bind_param("ss", $email, $password);
		$execval = $stmt->execute();
		echo $execval;
		
                echo '
                        <script>
                            alert("Ingreso exitoso...");
                            window.location = "index.html";
                        </script>
                    ';
		$stmt->close();
                // se cierra la conexión con la base de datos
		$conn->close();
	}
?>