rewrite ^/(assets|media)/\d/(.+)$
         /$1/$2
         last;
