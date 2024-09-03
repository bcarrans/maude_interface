<?php

require_once __DIR__.'/includes/config.php';

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

<div class=profile>Sorry, this page is not avaiable yet!</div>
EOS;

require __DIR__.'/includes/plantillas/plantilla.php';

?>
<script>
    window.onload = function() {
        var rightColumn = document.querySelector('.logs');
        rightColumn.scrollTop = rightColumn.scrollHeight;
    };
</script>