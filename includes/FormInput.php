<?php
namespace es\ucm\fdi\aw;

class FormInput extends Form {
    public function __construct() {
        parent::__construct('formInput');
    }
    
    protected function generaCamposFormulario($datos, $errores = array()) {
        $module = $datos['module'] ?? '';
        $command = $datos['command'] ?? '';

        $htmlErroresGlobales = self::generaListaErroresGlobales($errores);
        $errorCommand = self::createMensajeError($errores, 'command', 'span', array('class' => 'error'));

        $html = <<<EOF
        $htmlErroresGlobales
        <fieldset>
        <form method="post" ...>

            <div class="container">
                <label for="maude_command" style="margin-bottom: 10px; font-weight: bold; text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.1); height:5px;">Module</label>
                <div class="fileInput">
                    <input type="text" readonly="true" placeholder="Browse" style="font-family: monospace; padding-top: 0px; font-size:12px;">
                    <input type="file" id="file" name="file" autocomplete="off" accept=".txt, .maude" onchange="fileSelected() style="font-size:12px;">
                </div>   

                <div class="content-container">
                    <textarea cols="60" rows="7" name="maude_module" id="maude_module" style="font-family: monospace; font-size:12px;adding-top: 0px;margin-bottom: 5px;" placeholder="Enter your maude module here" value="$module"></textarea>
                    <label for="maude_command" style = "font-weight: bold; font-size:12px;text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.1);height:10px;">Command</label>

                    <div class="command-container">
                        <div class="input-group">
                            <input type="text" name="maude_command" id="maude_command" placeholder="Command" style="font-size:12px;margin-right:10px;" value="$command">
                            <button type="submit" class="submit-button">Submit</button>
                        </div>
                        <div class="error-message">$errorCommand</div>
                    </div>

                </div>

                <div class="modList-container">
                    <p sytle="text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.2);"><strong >Module Examples</strong></p>
                    <ul>
                        <li onclick="fillModule('NAT')">NAT</li>
                        <li onclick="fillModule('BOOL')">BOOL</li>
                        <li onclick="fillModule('fmod FOO is pr NAT . op f : Nat Nat -> Nat . eq f(M:Nat, N:Nat) = M:Nat + N:Nat . endfm')">FOO</li>
                        <li onclick="fillModule('fmod PEANO is sorts PeanoNat . op 0 : -> PeanoNat [ctor] . op s : PeanoNat -> PeanoNat [ctor] . vars N M : PeanoNat . op _+_ : PeanoNat PeanoNat -> PeanoNat [assoc comm] . op _*_ : PeanoNat PeanoNat -> PeanoNat [assoc comm] . op esPositivo : PeanoNat -> Bool . eq [s1] : 0 + N = N . eq [s2] : s(N) + M = s(N + M) . eq 0 * N = 0 . eq s(N) * M = M + (N * M) . eq esPositivo(0) = false . eq esPositivo(s(N)) = true . endfm')">PEANO</li>
                        <li onclick="fillModule('fmod PILA is pr NAT . sort Pila . op pila-vacia : -> Pila [ctor] . op apila : Nat Pila -> Pila [ctor] . op desapila : Pila -> Pila . vars N : Nat . vars P : Pila . endfm')">PILA</li>
                        <li onclick="fillModule('mod DIE-HARD is protecting NAT . sorts Vasija ConjVasija . subsort Vasija < ConjVasija . op vasija : Nat Nat -> Vasija [ctor] . *** Capacidad / Contenido actual op __ : ConjVasija ConjVasija -> ConjVasija [ctor assoc comm] . vars M1 N1 M2 N2 : Nat . op initial : -> ConjVasija . eq initial = vasija(3, 0) vasija(5, 0) vasija(8, 0) . rl [vacia] : vasija(M1, N1) => vasija(M1, 0) . rl [llena] : vasija(M1, N1) => vasija(M1, M1) . crl [transfer1] : vasija(M1, N1) vasija(M2, N2) => vasija(M1, 0) vasija(M2, N1 + N2) if N1 + N2 <= M2 . crl [transfer2] : vasija(M1, N1) vasija(M2, N2) => vasija(M1, sd(N1 + N2, M2)) vasija(M2, M2) if N1 + N2 > M2 . endm')">DIE-HARD</li>
                    </ul>
                </div>
            </div>
            </form>
        </fieldset>
       
        <script>
    
        function fillModule(example) {
            document.getElementById("maude_module").value = example;
        }
    
        function fileSelected() {
          var fileInput = document.getElementById('file');
          var file = fileInput.files[0];
    
          if (file) {
            var reader = new FileReader();
    
            reader.onload = function(e) {
              var fileContent = e.target.result;
              document.getElementById('maude_module').value = fileContent;
            };
    
            reader.readAsText(file);
          }
        }

        </script>

        EOF;

        return $html;
    } 

    protected function procesaFormulario($datos) {
        
        $this->errores = [];
        $module = $_POST['maude_module'] ?? null;
        $command = $_POST['maude_command'] ?? null;
        $user = $_SESSION['user_id'] ?? null;
/*
        if (empty($module)) { 
            if(empty($_SESSION['module'])) {
                $this->errores['module'] = "No module has been defined yet";
            }

            else {
                $module = $_SESSION['module'] ?? null;
            }
        }

        else{
            $_SESSION['module'] = $module;
        }
*/
        if (empty($command)) {
            $this->errores['command'] = "Enter a command";
        }

        if (count($this->errores) === 0) {
            $resultArray = Input::execute();

            $resultArray = array_pad($resultArray, 5, '');
// = $user ?? 1
            $input = Input::create($module, $command, $resultArray[4], $resultArray[3], $user = $user ?? 1);

            $result = <<<EOF
            <h4 style='margin-top: 5px; margin-bottom: 10px;'>Input:</h4>
            Module: $resultArray[0] <br> Command: $resultArray[1] <br> Parameters: $resultArray[2]
            <h4 style='margin-top: 20px; margin-bottom: 10px;'>Result  $resultArray[3]: </h4>
            $resultArray[4]
            EOF;

            return $result;
        }
        return $this->errores;
    }
   
}
