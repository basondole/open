# Conjure
> According to the Oxford dictionary conjure means; cause (a spirit or ghost) to appear by means of a magic ritual.

Conjure serves to help network administrator to easily collect configurations from all network devices as specified in the database.
Then creates a table of devices with their corresponding software versions and details providing the network invetory.


## Setup
Conjure requires the administrator to create a device database which is basically a textfile containing the ip addresses
and their corresponing software. 

Database example:
<pre>
C:\Users\u>cat devices.txt
junos   192.168.56.36
ios     192.168.56.26
ios     192.168.56.63

C:\Users\u>
</pre>

## Usage

Run the conjure on the same directory that contains the file `devices.txt`
When the application runs successfully it will generate a directory `backup` in the current directory
where the configurations backup will be stored

<pre>
C:\Users\u>python conjure.py

Config will be extracted from these boxes


+-----+----------------------+----------+
| No  | DEVICE IP            | SOFTWARE |
+-----+----------------------+----------+
| 1   | 192.168.56.36        | junos    |
+-----+----------------------+----------+
| 2   | 192.168.56.26        | ios      |
+-----+----------------------+----------+
| 3   | 192.168.56.63        | ios      |
+-----+----------------------+----------+


SSH LOGIN
-----------------------------------------
USERNAME: paul
PASSWORD:

Please wait...

Completed collecting config from 192.168.56.63   [router-1]
Completed collecting config from 192.168.56.36   [big]


FAILED CONNECTIONS

+-----+----------------------+------------------------------------------------------------------------------------+
| No  | DEVICE IP            | ERROR                                                                              |
+-----+----------------------+------------------------------------------------------------------------------------+
| 1   | 192.168.56.26        | ['ios', 'Cannot connect to 192.168.56.26']                                         |
+-----+----------------------+------------------------------------------------------------------------------------+


RECAP

+-----------+---------------+------------+------------+---------------+-----------------------------+------------+
| HOSTNAME  | DEVICE IP     | VENDOR     | MODEL      | SERIAL        | SOFTWARE                    | UPTIME (s) |
+-----------+---------------+------------+------------+---------------+-----------------------------+------------+
| big       | 192.168.56.36 | Juniper    | OLIVE      | None          | 12.1R1.9                    | 7281       |
+-----------+---------------+------------+------------+---------------+-----------------------------+------------+
| router-1  | 192.168.56.63 | Cisco      | 7206VXR    | 4279256517    | 7200 Software 15.2(4)S5     | 6720       |
+-----------+---------------+------------+------------+---------------+-----------------------------+------------+




SUMMARY
-------

 ! Failed connections: 1
 ! Collected config files: 2/3

 [Finished in 21s]




Support the developer
Cut cheque: bassosimons@me.com
Buy coffee: 255 (0)68 960 7406
Copyright℗: Paul S.I.Basondole



C:\Users\u>

C:\Users\u> ls backup
192.168.56.36_big_2019-11-07T15-54.conf       192.168.56.63_router-1_2019-11-07T15-54.conf

</pre>




