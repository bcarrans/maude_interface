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
        
        $result = "a";
        #$result = shell_exec("/opt/venv/bin/python3 " . escapeshellarg($python_script_path) . " " . escapeshellarg($maude_module) . " " . escapeshellarg($maude_command) . " 2>&1");

        #$result = shell_exec("python3 " . $python_script_path . " \"$maude_module\" \"$maude_command\"");
        #$result = shell_exec('python3 includes/script.py' . " \"$maude_module\" \"$maude_command\"");

        if($result == "a"){
            $resultArray = "m" . "<!-- SPLIT -->" . "c" . "<!-- SPLIT -->" . "p" . "<!-- SPLIT -->" . "s" . "<!-- SPLIT -->" . "ugh";
        }
        else{
            $resultArray = explode("<!-- SPLIT -->", "R: " . $result . "<!-- SPLIT -->" . "Empty command" . "<!-- SPLIT -->" . "No params" . "<!-- SPLIT -->" . "Nopes" . "<!-- SPLIT -->" . "Nopes");
            //$resultArray = explode("<!-- SPLIT -->", $result);
        }
        
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
                $input = new Input($fila['module'], $fila['command'], $fila['result'], $fila['sort'], $fila['user']);
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

    public static function getSessionInputs() {
        $app = Aplicacion::getSingleton();
        $conn = $app->conexionBd();
        $query = "SELECT * FROM Input";
        $rs = $conn->query($query);
        $inputs = [];
        if ($rs) {
            while ($fila = $rs->fetch_assoc()) {
                $input = new Input($fila['module'], $fila['command'], $fila['result'], $fila['sort'], $fila['user']);
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
                $input = new Input($fila['module'], $fila['command'], $fila['result'], $fila['sort'], $fila['user']);
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
    
    public static function create($module, $command, $result, $sort, $user) {
        $input = new Input($module, $command, $result, $sort, $user);
        return self::save($input);
    }
    
    public static function save($input) {
        if ($input->id !== null) {
            return self::update($input);
        }
        return self::insert($input);
    }
    
    private static function insert($input) {
        $app = Aplicacion::getSingleton();
        $conn = $app->conexionBd();
        $query=sprintf("INSERT INTO Input(module, command, result, sort, user) VALUES('%s', '%s', '%s', '%s', '%s')"
            , $conn->real_escape_string($input->module)
            , $conn->real_escape_string($input->command)
            , $conn->real_escape_string($input->result)
            , $conn->real_escape_string($input->sort)
            , $conn->real_escape_string($input->user));
        if ( $conn->query($query) ) {
            $input->id = $conn->insert_id;
        } else {
            echo "Error al insertar en la BD: (" . $conn->errno . ") " . utf8_encode($conn->error);
            exit();
        }
        return $input;
    }
    
    private static function update($input) {
        $app = Aplicacion::getSingleton();
        $conn = $app->conexionBd();
        $query=sprintf("UPDATE Input I SET module = '%s', command='%s', result = '%s', sort = '%s', user='%s' WHERE I.id=%i"
            , $conn->real_escape_string($module->module)
            , $conn->real_escape_string($command->command)
            , $conn->real_escape_string($user->result)
            , $conn->real_escape_string($input->sort)
            , $conn->real_escape_string($user->user)
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
    private $sort;
    private $user;

    private function __construct($module, $command, $result, $sort, $user = null) {
        $this->module = $module;
        $this->command = $command;
        $this->result = $result;
        $this->sort = $sort;
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

    public function sort() {
        return $this->sort;
    }

    public function user() {
        return $this->user;
    }
}
