<?php
require_once __DIR__.'/includes/config.php';

//destroy!!
unset($_SESSION["login"]);
unset($_SESSION["esAdmin"]);
unset($_SESSION["nombre"]);


session_destroy();

$tituloPagina = 'Logout';

$contenidoPrincipal = <<<EOS
<div class="logout">
    <h3>You have been logged out</h3>
</div>
EOS;

require __DIR__.'/includes/plantillas/plantilla.php';