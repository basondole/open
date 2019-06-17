# hocid
Huawei OLT ConfIg Differ
This tool uses ssh to gather configuration and user logs from Huawei OLT via SSH and mail the diff to the specified mail

Specify OLTs and their respective hostnames under the __name__ == __main__ section
SSH username and password for OLT login can be specified under __name__ == __main__ section

email configuration can be specified in the mail function
