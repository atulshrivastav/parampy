"""This module is used as utility for paramiko.


parampy
------

Paramiko utility in Python.

.. Built-In Modules::

    paramiko
    time

The main use cases of the library are::

    * Nested ssh.

    * sudoer ssh.

    * Switch ssh.



Usage:
-----

The module provides three main functionality::

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

"""

import paramiko as param

import time


def ssh_switch(ip, user, password, timeout=30, *args):
    """Method to called for executing commands in the switch console.

    :param ip:IP address of the switch(managment ip address)
    :param user: Login user name for the switch
    :param password: Login password for the switch
    :param cmd: Command that need to be execute in the switch console
    :return: channel_data
    """
    channel_data = ""
    ssh = param.SSHClient()
    ssh.set_missing_host_key_policy(param.AutoAddPolicy())
    ssh.connect(hostname=ip, username=user, password=password, timeout=timeout, compress=True,
                look_for_keys=False,
                allow_agent=False)
    channel = ssh.invoke_shell()
    channel.settimeout(30)
    for chan in args:
        channel.send(chan)
        channel.send('\n')
    channel.send("quit")
    channel.send("\n")

    while not channel.recv_ready():
        time.sleep(2)

    channel_data += channel.recv(10000)
    return channel_data


class SSHTool():
    """Class for utilty contains method for paramiko by overriding paramiko class.

    Nested ssh is also covered with this class.

    Example:
    ssht = SSHTool(ip_address, user, password)
    output = ssht.run(command)

    Example 1:
        ssht = SSHTool(ip_address, user, password)
        output = ssht.run(command, pause=milicescond)

    .. TODO::
        Need to add authorization with auth_key too.

    .. NOTE::
        If nested ssh pass value should be looks like below -
        host = ('192.168.1.1', 22)
        via_host = ('10.10.10.10', 22)
    """

    def __init__(self, host, user='nfvadmin', auth='HP1nvent',
                 via=None, via_user=None, via_auth=None):
        """Constructor for current class.

        It will initialize the paramiko object. it will create transport object for host.
        After starting client for transport object it will authorize with auth_password,
        by passing user name and password.

        If its a nested ssh it will check via value it will do above process for parent host,
        and with parent host transport object it will create child transport for host.

        Args:
            host (String): IP Address for host
            user (String): Username for host
            auth (String): Password for host
            via (Optional): IP Address for parent host
            via_user (Optional): Username for parent host
            via_auth (Optional): Password for parent host

        """
        if via:
            t0 = param.Transport(via)
            t0.start_client()
            t0.auth_password(via_user, via_auth)
            # setup forwarding from 127.0.0.1:<free_random_port> to |host|
            channel = t0.open_channel('direct-tcpip', host, ('127.0.0.1', 0))
            self.transport = param.Transport(channel)
        else:
            self.transport = param.Transport(host)
        self.transport.start_client()
        self.transport.auth_password(user, auth)

    def run(self, cmd, pause=''):
        """Method will execute command in current channel.

        Args:
            cmd (string): Contains the commands need to execute.
            pause (int): If execution of command is taking time user can pass the interval.

        Return:
            (String): Contains output for executed command.

        Process:
            - This method will open session for current transport channel.
            - It will set the error and output for standerd output.
            - Execute the commands which is passed.
            - Store the output in buffer if channel is ready for recieving.
        """
        ch = self.transport.open_session()
        ch.set_combine_stderr(True)
        ch.exec_command(cmd)
        retcode = ch.recv_exit_status()
        buf = ''
        if pause:
            time.sleep(pause)
        while ch.recv_ready():
            buf += ch.recv(1024)
        return retcode, buf

    def close(self):
        """Close the SSH Transport."""
        self.transport.close()

    def __del__(self):
        """Attempt to clean up if not explicitly closed."""
        self.close()


def sudo_ssh(ip, user, auth, cmd, sudo_pass=''):
    """Method for sudo commands.

    Args:
        ip (string): IP Address for host to connect.
        user (string): User name for host.
        auth (string): Password for host
        sudo_pass (string): Sudo password(optional).

    Return:
        (String) : output of exected command.

    """
    ssh = param.SSHClient()
    ssh.set_missing_host_key_policy(param.AutoAddPolicy())
    ssh.connect(hostname=ip, username=user, password=auth, timeout=30, compress=True,
                look_for_keys=False,
                allow_agent=False)
    (stdin, stdout, stderr) = ssh.exec_command(cmd, get_pty=True)
    stdin.write(sudo_pass + '\n')
    stdin.flush()
    res = stderr.read()
    output = stdout.readlines()
    if res:
        output = res

    return output
