<?php
$showNumber = 52;
$page = isset($_GET['page']) && $_GET['page'] > 1 ? $_GET['page'] : 1;
$selectOffset = ($page - 1) * $showNumber;

$db = new PDO('mysql:dbname=wallpaper_pconline;host=127.0.0.1', 'root', '', array(PDO::MYSQL_ATTR_INIT_COMMAND => 'SET NAMES "UTF8"'));
$paperData = $db->query("SELECT * FROM `paper_data` limit {$selectOffset},{$showNumber}", PDO::FETCH_NAMED);

$pconlineUrl = 'http://wallpaper.pconline.com.cn';

$hostsUrl = 'http://mywallpaper.pconline.com.cn';
// have to edit hosts file, redirect mywallpaper.pconline.com.cn -> localhost

include './template/index.php';
