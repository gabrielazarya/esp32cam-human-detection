<?php
$filename = "hasil.txt";
if (file_exists($filename)) {
    $content = trim(file_get_contents($filename));
    if ($content === "manusia" || $content === "bukan_manusia") {
        echo $content;
    } else {
        echo "unknown"; // fallback
    }
} else {
    echo "error";
}
?>
