<?php

require_once __DIR__.'/includes/config.php';
require_once __DIR__.'/includes/FormularioRegistro.php';

$form = new es\ucm\fdi\aw\FormularioRegistro();
$htmlFormRegistro = $form->gestiona();

$tituloPagina = 'Registro';

$contenidoPrincipal = <<<EOS
<div class="account">
    <h1>Create an account</h1>
    $htmlFormRegistro
    <p style="margin-top: 25px;color: #646464; font-size: 13px; text-align:center;">Already have an account?<br><a href='login.php'>Sing in</a></p>
</div>
EOS;

require __DIR__.'/includes/plantillas/plantilla.php';