<?php
namespace es\ucm\fdi\aw;

class Input {

    public static function compare($module, $command, $result, $user) {

        // Find two entries with the same command and different modules?

        return false;
    }

    public static function getModule($moduleName) { # ESTO DE MOMENTO NO
        //le paso mejor el module que referencia a otro module o el moduleName?
        //un metodo para cada mejor i think

        $app = Aplicacion::getSingleton();
        $conn = $app->conexionBd();
        
        //jaj no. tengo que encontrar el que se llame así, no coincide la string entera. y no otro que referencie al mismo tampoco.
        $query = sprintf("SELECT * FROM Input I WHERE I.module = '%s'", $conn->real_escape_string($moduleName));
        $rs = $conn->query($query);
        $result = false;
        if ($rs) {
            if ( $rs->num_rows == 1) {
                $fila = $rs->fetch_assoc();
                $user = new User($fila['username'], $fila['name'], $fila['password']);
                $user->id = $fila['id'];
                $result = $user;
            }
            $rs->free();
        } else {
            echo "Error al consultar en la BD: (" . $conn->errno . ") " . utf8_encode($conn->error);
            exit();
        }
        return $result;
    }   
           
    public static function execute() {
        $maude_module = base64_encode($_POST["maude_module"]);
        $maude_command = base64_encode($_POST["maude_command"]);
        
        $temp_module_path = __DIR__ . "/temp_module.txt";
        $temp_command_path = __DIR__ . "/temp_command.txt";
        $python_script_path = __DIR__ . "/script.py";
        
        file_put_contents($temp_module_path, $maude_module);
        file_put_contents($temp_command_path, $maude_command);
        
        $result = shell_exec("/venv/bin/python3 " . $python_script_path . " \"$maude_module\" \"$maude_command\"");

        $resultArray = explode("<!-- SPLIT -->", $result);
                
        unlink($temp_module_path);
        unlink($temp_command_path);
        
        return $resultArray;
    }

    public static function getUserInputs($userId) {
        $app = Aplicacion::getSingleton();
        $conn = $app->conexionBd();
        $query = sprintf("SELECT * FROM Input WHERE user = '%s'", $conn->real_escape_string($userId));
        $rs = $conn->query($query);
        $inputs = [];
        if ($rs) {
            while ($fila = $rs->fetch_assoc()) {
                $input = new Input($fila['module'], $fila['command'], $fila['result'], $fila['error'], $fila['sort'], $fila['session_id'], $fila['user']);
                $input->id = $fila['id'];
                $inputs[] = $input;
            }
            $rs->free();
        } else {
            echo "Error al consultar en la BD: (" . $conn->errno . ") " . utf8_encode($conn->error);
            exit();
        }
        return $inputs;
    }

    public static function getSessionInputs($sessionId) {
        $app = Aplicacion::getSingleton();
        $conn = $app->conexionBd();
        $query = sprintf("SELECT * FROM Input WHERE session_id = '%s'", $conn->real_escape_string($sessionId));
        $rs = $conn->query($query);
        $inputs = [];
        if ($rs) {
            while ($fila = $rs->fetch_assoc()) {
                $input = new Input($fila['module'], $fila['command'], $fila['result'], $fila['error'], $fila['sort'], $fila['session_id'], $fila['user']);
                $input->id = $fila['id'];
                $inputs[] = $input;
            }
            $rs->free();
        } else {
            echo "Error al consultar en la BD: (" . $conn->errno . ") " . utf8_encode($conn->error);
            exit();
        }
        return $inputs;
    }

    public static function getUserErrors($userId) {
        $app = Aplicacion::getSingleton();
        $conn = $app->conexionBd();
        $query = sprintf("SELECT * FROM Input WHERE user = '%s' AND result = 'Error'", $conn->real_escape_string($userId));
        $rs = $conn->query($query);
        $inputs = [];
        if ($rs) {
            while ($fila = $rs->fetch_assoc()) {
                $input = new Input($fila['module'], $fila['command'], $fila['result'], $fila['error'], $fila['sort'], $fila['session_id'], $fila['user']);
                $input->id = $fila['id'];
                $inputs[] = $input;
            }
            $rs->free();
        } else {
            echo "Error al consultar en la BD: (" . $conn->errno . ") " . utf8_encode($conn->error);
            exit();
        }
        return $inputs;
    }


    public static function getSessionErrors($sessionId) {
        $app = Aplicacion::getSingleton();
        $conn = $app->conexionBd();
        $query = sprintf("SELECT * FROM Input WHERE session_id = '%s' AND result = 'Error'", $conn->real_escape_string($sessionId));
        $rs = $conn->query($query);
        $inputs = [];
        if ($rs) {
            while ($fila = $rs->fetch_assoc()) {
                $input = new Input($fila['module'], $fila['command'], $fila['result'], $fila['error'], $fila['sort'], $fila['session_id'], $fila['user']);
                $input->id = $fila['id'];
                $inputs[] = $input;
            }
            $rs->free();
        } else {
            echo "Error al consultar en la BD: (" . $conn->errno . ") " . utf8_encode($conn->error);
            exit();
        }
        return $inputs;
    }

    public static function findInput($command) {
        $app = Aplicacion::getSingleton();
        $conn = $app->conexionBd();
        $query = sprintf("SELECT * FROM Input I WHERE I.command = '%s' AND I.user = '%s'", $conn->real_escape_string($command));
        $rs = $conn->query($query);
        $result = false;
        if ($rs) {
            if ( $rs->num_rows == 1) {
                $fila = $rs->fetch_assoc();
                $input = new Input($fila['module'], $fila['command'], $fila['result'], $fila['error'], $fila['sort'], $fila['session_id'], $fila['user']);
                $input->id = $fila['id'];
                $result = $input;
            }
            $rs->free();
        } else {
            echo "Error al consultar en la BD: (" . $conn->errno . ") " . utf8_encode($conn->error);
            exit();
        }
        return $result;
    }
    
    public static function create($module, $command, $result, $error, $sort, $session_id, $user) {
        $input = new Input($module, $command, $result, $error, $sort, $session_id, $user);
        return self::save($input);
    }
    
    public static function save($input) {
        if ($input->id !== null) {
            return self::update($input);
        }
        return self::insert($input);
    }
    
    /*private static function insert($input) {
        $app = Aplicacion::getSingleton();
        $conn = $app->conexionBd();

        //$userValue = is_null($input->user) ? "NULL" : $conn->real_escape_string($input->user);

        if (is_null($input->user)) {
            $userValue = "NULL";
        } else {
            $userValue = filter_var($input->user, FILTER_VALIDATE_INT);
            if ($userValue === false) {
                throw new InvalidArgumentException("User ID must be a valid integer or NULL");
            }
        }

        $query=sprintf("INSERT INTO Input(module, command, result, sort, user) VALUES('%s', '%s', '%s', '%s', '%s')"
            , $conn->real_escape_string($input->module)
            , $conn->real_escape_string($input->command)
            , $conn->real_escape_string($input->result)
            , $conn->real_escape_string($input->sort)
            ,$userValue);

        if ( $conn->query($query) ) {
            $input->id = $conn->insert_id;
        } else {
            echo "Error al insertar en la BD: (" . $conn->errno . ") " . utf8_encode($conn->error);
            exit();
        }
        return $input;
    }*/

    private static function insert($input) {
        $app = Aplicacion::getSingleton();
        $conn = $app->conexionBd();
        
        $query = "INSERT INTO Input(module, command, result, error, sort, session_id, user) VALUES(?, ?, ?, ?, ?, ?, ?)";
        $stmt = $conn->prepare($query);
        
        if ($stmt === false) {
            throw new Exception("Error preparing statement: " . $conn->error);
        }
        
        $userValue = is_null($input->user) ? null : filter_var($input->user, FILTER_VALIDATE_INT);
        if ($userValue === false && !is_null($input->user)) {
            throw new InvalidArgumentException("User ID must be a valid integer or NULL");
        }
        
        $stmt->bind_param("ssssssi", $input->module, $input->command, $input->result, $input->error, $input->sort, $input->session_id, $userValue);
        
        if ($stmt->execute()) {
            $input->id = $conn->insert_id;
        } else {
            throw new Exception("Error inserting into database: " . $stmt->error);
        }
        
        $stmt->close();
        return $input;
    }
    
    private static function update($input) {
        $app = Aplicacion::getSingleton();
        $conn = $app->conexionBd();
        $query=sprintf("UPDATE Input I SET module = '%s', command='%s', result = '%s', error = '%s', sort = '%s', session_id='%s', user='%s' WHERE I.id=%i"
            , $conn->real_escape_string($input->module)
            , $conn->real_escape_string($input->command)
            , $conn->real_escape_string($input->result)
            , $conn->real_escape_string($input->error)
            , $conn->real_escape_string($input->sort)
            , $conn->real_escape_string($input->session_id)
            , $conn->real_escape_string($input->user)
            , $input->id);
        if ( $conn->query($query) ) {
            if ( $conn->affected_rows != 1) {
                echo "Input could not be updated: " . $input->id;
                exit();
            }
        } else {
            echo "Error al insertar en la BD: (" . $conn->errno . ") " . utf8_encode($conn->error);
            exit();
        }
        
        return $input;
    }

    private $id;
    private $module;
    private $command;
    private $result;
    private $error;
    private $sort;
    private $session_id;
    private $user;

    private function __construct($module, $command, $result, $error, $sort, $session_id, $user = null) {
        $this->module = $module;
        $this->command = $command;
        $this->result = $result;
        $this->error = $error;
        $this->sort = $sort;
        $this->session_id = $session_id;
        $this->user = $user;
    }

    public function id() {
        return $this->id;
    }

    public function module() {
        return $this->module;
    }

    public function command() {
        return $this->command;
    }

    public function result() {
        return $this->result;
    }

    public function error() {
        return $this->error;
    }

    public function sort() {
        return $this->sort;
    }

    public function user() {
        return $this->user;
    }

    public function session_id() {
        return $this->session_id;
    }
}
