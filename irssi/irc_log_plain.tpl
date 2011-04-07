<?php

$b = (isset($_GET['b']) && is_numeric($_GET['b'])) ? $_GET['b'] + 1 : 1;

echo <<<EOD
<!doctype html>
<html>
<head>
        <title>$doc_title</title>
</head>
<style>
pre {
 overflow-x: auto; white-space: pre-wrap; white-space: -moz-pre-wrap !important;
 white-space: -pre-wrap; white-space: -o-pre-wrap; word-wrap: break-word;
}
</style>
<body>
        <h2>$doc_title</h2>
        <pre>$log_content</pre>
<a href="?b=$b">older</a> <a href="/topics/">topics</a>
</body>
</html>
EOD;

?>
