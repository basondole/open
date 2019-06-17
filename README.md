# hocid
Huawei OLT ConfIg Differ

This tool uses ssh to gather configuration and user logs from Huawei OLT via SSH and mail the diff to the specified mail

Specify OLTs and their respective hostnames under the __main__ section of the code

SSH username and password for OLT login can be specified under  __main__ section of the code

E-mail account configuration for mail notification can be specified in the mail function

Can be used with crontab to automate the process as per user requirement

Setup
Create a backups folder in your working directory, this folder will be used to store the backups. The working directory should contain the below entries

    [root@basonation basoman]# ls -l  
    drwxr-xr-x 2 root root 40960 Jun 17 16:05 backups  
    -rw-r--r-- 1 root root  7550 Jun 17 10:37 hocid.py
