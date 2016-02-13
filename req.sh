function login {
    curl -vv \
    -c "/home/ael/cookie" \
    --data "<request><Username>admin</Username><Password>admin</Password></request>" \
    "http://192.168.1.1/api/login"
}

function reboot {
    curl -vv \
    -b "/home/ael/cookie" \
    --data "CMD=reboot" \
    "http://192.168.1.1/apply.cgi"
}

function logout {
    curl -vv \
    -b "/home/ael/cookie" \
    --data "<request>1</request>" \
    "http://192.168.1.1/api/logout"
}

login
#reboot
logout

