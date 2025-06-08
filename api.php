<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: text/plain');

$data = json_decode(file_get_contents('php://input'), true);
if (!isset($data['imageData'])) { echo "No imageData"; exit; }

$img = preg_replace('/^data:image\/\w+;base64,/', '', $data['imageData']);
$img = base64_decode($img);
$fp = 'upload/input.jpg';
file_put_contents($fp, $img);

$output = shell_exec("python predict.py " . escapeshellarg($fp) . " 2>&1");
$output = trim($output);
file_put_contents('status.txt', $output);

echo $output;
