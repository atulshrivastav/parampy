===============
parampy
===============

Paramiko utility in Python.

.. Built-In Modules::

    paramiko
    time

The main use cases of the library are:

* Nested ssh.

* sudoer ssh.

* Switch ssh.


Usage
-----

The module provides three main functionality:-

* Nested ssh.

* sudoer ssh.

* Switch ssh.


Examples in this file use Python2.7.


Nested ssh
-----

To perform nested ssh user need to import SSHTool class from parampy::

    >>> from parampy import SSHTool
    >>> host = ('127.0.0.1', 22)
    >>> via_host = ('192.168.2.4', 22)
    >>> command = 'ls -ltr'
    >>> ssht = SSHTool(host, 'tmpuser', 'pass', via=via_host, via_user='viauser, via_auth='pass')
    >>> output = ssht.run(command)
    
    --------  --------  -------------------
    -rwxrwxrwx 1 max max      0 May 25 23:30 __init__.py
    -rwxrwxr-x 1 max max   1321 Jul  7 23:22 accordion.js
    drwxrwxr-x 2 max max   4096 Jul  7 23:22 img
    -rwxrwxr-x 1 max max   2970 Jul  7 23:22 demo.css
    -rwxrwxr-x 1 max max  47861 Jul  7 23:22 defaults.css

If user want to pause for sometime if commanexecution in host is taking time he can pass time value while
calling run method::

    >>> ssht.run(command)

sudoer ssh
-----

To perform sudoer ssh means if user want to ssh on some host and host is asking password or expecting any key from user,
user can import sudo_ssh from parampy::

    >>> from parampy import sudo_ssh
    >>> command = 'ls -ltr'
    >>> output = sudo_ssh(ip, user, password, command, sudo_pass='test@123')
    
    --------  --------  -------------------
    -rwxrwxrwx 1 max max      0 May 25 23:30 __init__.py
    -rwxrwxr-x 1 max max   1321 Jul  7 23:22 accordion.js
    drwxrwxr-x 2 max max   4096 Jul  7 23:22 img
    -rwxrwxr-x 1 max max   2970 Jul  7 23:22 demo.css
    -rwxrwxr-x 1 max max  47861 Jul  7 23:22 defaults.css

Switch ssh
-----

To perform ssh in switch and execute some commands,
user can import ssh_switch from parampy::

    >>> from parampy import ssh_switch
    >>> command = ['interconnect bay3', 'test@123']
    >>> output = (ip, user, password, timeout=30, command)
    
    --------  --------     -------------------
    switch_ip 127.32.33.44 connected

Contributors
------------

Atul Shrivastav, Mikhilesh Sekhar.