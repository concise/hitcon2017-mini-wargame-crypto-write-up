# HITCON2017 Mini Wargame Write-up: Crypto

### Problem

A secret makes a crypto crypto

    nc pwnhub.tw 12345

Your goal is to get the flag

### Attachment

- [prob.py](prob.py)

With the script, you can run your own instance of the problem server with some
commands like these:

    $ dd if=/dev/urandom count=1 bs=16 2> /dev/null > key.txt
    $ echo "hitcon{$( dd if=/dev/urandom count=1 bs=256 2> /dev/null | LC_ALL=C tr -d -c 'a-zA-Z0-9_' | head -c 16 )}" > flag.txt
    $ python2.7 -m pip install pycrypto
    $ netcat -k -l -p 12345 -c 'python2.7 prob.py'
