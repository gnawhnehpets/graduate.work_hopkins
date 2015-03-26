<?php
header("Content-Type: application/json");
$var1 = $_POST["var1"];
$var2 = $_POST["var2"];
$jsonData = '{ "obj1":{ "propertyA":"'.$var1.'", "propertyB":"'.$var2.'" } }';
echo $jsonData;
?>