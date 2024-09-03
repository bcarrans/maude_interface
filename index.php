<?php

require_once __DIR__.'/includes/config.php';

$form = new es\ucm\fdi\aw\FormInput();
$htmlFormLogin = $form->gestiona2();

$userId = $_SESSION['user_id'] ?? null;
$inputUserEntriesHtml = '<div>';
$inputSessionEntriesHtml = '<div>';

if ($userId !== null) {
    $inputs = es\ucm\fdi\aw\Input::getUserInputs($userId);
    foreach ($inputs as $input) {
        $inputUserEntriesHtml .= sprintf(
            '<div class="input-cell">
                <p><strong>Input:</strong></p>
                <p>Module: %s</p>
                <p>Command: %s</p>
                <p><strong>Result %s:</strong></p>
                <p>%s</p>
            </div>',
            htmlspecialchars($input->module()),
            htmlspecialchars($input->command()),
            htmlspecialchars($input->sort()),
            htmlspecialchars($input->result())
        );
    }
    $inputUserEntriesHtml .= '</div>';
}

else {
    $inputs = es\ucm\fdi\aw\Input::getSessionInputs();
    foreach ($inputs as $input) {
        $inputSessionEntriesHtml .= sprintf(
            '<div class="input-cell">
                <p><strong>Input:</strong></p>
                <p>Module: %s</p>
                <p>Command: %s</p>
                <p><strong>Result %s:</strong></p>
                <p>%s</p>
            </div>',           
            htmlspecialchars($input->module()),
            htmlspecialchars($input->command()),
            htmlspecialchars($input->sort()),
            htmlspecialchars($input->result())
        );
    }
    $inputSessionEntriesHtml .= '</div>';
}

$tituloPagina = 'Maude Web Interface';

$contenidoPrincipal = <<<EOS
<div class="prompt-columns">
    <div class="left-column">
        <div class="instructions">
            <p>To begin using Maude, enter a module and a command following The Maude System syntax and click "Submit".<br><br>You can also enter a module though an uploaded file (.txt, .maude) or use one of the sugested modules in the section "Module Examples".</p>
        </div>    
        $htmlFormLogin
        <div id="resultContainer"></div>
    </div>
    <div class="right-column">
        <div class="tabs">
            <input type="radio" id="tab1" name="tab" checked>
            <label for="tab1">Execution history</label>
            <input type="radio" id="tab2" name="tab">
            <label for="tab2">Review mistakes</label>
            <!-- <input type="text" id="searchField" placeholder="Search..." onkeyup="searchLogs()">  -->
        </div>
        <div class="tab-content" id="sessionContent">
            <div class="logs">
                $inputSessionEntriesHtml
            </div>
        </div>
        <div class="tab-content" id="allContent">
            <div class="logs">
                $inputUserEntriesHtml
            </div>
        </div>
    </div>
</div>
EOS;


/*$direcciones = [
    "pagina1" => ["Login" => resuelveURL("/login.php")],
    "pagina2" => ["Registro" => resuelveURL("/registro.php")],
];

if (compruebaLogueado(false)) {
    if (tieneRol([\es\ucm\fdi\aw\Usuario::PROF_ROLE])) {
        $direcciones = [
            "pagina1" => ["Registro" => resuelveURL("/registro.php")],
            "pagina2" => ["Gestiona evaluaciones" => resuelveURL("/gestionaEvaluaciones.php")],
            "pagina3" => ["Salir" => resuelveURL("/logout.php")]
        ];
    } else {
        $direcciones = [
            "pagina1" => ["Registro" => resuelveURL("/registro.php")],
            "pagina2" => ["Evaluar grupo" => resuelveURL("/autoevaluacion.php")],
            "pagina3" => ["Mis evaluaciones" => resuelveURL("/verMisEvaluaciones.php")],
            "pagina4" => ["Salir" => resuelveURL("/logout.php")]
        ];        
    }
}
$navegacion = creaMenu($direcciones);}*/

require __DIR__.'/includes/plantillas/plantilla.php';

?>
<script>
    window.onload = function() {
        var rightColumn = document.querySelector('.logs');
        rightColumn.scrollTop = rightColumn.scrollHeight;
    };
</script>