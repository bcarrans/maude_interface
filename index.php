<?php

require_once __DIR__.'/includes/config.php';

$form = new es\ucm\fdi\aw\FormInput();
$htmlFormLogin = $form->gestiona2();

$userId = $_SESSION['user_id'] ?? null;
#$userId = $_SESSION['session_id'] ?? null;
$sessionId = session_id();

$inputList = '<div>';
$errorList = '<div>';

if ($userId !== null) {
    $inputs = es\ucm\fdi\aw\Input::getUserInputs($userId);
    $errors = es\ucm\fdi\aw\Input::getUserErrors($userId);
}

else {
    $inputs = es\ucm\fdi\aw\Input::getSessionInputs($sessionId);
    $errors = es\ucm\fdi\aw\Input::getSessionErrors($sessionId);
}


if (!empty($inputs)) {
    foreach ($inputs as $input) {
        $inputList .= sprintf(
            '<div class="input-cell">
                <p><strong>Input:</strong></p>
                <p>Module: %s</p>
                <p>Command: %s</p>
                <p><strong>Result %s:</strong>  %s</p>
            </div>',
            htmlspecialchars($input->module()),
            htmlspecialchars($input->command()),
            htmlspecialchars($input->sort()),
            htmlspecialchars($input->result())
        );
    }
} else{
    $inputList .= '<p>No data</p>';
}

$inputList .= '</div>';


if (!empty($errors)) {
    foreach ($errors as $error) {
        $errorList .= sprintf(
            '<div class="input-cell">
                <p><strong>Input:</strong></p>
                <p>Module: %s</p>
                <p>Command: %s</p>
                <p><span style="color: rgb(150, 0, 0);"> <strong>Error:</strong> %s</span></p>
            </div>',
            htmlspecialchars($error->module()),
            htmlspecialchars($error->command()),
            htmlspecialchars($error->error())
        );
    }
} else {
    $errorList .= '<p>No data</p>';
}

$errorList .= '</div>';



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

        <div class="tab-content" id="inputContent">
            <div class="logs">
                <div class="input-cell">
                $inputList
                </div>
            </div>
        </div>

        <div class="tab-content" id="errorsContent">
            <div class="logs">
                <div class="input-cell">
                    $errorList
                </div>
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
    document.addEventListener("DOMContentLoaded", function() {
        var rightColumn = document.querySelector('.logs');
        if (rightColumn) {
            rightColumn.scrollTop = rightColumn.scrollHeight;
        }

        var inputContent = document.getElementById('inputContent');
        var errorsContent = document.getElementById('errorsContent');
        var tab1 = document.getElementById('tab1');
        var tab2 = document.getElementById('tab2');

        inputContent.style.display = 'block';
        errorsContent.style.display = 'none';

        tab1.addEventListener('change', function() {
            inputContent.style.display = 'block';
            errorsContent.style.display = 'none';
        });

        tab2.addEventListener('change', function() {
            inputContent.style.display = 'none';
            errorsContent.style.display = 'block';
        });
    });
</script>