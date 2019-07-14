import paramiko
import time
from common import rlog
from common import result
from common import BtfsCmd
import json






class BtfsNode():

    def __init__(self, hostname, username, password = None, key_filename=None):

        self.node_name = hostname
        self.host_name = hostname
        self.user_name = username
        self.version = ''
        self.private_key = None
        self.btfs_cmd_interval = 0

        #init ssh client
        self.client = paramiko.SSHClient()

        self.btfs = BtfsCmd()

        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.client.connect(hostname=hostname, port=22, username=username, password=password, key_filename=key_filename)

        #open ssh sftp
        self.sftp = self.client.open_sftp()

    def set_btfs_cmd_interval(self, t):
        self.btfs_cmd_interval = t

    def set_private_key(self, key_string):
        self.private_key = key_string

    def set_version(self, v):
        self.version = v

    def close(self):
        self.client.close()

    def exec_btfs_command(self, cmd, args = None):
        rlog.info('%s=>$%s' %(self.host_name, cmd))

        _, stdout, stderr = self.client.exec_command(cmd)
        out = stdout.read().replace('\n', '')
        err = stderr.read().replace('\n', '')
        if out != '':
            rlog.info('[stdout]:%s' % (out))
        if err != '':
            rlog.error('[stderr]:\n%s' % err)

        #The command interval should not be too short
        if self.btfs_cmd_interval > 0:
            time.sleep(self.btfs_cmd_interval)

        """
        if err != '':
            raise Exception("exec command %s" % err)
        else:
            pass
        """

        return out

    @result
    def reset(self):
        """Initialize node test environment"""
        #confirm if there is still a btfs process
        res = self.exec_btfs_command('ps -aux | grep "btfs daemon" | grep -v "grep"')
        if res != '':
            arrs = res.split()
            pid = arrs[1]
            self.exec_btfs_command('kill %s' % pid)

        self.exec_btfs_command('rm -rf *')
        self.exec_btfs_command('rm -rf btfs/bin')
        self.exec_btfs_command('rm -rf ~/.btfs')
        self.exec_btfs_command('sudo rm -rf /btfs')
        self.exec_btfs_command('sudo rm -rf /btns')



    @result
    def install_btfs_from_binary(self, binary):
        """Install BTFS (Linux)"""

        self.client.exec_command('mkdir -p btfs/bin')

        self.client.open_sftp().put(binary, 'btfs/bin/btfs')

        self.sftp.chmod('btfs/bin/btfs', 0755)

        #btfs init
        init_cmd = 'init'
        if self.private_key != None:
            init_cmd = init_cmd + '-i=%s' % self.private_key

        res = self.exec_btfs_command(self.btfs.with_args('init'))
        if not res.endswith('readme'):
            raise


    @result
    def version_test(self):
        """Show version (Linux)"""

        res = self.exec_btfs_command(self.btfs.with_args("version"))
        if not res.endswith(self.version):
            raise Exception("btfs binary version is incorrect")

    @result
    def config_test(self):
        """Show and change config (Linux)"""
        #check if FilestoreEnabled is false
        res = self.exec_btfs_command(self.btfs.with_args('config show | grep FilestoreEnabled'))
        if not res.endswith('false,'):
            raise Exception("FilestoreEnabled not false")

        #change config of FilestoreEnabled
        self.exec_btfs_command(self.btfs.with_args('config Experimental.FilestoreEnabled true --json'))

        #check if FilestoreEnabled is true
        res = self.exec_btfs_command(self.btfs.with_args('config show | grep FilestoreEnabled'))
        if not res.endswith('true,'):
            raise Exception("FilestoreEnabled not true")

    @result
    def start_daemon(self):
        """Start BTFS daemon (Linux)"""
        #confirm if there is still a btfs process
        res = self.exec_btfs_command('ps -aux | grep "btfs daemon" | grep -v "grep"')
        if res != '':
                raise  Exception('The previous daemon process did not close, please check')

        #start daemon
        res = self.exec_btfs_command(self.btfs.nohup_with_args("daemon > log.txt 2>&1 &"))
        time.sleep(5)
        res = self.exec_btfs_command('tail log.txt -n 1')
        if not res.endswith('Daemon is ready'):
            raise Exception('Daemon is not ready')


    @result
    def one_node_get_set_file_test(self):
        """Add and get file on one node (Linux)"""

        #------------------------------------------------------
        #1.Create a file:
        #   $head -c 10 /dev/urandom | base64 > /tmp/file.txt
        #------------------------------------------------------
        self.exec_btfs_command('head -c 10 /dev/urandom | base64 > /tmp/file.txt')

        tmp_file = self.exec_btfs_command('cat /tmp/file.txt')

        #------------------------------------------------------
        #2.Add file to BTFS:
        #   $btfs add  /tmp/file.txt
        #------------------------------------------------------
        res = self.exec_btfs_command(self.btfs.with_args('add /tmp/file.txt'))

        arrs = res.split()
        f_hash = arrs[1]

        #------------------------------------------------------
        #3. Get file just added:
        #   $btfs get <file_hash>
        #------------------------------------------------------
        self.exec_btfs_command(self.btfs.with_args('get %s' % f_hash))

        #------------------------------------------------------
        #4.$ls -l
        res = self.exec_btfs_command('ls')
        #------------------------------------------------------

        #Check if the file exists
        if f_hash not in res:
            raise Exception('can not find: %s' % f_hash)

        #------------------------------------------------------
        #5.Get the file and save to another name
        #   $btfs get <file_hash> -o file1.txt
        #------------------------------------------------------
        f_name = 'file1.txt'
        self.exec_btfs_command(self.btfs.with_args('get %s -o %s' % (f_hash, f_name)))


        #check if the file exists
        res = self.exec_btfs_command('ls')

        if f_name not in res:
            raise Exception('can not find: %s' % f_name)

        #check if the contents of /tmp/file.txt and file1.txt is the same.
        file = self.exec_btfs_command('cat %s' % f_name)
        if tmp_file != file:
            raise  Exception('/tmp/file.txt and file1.txt content is different')

    @result
    def one_node_add_and_cat_file(self):
        """Add and cat file on one node (Linux)"""
        #------------------------------------------------------
        #1.Create a file:
        #   $head -c 10 /dev/urandom | base64 > /tmp/file.txt
        #------------------------------------------------------
        self.exec_btfs_command('head -c 10 /dev/urandom | base64 > /tmp/file.txt')

        #------------------------------------------------------
        #2.Add file to BTFS:
        #   $btfs add  /tmp/file.txt
        #------------------------------------------------------
        res = self.exec_btfs_command(self.btfs.with_args('add  /tmp/file.txt'))
        arrs = res.split()
        f_hash = arrs[1]

        #------------------------------------------------------
        #3.Cat local file and file just added to BTFS
        #   $cat /tmp/file.txt
        #   $btfs cat <file_hash>
        #------------------------------------------------------
        #cat /tmp/file.txt
        tmp_file = self.exec_btfs_command('cat /tmp/file.txt')

        #btfs cat <file_hash>
        cat_file = self.exec_btfs_command(self.btfs.with_args('cat %s' % f_hash))

        #check if the contents of /tmp/file.txt and cat content is the same.
        if tmp_file != cat_file:
            raise Exception('/tmp/file.txt and cat content is different')


    @result
    def one_node_add_and_list_dir(self):
        """Test Case Name: Add and list directory and file on one node (Linux)"""

        #------------------------------------------------------
        #1.Create directory:
        #       $mkdir -p testData testData/dir1
        #  Create file:
        #       $echo "test" > testData/file1
        #       $head -c 10 /dev/urandom | base64 > testData/dir1/file2
        #       $ls -l testData
        #       $ls -l testData/dir1
        #------------------------------------------------------
        # mkdir -p testData testData/dir1
        self.exec_btfs_command('mkdir -p testData testData/dir1')

        # echo "test" > testData/file1
        self.exec_btfs_command('echo "test" > testData/file1')

        # head -c 10 /dev/urandom | base64 > testData/dir1/file2
        self.exec_btfs_command('head -c 10 /dev/urandom | base64 > testData/dir1/file2')

        # ls -l testData
        res = self.exec_btfs_command('ls -l testData')
        if 'file1' not in res:
            raise Exception('can not find file:file1')

        # ls -l testData/dir1
        res = self.exec_btfs_command('ls -l testData/dir1')
        if 'file2' not in res:
            raise Exception('can not find file: file2')

        #------------------------------------------------------
        #2.Add directory to BTFS:
        #       $ btfs add -r testData
        #------------------------------------------------------

        # btfs add -r testData
        #   testData
        #   | __
        #       file1
        #   | __dir1
        #       | __file2
        res = self.exec_btfs_command(self.btfs.with_args('add -r testData'))
        arrs = res.split()

        file2_hash = arrs[1]                #hash of /testData/dir/file2
        file1_hash = arrs[3]                #hash of testData/file1
        dir1_hash = arrs[5]                 #hash of testData/dir1
        testData_hash = arrs[7]             #hash of testData

        #------------------------------------------------------
        #3.List directory just added:
        #       $ btfs ls <testData_hash>
        #------------------------------------------------------
        res = self.exec_btfs_command(self.btfs.with_args('ls %s' % testData_hash))
        if file1_hash not in res:
            raise Exception('file1 is not in the result of btfs ls <testData_hash>')

        if dir1_hash not in res:
            raise Exception('dir1 is not in the result of btfs ls <testData_hash>')

        #------------------------------------------------------
        #4.List sub-directory just added:
        #       $ btfs ls <dir1_hash>
        #------------------------------------------------------
        res = self.exec_btfs_command(self.btfs.with_args('ls %s' % dir1_hash))
        if file2_hash not in res:
            raise Exception('file2 is not in the result of btfs ls <dir hash>')


    @result
    def mount_and_unmount_btfs_to_local_fs(self):
        """Test Case Name: Mount and unmount BTFS to local file system (Linux)"""

        #------------------------------------------------------
        #1.Mount BYFS:
        #    $sudo mkdir /btfs /btns
        #    $sudo chown `whoami` /btfs /btns
        #    $btfs mount
        #------------------------------------------------------

        #sudo mkdir /btfs /btns
        self.exec_btfs_command('sudo mkdir /btfs /btns')

        #sudo chown `whoami` /btfs /btns
        self.exec_btfs_command('sudo chown `whoami` /btfs /btns')

        #btfs mount
        self.exec_btfs_command(self.btfs.with_args('mount'))

        #------------------------------------------------------
        #2.ls -l /:
        #------------------------------------------------------
        res = self.exec_btfs_command('ls -l /')
        if ('btfs' not in res) or ('btns' not in res):
            raise  Exception('btfs and btns not found')


        #------------------------------------------------------
        #3.Create directory:
        #       $mkdir -p test
        #  Create file
        #       $head -c 10 /dev/urandom | base64 > test/file1
        #       $cat test/file1
        #------------------------------------------------------

        #mkdir -p test
        self.exec_btfs_command('mkdir -p test')

        #head -c 10 /dev/urandom | base64 > test/file1
        self.exec_btfs_command('head -c 10 /dev/urandom | base64 > test/file1')

        #cat test/file1
        file1 = self.exec_btfs_command('cat test/file1')


        #------------------------------------------------------
        #4.Add directory to BTFS:
        #       $ btfs add -r test
        #------------------------------------------------------
        res = self.exec_btfs_command(self.btfs.with_args('add -r test'))
        arrs = res.split()

        test_dir_hash = arrs[3]


        #------------------------------------------------------
        #5.Go to btfs mount dir:
        #       $ cd /btfs/<test_dir_hash>
        #       $ ls -l
        #------------------------------------------------------
        res = self.exec_btfs_command('cd /btfs/%s;ls' % test_dir_hash)
        if 'file1' not in res:
            raise Exception('file1 not found in /btfs/%s' % test_dir_hash)

        #------------------------------------------------------
        #6.Cat file1:
        #       $ cat file1
        #------------------------------------------------------
        cat_file1 = self.exec_btfs_command('cd /btfs/%s;cat file1' % test_dir_hash)
        if cat_file1 != file:
            Exception('file1  and cat content is different')

        #------------------------------------------------------
        #7.Unmount BTFS:
        #       $ cd /
        #       $ fusermount -u /btfs
        #       $ fusermount -u /btns
        #------------------------------------------------------
        self.exec_btfs_command('cd /;fusermount -u /btfs;fusermount -u /btns')


        #------------------------------------------------------
        #8.List directory:
        #       ls -l /
        #------------------------------------------------------
        res = self.exec_btfs_command('ls -l /')
        #if 'btfs' in res:
        #    raise  Exception('btfs still exists')
        #if 'btns' in res:
        #    raise  Exception('btns still exists')

    @result
    def publish_and_resolve_ipns_names(self):
        """Test Case Name: Publish and resolve IPNS names  (Linux)"""
        #------------------------------------------------------
        #1.Create directory:
        #       $ mkdir -p test
        # Create file:
        #       $ head -c 10 /dev/urandom | base64 > test/file1
        #       $ cat test/file1
        #------------------------------------------------------
        # $mkdir -p test
        self.exec_btfs_command('mkdir -p test')

        # $ head -c 10 /dev/urandom | base64 > test/file1
        self.exec_btfs_command('head -c 10 /dev/urandom | base64 > test/file1')

        # $ cat test/file1
        file_content = self.exec_btfs_command('cat test/file1')

        #------------------------------------------------------
        #2.Add directory to BTFS:
        #   $ btfs add -r test
        #------------------------------------------------------
        res = self.exec_btfs_command(self.btfs.with_args('add -r test'))
        arrs = res.split()

        test_dir_hash = arrs[3]

        #------------------------------------------------------
        #3.Publish name:
        #   $ btfs name publish <test_dir_hash>
        #------------------------------------------------------
        res = self.exec_btfs_command(self.btfs.with_args('name publish %s' % test_dir_hash))

        #------------------------------------------------------
        #4.Resolve name:
        #   $ btfs name resolve
        #------------------------------------------------------
        resolve = self.exec_btfs_command(self.btfs.with_args('name resolve'))
        if resolve not in res:
            raise Exception('btfs name resolve fail')

        #------------------------------------------------------
        #5.Modify file1:
        #   $ vi test/file1
        #------------------------------------------------------
        self.exec_btfs_command('echo "hello world" >> test/file1')

        #------------------------------------------------------
        #6.Add to BTFS again:
        #   $ btfs add -r test
        #------------------------------------------------------
        res = self.exec_btfs_command(self.btfs.with_args('add -r test'))
        arrs = res.split()

        test_dir_hash = arrs[3]

        #------------------------------------------------------
        #7.Publish again:
        #   $ btfs  name publish <test_dir_hash>
        #------------------------------------------------------
        res = self.exec_btfs_command(self.btfs.with_args('name publish %s' % test_dir_hash))

        #------------------------------------------------------
        #8.Resolve name again:
        #   $ btfs name resolve
        #------------------------------------------------------
        resolve = self.exec_btfs_command(self.btfs.with_args('name resolve'))
        if resolve not in res:
            raise Exception('btfs name resolve fail')



    @result
    def show_stats(self):
        """Test Case Name: Show stats (Linux)"""
        #------------------------------------------------------
        #1.Show stats:
        #   $ btfs stats bitswap
        #------------------------------------------------------
        res = self.exec_btfs_command(self.btfs.with_args('stats bitswap'))
        if 'dup blocks received' not in res:
            raise Exception('stats bitswap fail')

    @result
    def add_file_and_get_dag(self):
        """Test Case Name: Add file and get DAG (Linux)"""
        #------------------------------------------------------
        #1.Create a file:
        #   $ head -c 10 /dev/urandom | base64 > /tmp/file.txt
        #------------------------------------------------------
        self.exec_btfs_command('head -c 10 /dev/urandom | base64 > /tmp/file.txt')
        file_content = self.exec_btfs_command('cat /tmp/file.txt')

        #------------------------------------------------------
        #2.Add file to BTFS:
        #   $ btfs add  /tmp/file.txt
        #------------------------------------------------------
        res = self.exec_btfs_command(self.btfs.with_args('add  /tmp/file.txt'))
        arrs = res.split()
        file_hash = arrs[1]

        #------------------------------------------------------
        #3.Get file just added:
        #   $ btfs object get <file_hash>
        #------------------------------------------------------
        res = self.exec_btfs_command(self.btfs.with_args('object get %s' % file_hash))
        if file_content not in res:
            raise  Exception('file content not in dag')

    @result
    def api_show_node_id(self):
        """Test Case Name: API - show node id (Linux)"""
        #------------------------------------------------------
        #1. $ curl http://localhost:5001/api/v0/id
        #------------------------------------------------------
        res = self.exec_btfs_command('curl http://localhost:5001/api/v0/id')

        if ('ID' not in res) or ('PublicKey' not in res) \
                or ('Addresses' not in res) or ('AgentVersion' not in res) \
                    or('ProtocolVersion' not in res):
            raise  Exception('the node id retrieved from the API is incorrect ')


    @result
    def one_node_api_add_and_get_file(self):
        """Test Case Name: API - add and get file on one node (Linux)"""
        #------------------------------------------------------
        #1. Create a file:
        #   $ head -c 10 /dev/urandom | base64 > /tmp/file.txt
        #------------------------------------------------------
        self.exec_btfs_command('head -c 10 /dev/urandom | base64 > /tmp/file.txt')

        #------------------------------------------------------
        #2.Show file content:
        #   $ cat /tmp/file.txt
        #------------------------------------------------------
        file_content = self.exec_btfs_command('cat /tmp/file.txt')

        #------------------------------------------------------
        #3.Call API to add file to BTFS:
        #   $ curl -F "file=@/tmp/file.txt" http://127.0.0.1:5001/api/v0/add
        #------------------------------------------------------
        res = self.exec_btfs_command('curl -F "file=@/tmp/file.txt" http://127.0.0.1:5001/api/v0/add')
        text = json.loads(res)
        file_hash = text['Hash']


        #------------------------------------------------------
        #4.Cat file:
        #   $ btfs cat <file_hash>
        #------------------------------------------------------
        file_cmd_cat = self.exec_btfs_command(self.btfs.with_args('cat %s'% file_hash))
        if file_cmd_cat != file_content:
            raise Exception('Content error retrieved from btfs cat')

        #------------------------------------------------------
        #5.Call API to get file:
        #   $ curl -o - http://localhost:5001/api/v0/get?arg=<file_hash>
        #------------------------------------------------------
        file_api_get = self.exec_btfs_command('curl -o - http://localhost:5001/api/v0/get?arg=%s'%file_hash)
        if file_cmd_cat not in file_api_get :
            raise Exception('Content error retrieved from btfs api')


    @result
    def one_node_key_gen_ecdsa(self):
        """key gen ecdsa key pair to publish"""
        #------------------------------------------------------
        #1.Create a file:
        #   $ head -c 10 /dev/urandom | base64 > /tmp/file.txt
        #------------------------------------------------------
        self.exec_btfs_command('head -c 10 /dev/urandom | base64 > /tmp/file.txt')

        #------------------------------------------------------
        #3.Show file content:
        #   $ cat /tmp/file.txt
        #------------------------------------------------------
        tmp_content = self.exec_btfs_command('cat /tmp/file.txt')

        #------------------------------------------------------
        #3.Add file to BTFS:
        #   $ btfs add  /tmp/file.txt
        #------------------------------------------------------
        res = self.exec_btfs_command(self.btfs.with_args('add  /tmp/file.txt'))
        arrs = res.split()
        file_hash = arrs[1]

        #------------------------------------------------------
        #4.Generate an ECDSA key pair
        #   $ btfs key gen -t=ecdsa test-ecdsa
        #------------------------------------------------------
        self.exec_btfs_command(self.btfs.with_args('key gen -t=ecdsa test-ecdsa'))

        #------------------------------------------------------
        #5.Publish name:
        #   $ btfs name publish --key=test-ecdsa <file_hash>
        #------------------------------------------------------
        res = self.exec_btfs_command(self.btfs.with_args('name publish --key=test-ecdsa %s' % file_hash))
        arrs = res.split()
        peer_id = arrs[2].rstrip(':')

        #------------------------------------------------------
        #6.Call API to get file:
        #   $ curl 127.0.0.1:8080/btns/<peer id>
        #------------------------------------------------------
        content = self.exec_btfs_command('curl 127.0.0.1:8080/btns/%s' % peer_id)
        if content != tmp_content:
            raise Exception('content and tmp content is different')



    @result
    def stop_daemon(self):
        """Stop BTFS daemon (Linux)"""
        #------------------------------------------------------
        #1.Shutdown:
        #   $ btfs shutdown
        #------------------------------------------------------

        self.exec_btfs_command(self.btfs.with_args("shutdown"))

        time.sleep(5)

        #------------------------------------------------------
        #1.$ ps -ef | grep btfs
        #------------------------------------------------------
        res = self.exec_btfs_command('ps -aux | grep "btfs daemon" | grep -v "grep"')
        if res != "":
            raise  Exception('btfs daemon did not completely quit')






