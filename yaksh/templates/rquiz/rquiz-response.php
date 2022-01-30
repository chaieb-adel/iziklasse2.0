<?php

// NO PHP OUTPUT TO THE BROWSER BEFORE THIS SCRIPT!!!

$r = 17;
//$r = "Why did you need this may attempts?";

// save submitted data
file_put_contents('./request.txt', print_r($_REQUEST, true), FILE_APPEND);

// send response
header('Content-Type: text/plain; charset=utf-8');

// fake slow connection
sleep(4); // wait 4 seconds

// OUTPUT AFTER HEADER() CALL
echo $r;

exit;
