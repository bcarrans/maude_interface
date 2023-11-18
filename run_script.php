<?php
chdir(__DIR__);

//$maude_module = str_replace('\n', "\n", $_POST["maude_module"]);

$maude_module = $_POST["maude_module"];
$maude_command = $_POST["maude_command"];

$escaped_maude_module = escapeshellcmd($maude_module);
$escaped_maude_command = escapeshellcmd($maude_command);
file_put_contents("temp_module.txt", $maude_module);
file_put_contents("temp_command.txt", $maude_command);

$result = shell_exec("C:/Python311/python.exe script.py \"$escaped_maude_module\" \"$escaped_maude_command\"");

unlink("temp_module.txt");
unlink("temp_command.txt");

echo $result;
?>


