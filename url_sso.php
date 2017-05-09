<?php
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
    
    define("PLATFORM_URL", "https://inv999abc.docebosaas.com");
    define("SSO_SECRET", "123456");
    
    $username = 'tsung'; //get user name from your system
    $time = time();

    $token = md5($username.','.$time.','.SSO_SECRET);

    $url = PLATFORM_URL.
            '/lms/index.php?r=site/sso&login_user='.
            urlencode($username).
            '&time='.$time.
            '&token='.$token;
    
    //if you want to linnk to a course directly
    //$url .= "&id_course=6";
    
    print_r(PLATFORM_URL);
    print_r("<br>");
    print_r($time);
    print_r("<br>");
    print_r($url);
    print_r("<br>");
    print_r('<a href="'.$url.'">SSO</a>');


