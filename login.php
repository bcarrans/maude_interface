<?php

require_once __DIR__.'/includes/config.php';

$form = new es\ucm\fdi\aw\FormularioLogin();
$htmlFormLogin = $form->gestiona();

$tituloPagina = 'Login';

$contenidoPrincipal = <<<EOS
<div class="account">
    <h1>Log in to your account</h1>
    $htmlFormLogin
    <p style="margin-top: 25px;color: #646464; font-size: 13px; text-align:center;">Don't have an account yet?<br><a href='registro.php'>Sing up</a></p>
</div>
EOS;

require __DIR__.'/includes/plantillas/plantilla.php';