<?php
const CORRECT_CODE = "048116203";
const SLEEP_TIME = 5;
const FLAG = "uhctf{ikwillevenikwilvrijzijn-dac02015}";

function returnJson($json) {
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($json);
    // Very simple brute force prevention
    sleep(5);
    exit(0);
}

if (!isset($_REQUEST["code"])) {
    returnJson((object) [
        '🚨' => 'please provide a code',
        '🏳️' => ''
    ]);
}

if ($_REQUEST["code"] != CORRECT_CODE) {
    returnJson((object) [
        // To make the endpoint more difficult to understand
        '🚨' => '',
        '🏳️' => ''
    ]);
}

returnJson((object) [
    '🚨' => '',
    '🏳️' => FLAG
]);
