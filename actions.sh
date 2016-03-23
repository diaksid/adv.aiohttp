#!/bin/bash


echo  -e "";
source  /var/venv/bin/activate;
echo  -e "> activate";

ac="yes";
acc="yes";

until [ $ac = "-" ]; do
    echo  -e "";
    echo  -e "+ : start";
    echo  -e "7 : memcached restart";
    echo  -e "8 : supervisor restart";
    echo  -e "9 : nginx restart";
    echo  -e "0 : shell";
    echo  -e "* : upgrade all";
    echo  -e "- : deactivate";
    echo  -e "";
    echo  -e "Type \c ";
    read  ac;
    case $ac in
        "+")
            echo  -e "> start";
            ./proxy.py;;


        "7")
            echo  -e "> memcached restart";
            deactivate;
            service memcached restart;
            source /var/venv/bin/activate;;


        "8")
            echo  -e "> supervisor restart";
            deactivate;
            service supervisor restart;
            source /var/venv/bin/activate;;


        "9")
            echo  -e "> nginx restart";
            deactivate;
            service nginx restart;
            source /var/venv/bin/activate;;


        "0")
            echo  -e "> shell";
            ./shell.py;;


        "*")
            echo  -e "> upgrade";
            pip install --upgrade pip
            ./upgrade.py;;


        "-")
            echo  -e "> deactivate";
            deactivate;;
    esac
done
