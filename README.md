# btfs-auto-test

### requirements
  - python2.7+ installed
  - paramiko installed
    ```
    sudo pip install paramiko
    ```
  - btfs binary
  
    download link：https://github.com/TRON-US/btfs-binary-releases
    
    Choose linux-amd64 version
    
  - ssh private key 
    
    Two ways to get the private key of the login server：
    
      1.And I ask for a private key
      
      2.Use "ssh-keygen -m PEM to" generate a key pair, then append the public key to the server's ~/.ssh/authorized_keys file，cannot use "ssh-genkey" without "-m PEM" because paramiko does not recognize private keys generated using "ssh-genkey" without "-m PEM"
    
  - make sure that binary and xxxx_identity_file specified in these configurations exist on your system
    ```python
    #btfs binary to be installed
    binary = '/Users/tron/btfs-test/btfs-binary'

    #east asia hk node
    node0_hostname = 'btfs-hk-test1.eastasia.cloudapp.azure.com'
    node0_username = 'btfs_admin'
    node0_identity_file = '/Users/tron/btfs-test/id_rsa_btfs_zym'

    #west us node
    node1_hostname = 'btfs-us-test1.westus2.cloudapp.azure.com'
    node1_username = 'btfs_admin'
    node1_identity_file = '/Users/tron/btfs-test/id_rsa_btfs_zym'

    #east us node
    node2_hostname = 'btfs-us-test2.eastus2.cloudapp.azure.com'
    node2_username = 'btfs_admin'
    node2_identity_file = '/Users/tron/btfs-test/id_rsa_btfs_zym'
    ```
     
### usage
    python start.py

### output of test results
```shell
0.Initialize three nodes
    |---->0.Initialize node test environment                                               success
    |---->1.Initialize node test environment                                               success
    |---->2.Initialize node test environment                                               success
1.Install BTFS to all nodes
    |---->0.Install BTFS (Linux)                                                           success
    |---->1.Install BTFS (Linux)                                                           success
    |---->2.Install BTFS (Linux)                                                           success
2.Show version (Linux)                                                                     success
3.Show and change config (Linux)                                                           success
4.Start BTFS daemon for all nodes
    |---->0.Start BTFS daemon (Linux)                                                      success
    |---->1.Start BTFS daemon (Linux)                                                      success
    |---->2.Start BTFS daemon (Linux)                                                      success
5.Add and get file on one node (Linux)                                                     success
6.Add and get file on two nodes in different regions (Linux)                               success
7.Add and cat file on one node (Linux)                                                     success
8.Test Case Name: Add and cat file on two nodes in different regions (Linux)               success
9.Test Case Name: Add and cat a large file(5MB) on two nodes in different reg...           success
10.Test Case Name: Add and pin file on two nodes in different regions (Linux)              success
11.Test Case Name: Pin and Remove pin file on two nodes in different regions ...           success
12.Test Case Name: Add and list directory and file on one node (Linux)                     success
13.Test Case Name: Mount and unmount BTFS to local file system (Linux)                     success
14.Test Case Name: Publish and resolve IPNS names  (Linux)                                 success
15.Test Case Name: Show stats (Linux)                                                      success
16.Test Case Name: Add file and get DAG (Linux)                                            success
17.Test Case Name: API - show node id (Linux)                                              success
18.Test Case Name: API - add and get file on one node (Linux)                              success
19.Test Case Name: Swarm - cross network connection in different regions (Linux)           success
20.key gen ecdsa key pair to publish                                                       success
21.Stop BTFS daemon for all nodes
    |---->0.Stop BTFS daemon (Linux)                                                       success
    |---->1.Stop BTFS daemon (Linux)                                                       success
    |---->2.Stop BTFS daemon (Linux)                                                       success
```

### output detailed execution process

```
cd btfs-auto-test
tail -f deail.log
```

```
14-40-2019 15:40:40 paramiko.transport:INFO:Connected (version 2.0, client OpenSSH_7.6p1)
14-40-2019 15:40:40 paramiko.transport:INFO:Authentication (publickey) successful!
14-40-2019 15:40:41 paramiko.transport.sftp:INFO:[chan 0] Opened sftp connection (server version 3)
14-40-2019 15:40:42 paramiko.transport:INFO:Connected (version 2.0, client OpenSSH_7.6p1)
14-40-2019 15:40:43 paramiko.transport:INFO:Authentication (publickey) successful!
14-40-2019 15:40:44 paramiko.transport.sftp:INFO:[chan 0] Opened sftp connection (server version 3)
14-40-2019 15:40:45 paramiko.transport:INFO:Connected (version 2.0, client OpenSSH_7.6p1)
14-40-2019 15:40:47 paramiko.transport:INFO:Authentication (publickey) successful!
14-40-2019 15:40:48 paramiko.transport.sftp:INFO:[chan 0] Opened sftp connection (server version 3)
14-40-2019 15:40:48 root:INFO:-------------------->Initialize node test environment<-------------------
14-40-2019 15:40:48 root:INFO:btfs-hk-test1.eastasia.cloudapp.azure.com=>$ps -aux | grep "btfs daemon" | grep -v "grep"
14-40-2019 15:40:58 root:INFO:btfs-hk-test1.eastasia.cloudapp.azure.com=>$rm -rf *
14-41-2019 15:41:08 root:INFO:btfs-hk-test1.eastasia.cloudapp.azure.com=>$rm -rf btfs/bin
14-41-2019 15:41:18 root:INFO:btfs-hk-test1.eastasia.cloudapp.azure.com=>$rm -rf ~/.btfs
14-41-2019 15:41:29 root:INFO:btfs-hk-test1.eastasia.cloudapp.azure.com=>$sudo rm -rf /btfs
14-41-2019 15:41:39 root:INFO:btfs-hk-test1.eastasia.cloudapp.azure.com=>$sudo rm -rf /btns
14-41-2019 15:41:49 root:INFO:-------------------->success<-------------------
14-41-2019 15:41:49 root:INFO:-------------------->Initialize node test environment<-------------------
14-41-2019 15:41:49 root:INFO:btfs-us-test1.westus2.cloudapp.azure.com=>$ps -aux | grep "btfs daemon" | grep -v "grep"
14-41-2019 15:41:49 root:INFO:btfs-us-test1.westus2.cloudapp.azure.com=>$rm -rf *
14-41-2019 15:41:50 root:INFO:btfs-us-test1.westus2.cloudapp.azure.com=>$rm -rf btfs/bin
14-41-2019 15:41:51 root:INFO:btfs-us-test1.westus2.cloudapp.azure.com=>$rm -rf ~/.btfs
14-41-2019 15:41:52 root:INFO:btfs-us-test1.westus2.cloudapp.azure.com=>$sudo rm -rf /btfs
14-41-2019 15:41:52 root:INFO:btfs-us-test1.westus2.cloudapp.azure.com=>$sudo rm -rf /btns
14-41-2019 15:41:53 root:INFO:-------------------->success<-------------------
........
```
