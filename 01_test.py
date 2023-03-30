import os
from common_input import *


def main():
    # Create a new SSH client and connect to the remote VM
    ssh = paramiko.SSHClient ()
    ssh.set_missing_host_key_policy (paramiko.AutoAddPolicy ())
    ssh.connect (ssh_host, ssh_port, ssh_username, ssh_password)

    # Define the command to execute
    oc_login_command = f"oc login --token={oc_token} --server={oc_url}"
    command34 = f"{oc_login_command}; oc get pods -n lifecycle-manager "
    # command1 = "oc get pods -n lifecycle-manager | grep siteplanner"
    stdin, stdout, stderr = ssh.exec_command (command34)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print ("printing pod details")
    print (output)

    pod = "siteplanner"
    print (f"pod status :  {check_pod_status (pod)}")
    if check_pod_status (pod) == 1:
        command4 = "oc patch orchestration default --patch '{\"spec\":{\"advanced\":{\"enableMultiCloudPlugin\": true}}}' --type=merge"
        print (command4)
        stdin, stdout, stderr = ssh.exec_command (command4)
        time.sleep (5)
        output = stdout.read ().decode ('utf-8')
        print (output)
        command2 = "oc delete secret cp4na-o-siteplanner-configuration"
        stdin, stdout, stderr = ssh.exec_command (command2)
        time.sleep (5)
        output = stdout.read ().decode ('utf-8')
        print (output)
        delete_pod_name (pod)
    else:
        print ("Unable to delete secret and pod")

    command2 = "git clone https://github.com/IBM/lmctl.git"
    command3 = "cd lmctl; python3 -m pip install virtualenv ; python3 -m virtualenv env ; source env/bin/activate ; python3 -m pip install --editable . ; lmctl --version"

    stdin, stdout, stderr = ssh.exec_command (command2)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    stdin, stdout, stderr = ssh.exec_command (command3)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    command4 = "lmctl --version"

    stdin, stdout, stderr = ssh.exec_command (command4)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    command5 = 'export ZEN_AUTH_ADDRESS="https://$(oc get route cpd -o jsonpath={.spec.host})/icp4d-api/v1/authorize"'
    command6 = 'export API_GATEWAY="https://$(oc get route cp4na-o-ishtar -o jsonpath={.spec.host})"'
    command7 = f"export API_KEY={API_Key}"
    command8 = "lmctl login $API_GATEWAY --zen --auth-address $ZEN_AUTH_ADDRESS --username admin --api-key $API_KEY"
    command9 = "lmctl ping env default"

    stdin, stdout, stderr = ssh.exec_command (command5)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    stdin, stdout, stderr = ssh.exec_command (command6)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    stdin, stdout, stderr = ssh.exec_command (command7)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    stdin, stdout, stderr = ssh.exec_command (command8)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    stdin, stdout, stderr = ssh.exec_command (command9)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    command10 = "cd ~; mkdir helm; cd helm; wget https://get.helm.sh/helm-v3.2.4-linux-amd64.tar.gz; tar -xzf helm-v3.2.4-linux-amd64.tar.gz ;mv linux-amd64/helm /usr/local/bin/helm ; helm list"
    stdin, stdout, stderr = ssh.exec_command (command10)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    command11 = f"oc create secret generic cp4na-o-wired-credentials --from-literal=keystorePassword='password' --from-literal=mcnp.gateway.zen.userName='admin' --from-literal=mcnp.gateway.zen.apiKey='{API_Key}'"
    stdin, stdout, stderr = ssh.exec_command (command11)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    command12 = "oc get secret cp4na-o-wired-credentials -o yaml"
    stdin, stdout, stderr = ssh.exec_command (command12)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    command14 = 'openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:4096 -keyout private.key -out public.crt -subj "/C=IN/ST=Karnataka/L=Bangalore/O=IBM Ltd/CN=api.cp4na0309.cp.fyre.ibm.com"'
    stdin, stdout, stderr = ssh.exec_command (command14)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    command13 = "cd ~; mkdir ca_certs; cd ca_certs"
    stdin, stdout, stderr = ssh.exec_command (command13)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    ssh = paramiko.SSHClient ()
    ssh.load_host_keys (os.path.expanduser (os.path.join ("~", ".ssh", "known_hosts")))
    ssh.connect (ssh_host, ssh_port, ssh_username, ssh_password)
    sftp = ssh.open_sftp ()
    sftp.put ("/Users/athikhak1/MCNP_automation_Work/ca_certs/AmazonRootCA1.crt", "/root/ca_certs/AmazonRootCA1.crt")
    sftp.put ("/Users/athikhak1/MCNP_automation_Work/ca_certs/AmazonRootCA2.crt", "/root/ca_certs/AmazonRootCA2.crt")
    sftp.put ("/Users/athikhak1/MCNP_automation_Work/ca_certs/AmazonRootCA3.crt", "/root/ca_certs/AmazonRootCA3.crt")
    sftp.put ("/Users/athikhak1/MCNP_automation_Work/ca_certs/AmazonRootCA4.crt", "/root/ca_certs/AmazonRootCA4.crt")
    sftp.put ("/Users/athikhak1/MCNP_automation_Work/ca_certs/AmazonRootCA5.crt", "/root/ca_certs/AmazonRootCA5.crt")
    sftp.put ("/Users/athikhak1/MCNP_automation_Work/ca_certs/Baltimore_CyberTrust_Root.crt",
              "/root/ca_certs/Baltimore_CyberTrust_Root.crt")
    sftp.put ("/Users/athikhak1/MCNP_automation_Work/ca_certs/DigiCert_Global_Root_CA.crt",
              "/root/ca_certs/DigiCert_Global_Root_CA.crt")
    sftp.put ("/Users/athikhak1/MCNP_automation_Work/ca_certs/DigiCert_Global_Root_G2.crt",
              "/root/ca_certs/DigiCert_Global_Root_G2.crt")
    sftp.put ("/Users/athikhak1/MCNP_automation_Work/ca_certs/DigiCert_Global_Root_G3.crt",
              "/root/ca_certs/DigiCert_Global_Root_G3.crt")
    sftp.put ("/Users/athikhak1/MCNP_automation_Work/ca_certs/MicrosoftECCRootCertificate1.crt",
              "/root/ca_certs/MicrosoftECCRootCertificate1.crt")
    sftp.put ("/Users/athikhak1/MCNP_automation_Work/ca_certs/MicrosoftECCRootCertificate2.crt",
              "/root/ca_certs/MicrosoftECCRootCertificate2.crt")
    sftp.put ("/Users/athikhak1/MCNP_automation_Work/Files/idp-certificate.crt.zip", "/root/idp-certificate.crt.zip")
    sftp.put ("/Users/athikhak1/MCNP_automation_Work/Files/cp4nawired.yaml", "/root/cp4nawired.yaml")
    sftp.close ()

    # command13 = "cd ~; cd ca_certs; oc project -n lifecycle-manager"
    # stdin, stdout, stderr = ssh.exec_command (command13)
    # time.sleep (5)
    # output = stdout.read ().decode ('utf-8')
    # print (output)

    command17 = 'cd ~; cd ca_certs; oc project -n lifecycle-manager; oc get secret internal-nginx-svc-tls -o jsonpath="{.data[\'tls\.crt\']}" | base64 -d > cpd-internal.crt'
    stdin, stdout, stderr = ssh.exec_command (command17)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    command18 = 'cd ~; cd ca_certs; oc project -n lifecycle-manager ; oc get secret cp4na-o-ishtar-cert -o jsonpath="{.data[\'tls\.crt\']}" | base64 -d > ishtar.crt'
    stdin, stdout, stderr = ssh.exec_command (command18)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    command19 = 'cd ~; cd ca_certs; oc project -n lifecycle-manager ; oc get secret cp4na-o-siteplanner-cert -o jsonpath="{.data[\'tls\.crt\']}" | base64 -d > siteplanner.crt'
    stdin, stdout, stderr = ssh.exec_command (command19)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    command20 = "cd ~; cd ca_certs; oc project -n lifecycle-manager ; oc create secret generic cp4na-o-wired-trustedcerts --from-file=."
    stdin, stdout, stderr = ssh.exec_command (command20)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    command14 = "cd ~; yum install unzip -y; unzip idp-certificate.crt.zip"
    stdin, stdout, stderr = ssh.exec_command (command14)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    command15 = "oc project lifecycle-manager"
    stdin, stdout, stderr = ssh.exec_command (command15)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    command16 = "oc project lifecycle-manager; oc create secret generic cp4na-o-wired-configs --from-file=idp-metadata.xml --from-file=idp-certificate.crt --from-file=private.key --from-file=public.crt"
    stdin, stdout, stderr = ssh.exec_command (command16)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    command21 = "cd ~ ; oc apply -f cp4nawired.yaml -n lifecycle-manager"
    stdin, stdout, stderr = ssh.exec_command (command21)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    command22 = "oc get CP4NAWired"
    stdin, stdout, stderr = ssh.exec_command (command22)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    pod = "mcnp"
    if check_pod_status (pod) == 1:
        print ("MCNP is running")

    command22 = "oc get routes"
    stdin, stdout, stderr = ssh.exec_command (command22)
    time.sleep (5)
    output = stdout.read ().decode ('utf-8')
    print (output)

    ssh.close ()


if __name__ == "__main__":
    main ()
