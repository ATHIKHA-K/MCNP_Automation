import paramiko
import time

oc_url = "https://api.java17off.cp.fyre.ibm.com:6443"
oc_token = "sha256~rAnPArUf0Ar48duGchW1Nik1DnS_SE0HHYYwep0HM5M"
API_Key = "knEqhGLitXgyEKMnH8CbXObf0vS89pcUkEqJmflO"


ssh_host = "api.java17off.cp.fyre.ibm.com"
ssh_port = 22
ssh_username = "root"
ssh_password = "Testing@987654321"


def check_pod_status(pod_name):
    com = f"oc get pods -n lifecycle-manager | grep {pod_name}"
    # Create a new SSH client and connect to the remote VM
    if pod_name == "siteplanner":
        ready = "2/2"
    else:
        ready = "1/1"
    ssh = paramiko.SSHClient ()
    ssh.set_missing_host_key_policy (paramiko.AutoAddPolicy ())
    ssh.connect (ssh_host, ssh_port, ssh_username, ssh_password)
    stdin, stdout, stderr = ssh.exec_command(com)
    time.sleep(5)
    output1 = stdout.read().decode('utf-8')
    print(output1)
    str = output1.split()
    print(len(str))
    print(str[0])
    print(str[1])
    print(str[2])
    print(str[3])
    flag = 0
    while (1):
        print(flag)
        stdin, stdout, stderr = ssh.exec_command(com)
        time.sleep(5)
        output1 = stdout.read().decode('utf-8')
        print(output1)
        str = output1.split()
        print(str[2])
        if str[2] == "Running" and str[1] == ready:
            flag = 1
            break
        time.sleep(5)
    if flag == 1:
        return 1
    else:
        return 0


def delete_pod_name(pod_name):
    com = f"oc get pods -n lifecycle-manager | grep {pod_name}"

    # Create a new SSH client and connect to the remote VM
    ssh = paramiko.SSHClient ()
    ssh.set_missing_host_key_policy (paramiko.AutoAddPolicy ())
    ssh.connect (ssh_host, ssh_port, ssh_username, ssh_password)
    stdin, stdout, stderr = ssh.exec_command(com)
    time.sleep(5)
    output1 = stdout.read().decode('utf-8')
    print(output1)
    str = output1.split()
    print(str[0])
    command3 = f"oc delete pod -n lifecycle-manager {str[0]}"
    stdin, stdout, stderr = ssh.exec_command(command3)
    time.sleep(5)
    output = stdout.read().decode('utf-8')
    print(output)
    time.sleep(5)
    if check_pod_status(pod_name) == 1:
        print(f"{pod_name} is running")