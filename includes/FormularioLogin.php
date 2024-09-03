<?php
namespace es\ucm\fdi\aw;

class FormularioLogin extends Form
{
    public function __construct() {
        parent::__construct('formLogin');
    }
    
    protected function generaCamposFormulario($datos, $errores = array())
    {
        $nombreUsuario =$datos['nombreUsuario'] ?? '';

        $htmlErroresGlobales = self::generaListaErroresGlobales($errores);
        //$htmlErroresGlobales = isset($errores['global']) ? $errores['global'] : '';

        $errorNombreUsuario = self::createMensajeError($errores, 'nombreUsuario', 'span', array('class' => 'error'));
        $errorPassword = self::createMensajeError($errores, 'password', 'span', array('class' => 'error'));

        $html = <<<EOF
        <div class="accountform">
        <fieldset>
            $htmlErroresGlobales
            <p><label>Username</label> <input type="text" name="nombreUsuario" value="$nombreUsuario"/>$errorNombreUsuario</p>
            <p><label>Password</label> <input type="password" name="password" />$errorPassword</p>
            <div class=loginbutton>
                <button type="submit" name="login">Log in</button>
            </div>
        </fieldset>
        </div>

        EOF;
        return $html;
    }
    

    protected function procesaFormulario($datos)
    {
        $result = array();
        
        $nombreUsuario =$datos['nombreUsuario'] ?? null;
                
        if ( empty($nombreUsuario) ) {
            $result['nombreUsuario'] = "This field is required";
        }
        
        $password = $datos['password'] ?? null;
        if ( empty($password) ) {
            $result['password'] = "This field is required";
        }
        
        if (count($result) === 0) {
            $usuario = User::login($nombreUsuario, $password);
            if (!$usuario) {
                $result[] = "<div class='error'>The username or password is incorrect</div>";
            } else {
                $_SESSION['login'] = true;
                $_SESSION['nombre'] = $nombreUsuario;
                $_SESSION['user_id'] = $usuario->id();
                $result = 'index.php';
            }
        }
        return $result;
    }
}