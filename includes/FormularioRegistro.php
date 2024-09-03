<?php
namespace es\ucm\fdi\aw;

class FormularioRegistro extends Form
{
    public function __construct() {
        parent::__construct('formRegistro');
    }
    
    protected function generaCamposFormulario($datos, $errores = array())
    {
        $nombreUsuario = $datos['nombreUsuario'] ?? '';
        $nombre = $datos['nombre'] ?? '';

        $htmlErroresGlobales = self::generaListaErroresGlobales($errores);
        $errorNombreUsuario = self::createMensajeError($errores, 'nombreUsuario', 'span', array('class' => 'error'));
        $errorNombre = self::createMensajeError($errores, 'nombre', 'span', array('class' => 'error'));
        $errorPassword = self::createMensajeError($errores, 'password', 'span', array('class' => 'error'));
        $errorPassword2 = self::createMensajeError($errores, 'password2', 'span', array('class' => 'error'));

        $html = <<<EOF
        <div class="accountform">
        <fieldset>
            $htmlErroresGlobales
            <label>Username</label> <input class="control" type="text" name="nombreUsuario" value="$nombreUsuario" />$errorNombreUsuario
            <label>Full name</label> <input class="control" type="text" name="nombre" value="$nombre" />$errorNombre
            <label>Password</label> <input class="control" type="password" name="password" />$errorPassword
            <label>Confirm your password</label> <input class="control" type="password" name="password2" />$errorPassword2
            <div class=loginbutton>
                <div class="grupo-control"><button type="submit" name="registro" style="margin-top:10px;">Create account</button></div>
            </div>
        </fieldset>
        </div>
        EOF;
        return $html;
    }
    

    protected function procesaFormulario($datos)
    {
        $result = array();
        
        $nombreUsuario = $datos['nombreUsuario'] ?? null;
        
        if ( empty($nombreUsuario) || mb_strlen($nombreUsuario) < 5 ) {
            $result['nombreUsuario'] = "The username must contain at<br>least 5 characters";
        }
        
        $nombre = $datos['nombre'] ?? null;
        if ( empty($nombre) || mb_strlen($nombre) < 5 ) {
            $result['nombre'] = "The username must contain at<br>least 5 characters";
        }
        
        $password = $datos['password'] ?? null;
        if ( empty($password) || mb_strlen($password) < 5 ) {
            $result['password'] = "The passwords must contain at<br>least 5 characters";
        }
        $password2 = $datos['password2'] ?? null;
        if ( empty($password2) || strcmp($password, $password2) !== 0 ) {
            $result['password2'] = "The passwords do not match";
        }
        
        if (count($result) === 0) {
            $user = User::crea($nombreUsuario, $nombre, $password);
            if ( ! $user ) {
                $result[] = "<div class='error'>This user already exists</div>";
            } else {
                $_SESSION['login'] = true;
                $_SESSION['nombre'] = $nombreUsuario;
                $_SESSION['user_id'] = $user->id();
                $result = 'index.php';
            }
        }
        return $result;
    }
}