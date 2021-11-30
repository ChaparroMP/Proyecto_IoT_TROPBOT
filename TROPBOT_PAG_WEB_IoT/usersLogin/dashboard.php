<?php
// Solo se permite el ingreso con el inicio de sesion.
session_start();
// Si el usuario no se ha logueado se le regresa al inicio.
if (!isset($_SESSION['login_sess'])) {
   echo '
     <script>
        alert("Por favor, inicie sesión primero para ver esta página.");
        window.location = "http://tropbot-iot21.125mb.com/usersLogin/logout.php";
     </script>';
     exit();
	
}

?>


<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TROPBOT &amp; Porque sabemos que amas tu cultivo  | Dashboard</title>
  <!-- Favicon -->
  <link rel="shortcut icon" href="../img/core-img/favicon.png" type="image/x-icon">
  <!-- ////////////////////////////////////////////////////////////////////////////////////////////-->
   <!-- Font Awesome Icons -->
  <link rel="stylesheet" href="charts/plugins/fontawesome-free/css/all.min.css">
   <!-- Theme style -->
  <link rel="stylesheet" href="charts/dist/css/adminlte.min.css">
  <!-- Custom styles -->
  <link rel="stylesheet" href="./css/style.css">
</head>

<body>
  <div class="layer"></div>
<!-- ! Body -->
<a class="skip-link sr-only" href="#skip-target">Skip to content</a>
<div class="page-flex">
 <!-- ! Sidebar -->
  <aside class="sidebar">
    <div class="sidebar-start">
        <div class="sidebar-head">
            <a href="/usersLogin/dashboard.php" class="logo-wrapper" title="Home">
                <span class="sr-only">Home</span>
                <span class="icon logo" aria-hidden="true"></span>
                <div class="logo-text">
                    <span class="logo-title">TROPBOT</span>
                    <span class="logo-subtitle"><p>Monitorea tu cultivo <br></p></span>
                </div>
            </a>
            <button class="sidebar-toggle transparent-btn" title="Menu" type="button">
                <span class="sr-only">Toggle menu</span>
                <span class="icon menu-toggle" aria-hidden="true"></span>
            </button>
        </div>
        <div class="sidebar-body">
            <ul class="sidebar-body-menu">
                <li>
                    <a class="active" href="/usersLogin/dashboard.php"><span class="icon home" aria-hidden="true"></span>
                    <p>Página Principal</p></a>
                </li>
                
            </ul>
            <span class="system-menu__title">Datos</span>
            <ul class="sidebar-body-menu">
                <li>
                    <a href="/usersLogin/data_sensores.php"> 
                        <p>  <span class="icon document" aria-hidden="true"></span> Temperatura <br>Ambiente <br>
                        <br> <span class="icon folder" aria-hidden="true"></span>
                        Humedad Relativa <br>del aire<br>
                        <br> <span class="icon image" aria-hidden="true"></span>Radiación Solar e Iluminación Ambiente</p>
                    </a> 
                        
                </li>
            </ul>
            <span class="system-menu__title">Actuador (Motores)</span>
            <ul class="sidebar-body-menu">
                <li>
                    <a href="/usersLogin/data_prox.php"><span class="icon paper" aria-hidden="true"></span>Proximidad</a> 
                        
                </li>
            </ul>
            <ul class="sidebar-body-menu">
                <li>
                    <a class="show-cat-btn" href="##">
                        <span  class="system-menu__title" aria-hidden="true"></span>Descargas
                        <span class="category__btn transparent-btn" title="Open list">
                            <span class="sr-only">Open list</span>
                            <span class="icon arrow-down" aria-hidden="true"></span>
                        </span>
                    </a>
                    <ul class="cat-sub-menu">
                        
                    </ul>
                </li>
            </ul>

        </div>
    </div>
    <div class="sidebar-footer">
        <a href="https://www.dropbox.com/sh/enowgqeojr058ir/AAAiA7FOrlkQXJC_YmmOfFtUa?dl=0" class="sidebar-user">
            <span class="sidebar-user-img">
                <img src="/usersLogin/img/svg/Icon_download.svg" alt="User name">
            </span>
            <div class="sidebar-user-info">
                <span class="sidebar-user__title"> Obtener info.</span>
                <span class="sidebar-user__subtitle">en formato csv</span>
            </div>
       </a>
    </div>
  </aside>
  <div class="main-wrapper">
    <!-- ! Main nav -->
    <nav class="main-nav--bg">
  <div class="container main-nav">
    <div class="main-nav-start"></div>
    
    <div class="main-nav-end">
      <button class="sidebar-toggle transparent-btn" title="Menu" type="button">
        <span class="sr-only">Toggle menu</span>
        <span class="icon menu-toggle--gray" aria-hidden="true"></span>
      </button>
     
      <button class="theme-switcher gray-circle-btn" type="button" title="Switch theme">
        <span class="sr-only">Switch theme</span>
        <i class="sun-icon" data-feather="sun" aria-hidden="true"></i>
        <i class="moon-icon" data-feather="moon" aria-hidden="true"></i>
      </button>
      
      <div class="nav-user-wrapper">
        <button href="##" class="nav-user-btn dropdown-btn" title="My profile" type="button">
          <span class="sr-only">My profile</span>
          <span class="nav-user-img">
            <img src="./img/avatar/avatar-illustrated-02.png" alt="User name">
          </span>
        </button>
        <ul class="users-item-dropdown nav-user-dropdown dropdown">
          <li><a class="danger" href="logout.php">
              <i data-feather="log-out" aria-hidden="true"></i>
              <span>Cerrar Sesión</span>
              </a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</nav>
    <!-- ! Main -->
<main class="main users chart-page" id="skip-target">
    <div class="container">
      <h2 class="main-title">Bienvenid@</h2>
      <div class="col-lg-12">
         <article class="white-block">
              En tu dashboard de TROPBOT podrás encontrar:
         </article>
      </div>
      <div class="row stat-cards">
        <div class="col-md-6 col-xl-4">
          <article class="stat-cards-item">
            <div class="stat-cards-icon primary">
              <i data-feather="bar-chart-2" aria-hidden="true"></i>
            </div>
            <div class="stat-cards-info">
              <p class="stat-cards-info__num">1.	Podrás ver el reporte actual de cada uno de los datos tomados por la plataforma. </p>
              <p class="stat-cards-info__title">(Temperatura, Humedad Relativa del aire y Radiación e Iluminación Solar)
              </p>
            </div>
          </article>
        </div>
       <div class="col-md-6 col-xl-4">
          <article class="stat-cards-item">
            <div class="stat-cards-icon warning">
              <i data-feather="bar-chart-2" aria-hidden="true"></i>
            </div>
            <div class="stat-cards-info">
              <p class="stat-cards-info__num">2.	Cada reporte contiene una gráfica de los últimos datos.  </p>
              <p class="stat-cards-info__title">Cada gráfica tiene un umbral máximo y mínimo para que se reconozca si hay niveles que puedan ser dañinos para su cultivo.
              </p>
            </div>
          </article>
        </div>
        <div class="col-md-6 col-xl-4">
          <article class="stat-cards-item">
            <div class="stat-cards-icon purple">
              <i data-feather="file" aria-hidden="true"></i>
            </div>
             <div class="stat-cards-info">
              <p class="stat-cards-info__num">3.	La gráfica esta divida por regiones (verde y blanca) que indican agrupaciones de datos de GPS. </p>
              <p class="stat-cards-info__title">De esta forma el usuario conoce en que punto exacto se toma una medición. 
              </p>
            </div>
          </article>
        </div>
        
      </div>

       <div class="col-lg-12"></div>
       <div class="col-lg-12"></div>
       <div class="col-lg-12"></div>
       <div class="col-lg-12"></div>
       <div class="col-lg-12"></div>
       <div class="col-lg-12"></div>
      
      <div class="row stat-cards">
        <div class="col-md-6 col-xl-6">
          <article class="stat-cards-item">
            <div class="stat-cards-icon primary">
              <i data-feather="bar-chart-2" aria-hidden="true"></i>
            </div>
            <div class="stat-cards-info">
              <p class="stat-cards-info__num">4.	Cada medida contiene además los valores medios, máximos y mínimos, para conocer el estado diario general de tu cultivo. </p>
              <p class="stat-cards-info__title">También tiene una alerta que indica si el cultivo está en niveles sanos en base a los umbrales de las gráficas.</p>
             
            </div>
          </article>
        </div>
        <div class="col-md-6 col-xl-6">
          <article class="stat-cards-item">
            <div class="stat-cards-icon warning">
              <i data-feather="file" aria-hidden="true"></i>
            </div>
            <div class="stat-cards-info">
              <p class="stat-cards-info__num">5.	Al final de la página descarga los datos tomados.</p>
              <p class="stat-cards-info__title">Por recorrido o el histórico completo en formato CSV.</p>
              
            </div>
          </article>
        </div>
      </div>
      
      <div class="col-lg-12"></div>
      <div class="col-lg-12"></div>
      <div class="col-lg-12"></div>
      <div class="col-lg-12"></div>
      <div class="col-lg-12"></div>
      <div class="col-lg-12"></div>
         
      <div class="row">
        
        <div class="col-lg-6">
           <!-- VIDEO Content Area -->
          <iframe width="560" height="315" src="https://www.youtube.com/embed/OWV_B5Q9NdE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
          
        </div>
        
         <div class="col-lg-6">
              
              <article class="white-block">
                 <center>
                    <img src="/usersLogin/img/control.png" alt="Descripción de la imagen">
                 </center>
              </article>
        </div>
      
      </div>
    </div>
</main>
    <!-- ! Footer -->
    <footer class="footer">
  <div class="container footer--flex">
    <div class="footer-start"> </div>
    <ul class="footer-end">
       <p>2021 © TROPBOT IoT</p>
    </ul>
  </div>
</footer>
  </div>
</div>
<!-- Chart library -->
<script src="./plugins/chart.min.js"></script>
<!-- Icons library -->
<script src="plugins/feather.min.js"></script>
<!-- Custom scripts -->
<script src="js/script.js"></script>
</body>

</html>