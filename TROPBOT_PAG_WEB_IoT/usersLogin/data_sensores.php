<?php
// Solo se permite el ingreso con el inicio de sesion.
session_start();
// Si el usuario no se ha logueado se le regresa al inicio.
if (!isset($_SESSION['login_sess'])) {
   echo '
     <script>
        alert("Por favor, inicie sesión primero para ver esta página.");
        window.location = "http:///tropbot-iot21.125mb.com/usersLogin/logout.php";
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
  <title>TROPBOT &amp; Porque sabemos que amas tu cultivo | Adquisición</title>
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
                    <a class="active" href="/usersLogin/data_sensores.php">
                       <p>  <span class="icon document" aria-hidden="true"></span> Temperatura <br>Ambiente <br>
                        <br> <span class="icon folder" aria-hidden="true"></span>
                        Humedad Relativa <br>del aire<br>
                        <br> <span class="icon image" aria-hidden="true"></span>Radiación Solar e Iluminación Ambiente</p> </a>
                     
                </li>
                <span class="system-menu__title">Principal</span>
                <li>
                    <a href="/usersLogin/dashboard.php"><span class="icon home" aria-hidden="true"></span>Página Principal</a> 
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
    <!-- ! Main -->
    <main class="main users chart-page" id="skip-target">
        <nav class="main-nav--bg ">
            <div class="container main-nav">
                <!--div class="main-nav-start"></div-->
                <h2 class="main-title">Estado de su cultivo</h2>
                <div class="main-nav-end">
                    <button class="theme-switcher gray-circle-btn" type="button" title="Switch theme">
                        <span class="sr-only">Cambiar Tema</span>
                        <i class="sun-icon" data-feather="sun" aria-hidden="true"></i>
                        <i class="moon-icon" data-feather="moon" aria-hidden="true"></i>
                    </button>
                
                    <div class="nav-user-wrapper">
                    
                        <button href="##" class="nav-user-btn dropdown-btn" title="My profile" type="button">
                            <span class="sr-only">Mi Perfil</span>
                            <span class="nav-user-img"><img src="./img/avatar/avatar-illustrated-02.png" alt="User name"></span>
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

      <div class="container">
        <!-- ////////////////////////////////////////////////////////////////////////////////////////////-->
                    <div class="row">
                        <div class="col-md-12">
                            <div class="card">
                                <div class="card-header">
                                    <h5 class="card-title">Reporte Mensual de <strong> Temperatura </strong></h5>
                                    <div class="card-tools">
                                        <button type="button" class="btn btn-tool" data-card-widget="collapse">
                                            <i class="fas fa-minus"></i>
                                        </button>
                                        
                                    </div>
                                </div>
                                <!-- /.card-header -->
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-md-8">
                                            <p class="text-center">
                                                <strong>Temperatura ° C por Regiones</strong>
                                            </p>
                                            <div class="chart">
                                                <!-- Sales Chart Canvas -->
                                                <iframe width="705" height="365" style="border: 3px solid #cccccc;" src="https://thingspeak.com/apps/matlab_visualizations/436757?width=690&height=350">
                                                </iframe>
                                            </div>
                                            <!-- /.chart-responsive -->
                                        </div>      
                                        <!-- /.col -->
                                        <div class="col-md-4">
                                            <p class="text-center">
                                                <strong>Alerta Temperatura</strong>
                                            </p>
                                            <div class = "chart">
                                                <iframe width="350" height="200" style="border: 3px solid #cccccc;" src="https://thingspeak.com/apps/matlab_visualizations/437389?width=300">
                                                </iframe>
                                            </div>
                                            <!-- /.progress-group -->
                                        </div>
                                        <!-- /.col -->
                                    </div>
                                    <!-- /.row -->
                                </div>
                                <!-- ./card-body -->
                                <div class="card-footer">
                                    <div class="row">
                                        <div class="col-sm-4 col-8">
                                            <div class="description-block border-right">
                                                <h5 class="description-header">Valor mínimo de Temperatura °C</h5>
                                                <iframe width="90" height="50" style="border: 3px solid #fc021a;" src="https://thingspeak.com/apps/matlab_visualizations/437403?width=50&height=50"></iframe>
                                            </div>
                                            <!-- /.description-block -->
                                        </div>
                                        <!-- /.col -->
                                        <div class="col-sm-4 col-8">
                                            <div class="description-block border-right">
                                                <h5 class="description-header">Valor Promedio de Temperatura °C</h5>
                                                <iframe width="90" height="50" style="border: 3px solid #fb5c04;" src="https://thingspeak.com/apps/matlab_visualizations/437396?width=50&height=50"></iframe>
                                            </div>
                                            <!-- /.description-block -->
                                        </div>
                                        <!-- /.col -->
                                        <div class="col-sm-4 col-8">
                                            <div class="description-block border-right">
                                                <h5 class="description-header">Valor máximo de Temperatura °C</h5>
                                                <iframe width="90" height="50" style="border: 3px solid #f9b900;" src="https://thingspeak.com/apps/matlab_visualizations/436053?width=50&height=50"></iframe>
                                            </div>
                                            <!-- /.description-block -->
                                        </div>
                                        <!-- /.col -->
                                    </div>
                                    <!-- /.row -->
                                </div>
                                <!-- /.card-footer -->                                                                                               
                            </div>
                            <!-- /.card -->                       
                        </div>
                        <!-- /.col -->
                    </div> 
                    <!-- /.row -->
         <!-- ////////////////////////////////////////////////////////////////////////////////////////////-->
                    <div class="row">
                        <div class="col-md-12">
                            <div class="card">
                                <div class="card-header">
                                    <h5 class="card-title">Reporte Mensual de <strong> Humedad Relativa </strong></h5>
                                    <div class="card-tools">
                                        <button type="button" class="btn btn-tool" data-card-widget="collapse">
                                            <i class="fas fa-minus"></i>
                                        </button>
                                        
                                    </div>
                                </div>
                                <!-- /.card-header -->
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-md-8">
                                            <p class="text-center">
                                                <strong>Porcentaje de Humedad Relativa en el Aire por Regiones</strong>
                                            </p>
                                            <div class="chart">
                                                <!-- Sales Chart Canvas -->
                                                <iframe width="705" height="365" style="border: 3px solid #cccccc;" src="https://thingspeak.com/apps/matlab_visualizations/436765?width=690&height=350">
                                                </iframe>
                                            </div>
                                            <!-- /.chart-responsive -->
                                        </div>      
                                        <!-- /.col -->
                                        <div class="col-md-4">
                                            <p class="text-center">
                                                <strong>Alerta Humedad</strong>
                                            </p>
                                            <div class="chart">
                                                <iframe width="350" height="200" style="border: 3px solid #cccccc;" src="https://thingspeak.com/apps/matlab_visualizations/437388?width=300">
                                                </iframe>
                                            </div>
                                            <!-- /.progress-group -->
                                        </div>
                                        <!-- /.col -->
                                    </div>
                                    <!-- /.row -->
                                </div>
                                <!-- ./card-body -->
                                <div class="card-footer">
                                    <div class="row">
                                        <div class="col-sm-4 col-8">
                                            <div class="description-block border-right">
                                                <h5 class="description-header">Porcentaje mínimo de Humedad Relativa</h5>
                                                <iframe width="90" height="50" style="border: 3px solid #fc021a;" src="https://thingspeak.com/apps/matlab_visualizations/436052?width=50&height=50"></iframe>
                                            </div>
                                            <!-- /.description-block -->
                                        </div>
                                        <!-- /.col -->
                                        <div class="col-sm-4 col-8">
                                            <div class="description-block border-right">
                                                <h5 class="description-header">Porcentaje Promedio de Humedad Relativa</h5>
                                                <iframe width="90" height="50" style="border: 3px solid #fb5c04;" src="https://thingspeak.com/apps/matlab_visualizations/436044?width=50&height=50"></iframe>
                                            </div>
                                            <!-- /.description-block -->
                                        </div>
                                        <!-- /.col -->
                                        <div class="col-sm-4 col-8">
                                            <div class="description-block border-right">
                                                <h5 class="description-header">Porcentaje máximo de Humedad Relativa</h5>
                                                <iframe width="90" height="50" style="border: 3px solid #f9b900;" src="https://thingspeak.com/apps/matlab_visualizations/436049?width=50&height=50"></iframe>
                                            </div>
                                            <!-- /.description-block -->
                                        </div>
                                        <!-- /.col -->
                                    </div>
                                    <!-- /.row -->
                                </div>
                                <!-- /.card-footer -->                                                                                               
                            </div>
                            <!-- /.card -->                       
                        </div>
                        <!-- /.col -->
                    </div> 
                    <!-- /.row -->
        <!-- ////////////////////////////////////////////////////////////////////////////////////////////-->
                <div class="row">
                        <div class="col-md-12">
                            <div class="card">
                                <div class="card-header">
                                    <h5 class="card-title">Reporte Mensual de <strong> Iluminación Ambiente </strong></h5>
                                    <div class="card-tools">
                                        <button type="button" class="btn btn-tool" data-card-widget="collapse">
                                            <i class="fas fa-minus"></i>
                                        </button>
                                       
                                    </div>
                                </div>
                                <!-- /.card-header -->
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-md-8">
                                            <p class="text-center">
                                                <strong>Iluminación Ambiente por Regiones</strong>
                                            </p>
                                            <div class="chart">
                                                <!-- Sales Chart Canvas -->
                                                <iframe width="705" height="365" style="border: 3px solid #cccccc;" src="https://thingspeak.com/apps/matlab_visualizations/436766?width=690&height=350">
                                                </iframe>
                                            </div>
                                            <!-- /.chart-responsive -->
                                        </div>      
                                        <!-- /.col -->
                                        <div class="col-md-4">
                                            <p class="text-center">
                                                <strong>Alerta Iluminación Ambiente</strong>
                                            </p>
                                            <div class="chart">
                                                <iframe width="350" height="200" style="border: 3px solid #cccccc;" src="https://thingspeak.com/apps/matlab_visualizations/437390?width=300">
                                                </iframe>
                                            </div>
                                            <!-- /.progress-group -->
                                        </div>
                                        <!-- /.col -->
                                    </div>
                                    <!-- /.row -->
                                </div>
                                <!-- ./card-body -->
                                <div class="card-footer">
                                    <div class="row">
                                        <div class="col-sm-4 col-8">
                                            <div class="description-block border-right">
                                                <h5 class="description-header">Valor mínimo de Iluminación Ambiente</h5>
                                                <iframe width="90" height="50" style="border: 3px solid #fc021a;" src="https://thingspeak.com/apps/matlab_visualizations/437405?width=50&height=50"></iframe>
                                            </div>
                                            <!-- /.description-block -->
                                        </div>
                                        <!-- /.col -->
                                        <div class="col-sm-4 col-8">
                                            <div class="description-block border-right">
                                                <h5 class="description-header">Valor promedio de Iluminación Ambiente</h5>
                                                <iframe width="90" height="50" style="border: 3px solid #fb5c04;" src="https://thingspeak.com/apps/matlab_visualizations/437404?width=50&height=50"></iframe>
                                            </div>
                                            <!-- /.description-block -->
                                        </div>
                                        <!-- /.col -->
                                        <div class="col-sm-4 col-8">
                                            <div class="description-block border-right">
                                                <h5 class="description-header">Valor máximo de Iluminación Ambiente</h5>
                                                <iframe width="90" height="50" style="border: 3px solid #f9b900;" src="https://thingspeak.com/apps/matlab_visualizations/437406?width=50&height=50"></iframe>
                                            </div>
                                            <!-- /.description-block -->
                                        </div>
                                        <!-- /.col -->
                                    </div>
                                    <!-- /.row -->
                                </div>
                                <!-- /.card-footer -->                                                                                               
                            </div>
                            <!-- /.card -->                       
                        </div>
                        <!-- /.col -->
                    </div> 
                    <!-- /.row -->
        
        <!-- ////////////////////////////////////////////////////////////////////////////////////////////-->
                <div class="row">
                        <div class="col-md-12">
                            <div class="card">
                                <div class="card-header">
                                    <h5 class="card-title">Reporte Mensual de <strong> Radiación UV </strong></h5>
                                    <div class="card-tools">
                                        <button type="button" class="btn btn-tool" data-card-widget="collapse">
                                            <i class="fas fa-minus"></i>
                                        </button>
                                       
                                    </div>
                                </div>
                                <!-- /.card-header -->
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-md-8">
                                            <p class="text-center">
                                                <strong>Radiación UV por Regiones</strong>
                                            </p>
                                            <div class="chart">
                                                <!-- Sales Chart Canvas -->
                                                <iframe width="705" height="365" style="border: 3px solid #cccccc;" src="https://thingspeak.com/apps/matlab_visualizations/436767?width=690&height=350">
                                                </iframe>
                                            </div>
                                            <!-- /.chart-responsive -->
                                        </div>      
                                        <!-- /.col -->
                                        <div class="col-md-4">
                                            <p class="text-center">
                                                <strong>Alerta Exposición a Radiación UV</strong>
                                            </p>
                                            <div class="chart">
                                                <iframe width="350" height="200" style="border: 3px solid #cccccc;" src="https://thingspeak.com/apps/matlab_visualizations/437391?width=300">
                                                </iframe>
                                            </div>
                                            <!-- /.progress-group -->
                                        </div>
                                        <!-- /.col -->
                                    </div>
                                    <!-- /.row -->
                                </div>
                                <!-- ./card-body -->
                                <div class="card-footer">
                                    <div class="row">
                                        <div class="col-sm-4 col-8">
                                            <div class="description-block border-right">
                                                <h5 class="description-header">Valor mínimo de Radiación UV</h5>
                                                <iframe width="90" height="50" style="border: 3px solid #fc021a;" src="https://thingspeak.com/apps/matlab_visualizations/436054?width=50&height=50"></iframe>
                                            </div>
                                            <!-- /.description-block -->
                                        </div>
                                        <!-- /.col -->
                                        <div class="col-sm-4 col-8">
                                            <div class="description-block border-right">
                                                <h5 class="description-header">Valor promedio de Radiación UV</h5>
                                                <iframe width="90" height="50" style="border: 3px solid #fb5c04;" src="https://thingspeak.com/apps/matlab_visualizations/436045?width=50&height=50"></iframe>
                                            </div>
                                            <!-- /.description-block -->
                                        </div>
                                        <!-- /.col -->
                                        <div class="col-sm-4 col-8">
                                            <div class="description-block border-right">
                                                <h5 class="description-header">Valor máximo de Radiación UV</h5>
                                                <iframe width="90" height="50" style="border: 3px solid #f9b900;" src="https://thingspeak.com/apps/matlab_visualizations/436291?width=50&height=50"></iframe>
                                            </div>
                                            <!-- /.description-block -->
                                        </div>
                                        <!-- /.col -->
                                    </div>
                                    <!-- /.row -->
                                </div>
                                <!-- /.card-footer -->                                                                                               
                            </div>
                            <!-- /.card -->                       
                        </div>
                        <!-- /.col -->
                    </div> 
                    <!-- /.row -->
        
          <!-- ////////////////////////////////////////////////////////////////////////////////////////////-->
                   <div class="row">
                        <div class="col-md-12">
                            <div class="card">
                                <div class="card-header">
                                    <h5 class="card-title"><strong> Reporte de Ubicación </strong> del recorrido en el Cultivo</h5>
                                  
                                </div>
                                <!-- /.card-header -->
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-md-6">
                                            <p class="text-center">
                                                <strong>Región 1</strong>
                                            </p>
                                            <div class="chart">
                                                <!-- Sales Chart Canvas -->
                                                <iframe width="500" height="365" style="border: 3px solid #cccccc;" src="https://thingspeak.com/apps/matlab_visualizations/436769?width=490&height=350">
                                                </iframe>
                                            </div>
                                            <!-- /.chart-responsive -->
                                        </div>  
                                        
                                        <div class="col-md-6">
                                            <p class="text-center">
                                                <strong>Región 2</strong>
                                            </p>
                                            <div class="chart">
                                                <!-- Sales Chart Canvas -->
                                                <iframe width="500" height="365" style="border: 3px solid #cccccc;" src="https://thingspeak.com/apps/matlab_visualizations/436770?width=490&height=350">
                                                </iframe>
                                            </div>
                                            <!-- /.chart-responsive -->
                                        </div>  
                                   
                                    </div>
                                    <!-- /.row -->
                                </div>                                                                                             
                            </div>
                            <!-- /.card -->                       
                        </div>
                        <!-- /.col -->
                    </div> 
                    <!-- /.row -->
          
        <!-- ////////////////////////////////////////////////////////////////////////////////////////////-->
         
          
        <!-- ////////////////////////////////////////////////////////////////////////////////////////////-->
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


<!-- ////////////////////////////////////////////////////////////////////////////////////////////-->
<!-- REQUIRED SCRIPTS -->
<!-- jQuery -->
<script src="charts/plugins/jquery/jquery.min.js"></script>
<!-- Bootstrap -->
<script src="charts/plugins/bootstrap/js/bootstrap.bundle.min.js"></script>
<!-- AdminLTE App -->
<script src="charts/dist/js/adminlte.js"></script>
<!-- ChartJS -->
<script src="charts/plugins/chart.js/Chart.min.js"></script>
<!-- AdminLTE dashboard demo (This is only for demo purposes) -->
<script src="charts/dist/js/pages/dashboard2.js"></script>

</body>

</html>