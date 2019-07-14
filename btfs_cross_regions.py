from common import result
from common import BtfsCmd

class Regions():
    def __init__(self,node0, node1, node2):
        self.node0 = node0
        self.node1 = node1
        self.node2 = node2

        self.btfs = BtfsCmd()


    @result
    def two_nodes_add_get_file(self):
        """Add and get file on two nodes in different regions (Linux)"""
        #------------------------------------------------------
        #1.On node1, create a file:
        #      $ head -c 10 /dev/urandom | base64 > /tmp/file.txt
        #------------------------------------------------------
        self.node0.exec_btfs_command('head -c 10 /dev/urandom | base64 > /tmp/file.txt')

        tmp_file = self.node0.exec_btfs_command('cat /tmp/file.txt')

        #------------------------------------------------------
        #2.On node1, add file to BTFS:
        #   $ btfs add  /tmp/file.txt
        #------------------------------------------------------
        res = self.node0.exec_btfs_command(self.node0.btfs.with_args('add /tmp/file.txt'))
        arrs = res.split()
        f_hash = arrs[1]


        #------------------------------------------------------
        #3.On node2, get file:
        #   $ btfs get <file_hash> -o file2.txt
        #------------------------------------------------------
        self.node2.exec_btfs_command(self.btfs.with_args('get %s -o file2.txt' % f_hash))

        #------------------------------------------------------
        #4 $ ls -l
        #------------------------------------------------------
        res = self.node2.exec_btfs_command('ls -l')
        if 'file2.txt' not in res:
            raise Exception('file2.txt can not found')

        file2 = self.node2.exec_btfs_command('cat file2.txt')

        if tmp_file != file2:
            raise Exception('/tmp/file.txt and file1.txt content is different')

    @result
    def two_nodes_add_and_cat_file(self):
        """Test Case Name: Add and cat file on two nodes in different regions (Linux)"""

        #------------------------------------------------------
        #1.On node1, create a file:
        #   $ head -c 10 /dev/urandom | base64 > /tmp/file.txt
        #------------------------------------------------------
        self.node0.exec_btfs_command('head -c 10 /dev/urandom | base64 > /tmp/file.txt')

        #------------------------------------------------------
        #2.On node1, add file to BTFS:
        #   $ btfs add  /tmp/file.txt
        #------------------------------------------------------
        res = self.node0.exec_btfs_command(self.node0.btfs.with_args('add /tmp/file.txt'))
        arrs = res.split()
        f_hash = arrs[1]

        #------------------------------------------------------
        #3.On node1, cat local file
        #   $ cat /tmp/file.txt
        #------------------------------------------------------
        tmp_file = self.node0.exec_btfs_command('cat /tmp/file.txt')

        #------------------------------------------------------
        #4.On node2, cat file:
        #   $ btfs cat <file_hash>
        #------------------------------------------------------
        cat_file = self.node2.exec_btfs_command(self.btfs.with_args('cat %s' % f_hash))

        if tmp_file != cat_file:
            raise Exception('/tmp/file.txt and cat content is different')


    @result
    def two_nodes_add_and_cat_large_file(self):
        """Test Case Name: Add and cat a large file(5MB) on two nodes in different regions (Linux)"""
        #------------------------------------------------------
        #1.On node1, create a 5MB size file:
        #   $ head -c 5000000 /dev/urandom | base64 > /tmp/file.txt && md5sum /tmp/file.txt | cut -d ' ' -f 1
        #------------------------------------------------------
        tmp_md5 = self.node0.exec_btfs_command('head -c 5000000 /dev/urandom | base64 > /tmp/file.txt && md5sum /tmp/file.txt | cut -d \' \' -f 1')

        #------------------------------------------------------
        #2.On node1, add file to BTFS:
        #   $ btfs add  /tmp/file.txt
        #------------------------------------------------------
        res = self.node0.exec_btfs_command(self.btfs.with_args('add /tmp/file.txt'))
        arrs = res.split()
        f_hash = arrs[1]

        #------------------------------------------------------
        #3.On node2, cat file:
        #    $ btfs cat <file_hash> | md5sum | cut -d ' ' -f 1
        #------------------------------------------------------
        cat_md5 = self.node2.exec_btfs_command(self.btfs.with_args('cat %s | md5sum | cut -d \' \' -f 1' % f_hash))

        if tmp_md5 != cat_md5:
            raise Exception('md5 and cat md5 is different')

    @result
    def two_nodes_add_and_pin_file(self):
        """Test Case Name: Add and pin file on two nodes in different regions (Linux)"""
        #------------------------------------------------------
        #1.On node1, create a file:
        #   $ head -c 10 /dev/urandom | base64 > /tmp/file.txt
        #------------------------------------------------------
        self.node0.exec_btfs_command('head -c 10 /dev/urandom | base64 > /tmp/file.txt')

        #------------------------------------------------------
        #2.On node1, add file to BTFS:
        #   $ btfs add  /tmp/file.txt
        #------------------------------------------------------
        res = self.node0.exec_btfs_command(self.btfs.with_args('add /tmp/file.txt'))
        arrs = res.split()
        f_hash = arrs[1]

        #------------------------------------------------------
        #3.On node1, cat local file
        #   $ cat /tmp/file.txt
        #------------------------------------------------------
        tmp_content = self.node0.exec_btfs_command('cat /tmp/file.txt')

        #------------------------------------------------------
        #4.On node2, pin file:
        #   $ btfs  pin add  <file_hash>
        #------------------------------------------------------
        self.node2.exec_btfs_command(self.btfs.with_args('pin add %s' % f_hash))

        #------------------------------------------------------
        #5.On node2, cat file:
        #   $ btfs cat <file_hash>
        #------------------------------------------------------
        cat_content = self.node2.exec_btfs_command(self.btfs.with_args('cat %s' % f_hash))

        if cat_content != tmp_content:
            raise Exception('tmp content and cat content is different')

    @result
    def two_nodes_pin_and_remove_pin_file(self):
        """Test Case Name: Pin and Remove pin file on two nodes in different regions (Linux)"""
        #------------------------------------------------------
        #1.On node1, create a file:
        #   $ head -c 10 /dev/urandom | base64 > /tmp/file.txt
        #------------------------------------------------------
        self.node0.exec_btfs_command('head -c 10 /dev/urandom | base64 > /tmp/file.txt')

        #------------------------------------------------------
        #2.On node1, add file to BTFS:
        #   $ btfs add  /tmp/file.txt
        #------------------------------------------------------
        res = self.node0.exec_btfs_command(self.btfs.with_args('add /tmp/file.txt'))
        arrs = res.split()
        f_hash = arrs[1]

        #------------------------------------------------------
        #3.On node1, cat local file
        #   $ cat /tmp/file.txt
        #------------------------------------------------------
        tmp_content = self.node0.exec_btfs_command('cat /tmp/file.txt')

        #------------------------------------------------------
        #4.On node2, pin file:
        #   $ btfs  pin add  <file_hash>
        #------------------------------------------------------
        self.node2.exec_btfs_command(self.btfs.with_args('pin add %s' % f_hash))

        #------------------------------------------------------
        #5.On node1, remove pin:
        #   $ btfs pin rm <file_hash>
        #------------------------------------------------------
        self.node2.exec_btfs_command(self.btfs.with_args('pin rm %s' % f_hash))

        #------------------------------------------------------
        #6.On node1, run GC(garbage collection):
        #   $ btfs repo gc
        #------------------------------------------------------
        self.node2.exec_btfs_command(self.btfs.with_args('repo gc'))

        #------------------------------------------------------
        #7.On node2, cat file:
        #   $ btfs cat <file_hash>
        #------------------------------------------------------
        cat_content = self.node2.exec_btfs_command(self.btfs.with_args('cat %s' % f_hash))

        if cat_content != tmp_content:
            raise Exception('tmp content and cat content is different')


    @result
    def three_nodes_swarm_cross_network_connection(self):
        """Test Case Name: Swarm - cross network connection in different regions (Linux)"""
        #------------------------------------------------------
        #1.On node1, remove all bootstrap peers:
        #   $ btfs bootstrap list
        #   $ btfs bootstrap rm --all
        #   $ btfs bootstrap list
        #------------------------------------------------------
        #   $ btfs bootstrap list
        self.node0.exec_btfs_command(self.btfs.with_args('bootstrap list'))

        #   $ btfs bootstrap rm --all
        self.node0.exec_btfs_command(self.btfs.with_args('bootstrap rm --all'))

        #   $ btfs bootstrap list
        res = self.node0.exec_btfs_command(self.btfs.with_args('bootstrap list'))
        if res != '':
            raise Exception('bootstrap list Bootstrap is not deleted clean')

        #------------------------------------------------------
        #2.On node3, remove all bootstrap peers:
        #   $ btfs bootstrap list
        #   $ btfs bootstrap rm --all
        #   $ btfs bootstrap list
        #------------------------------------------------------
        #   $ btfs bootstrap list
        self.node2.exec_btfs_command(self.btfs.with_args('bootstrap list'))

        #   $ btfs bootstrap rm --all
        self.node2.exec_btfs_command(self.btfs.with_args('bootstrap rm --all'))

        #   $ btfs bootstrap list
        res = self.node2.exec_btfs_command(self.btfs.with_args('bootstrap list'))
        if res != '':
            raise Exception('bootstrap list Bootstrap is not deleted clean')


        #------------------------------------------------------
        #3.On node1, remove all other peers:
        #   $ for node in $(btfs swarm peers); do btfs swarm disconnect $node; done;
        #   $ btfs swarm peers
        #------------------------------------------------------
        #   $ for node in $(btfs swarm peers); do btfs swarm disconnect $node; done;
        self.node0.exec_btfs_command('for node in $(%s swarm peers); do %s swarm disconnect $node; done;' % (self.btfs.cmd_name(),self.btfs.cmd_name()))

        #   $ btfs swarm peers
        self.node0.exec_btfs_command(self.btfs.with_args('swarm peers'))

        #------------------------------------------------------
        #4.On node3, remove all other peers:
        #   $ for node in $(btfs swarm peers); do btfs swarm disconnect $node; done;
        #   $ btfs swarm peers
        #------------------------------------------------------
        #   $ for node in $(btfs swarm peers); do btfs swarm disconnect $node; done;
        self.node2.exec_btfs_command('for node in $(%s swarm peers); do %s swarm disconnect $node; done;' % (self.btfs.cmd_name(),self.btfs.cmd_name()))

        #   $ btfs swarm peers
        self.node2.exec_btfs_command(self.btfs.with_args('swarm peers'))

        #------------------------------------------------------
        #5.On node1,  create a 5MB size file:
        #   $ head -c 5000000 /dev/urandom | base64 > /tmp/file.txt && md5sum /tmp/file.txt | cut -d ' ' -f 1
        #------------------------------------------------------
        tmp_md5 = self.node0.exec_btfs_command('head -c 5000000 /dev/urandom | base64 > /tmp/file.txt && md5sum /tmp/file.txt | cut -d \' \' -f 1')

        #------------------------------------------------------
        #6.On node1, add file to BTFS:
        #   $ btfs add  /tmp/file.txt
        #------------------------------------------------------
        res = self.node0.exec_btfs_command(self.btfs.with_args('add /tmp/file.txt'))
        arrs = res.split()
        f_hash = arrs[1]

        #------------------------------------------------------
        #7.On node2, get connection info:
        #   $ btfs id -f "<addrs>"
        #------------------------------------------------------
        node1_addr = self.node1.exec_btfs_command(self.btfs.with_args('id -f "<addrs>"'))

        #------------------------------------------------------
        #8.On node1, connect to node2:
        #   $ btfs swarm connect <Lan_addr>
        #------------------------------------------------------
        self.node0.exec_btfs_command(self.btfs.with_args('swarm connect %s' % node1_addr))

        #------------------------------------------------------
        #9.On node3, connect to node2:
        #   $ btfs swarm connect <Lan_addr>
        #------------------------------------------------------
        self.node2.exec_btfs_command(self.btfs.with_args('swarm connect %s' % node1_addr))

        #------------------------------------------------------
        #10.On node3, cat file:
        #   $ btfs cat <file_hash> | md5sum | cut -d ' ' -f 1
        #------------------------------------------------------
        cat_md5 = self.node2.exec_btfs_command(self.btfs.with_args('cat %s | md5sum | cut -d \' \' -f 1' % f_hash))
        if cat_md5 != tmp_md5:
            raise Exception('md5 and cat md5 is different')

        #------------------------------------------------------
        #11.Recover bootstrap nodes on node1 and node 3:
        #    $ btfs bootstrap add /ip4/3.14.203.8/tcp/4001/btfs/QmbsqP3GLrRRhGWwnXnb6gb7EFC9LAege333NBpn9cDXAv
        #    $ btfs bootstrap add /ip4/3.14.238.171/tcp/4001/btfs/QmRb1Vi7JeNMVE2QVvCuWFU2J2qt6rn4pLf31CHyjt9GbB
        #    $ btfs bootstrap add /ip4/3.18.120.107/tcp/4001/btfs/QmcmRdAHQYTtpbs9Ud5rNx6WzHmU9WcYCrBneCSyKhMr7H
        #   Run:
        #    $ btfs bootstrap list
        #------------------------------------------------------
        lan_addr_0 = '/ip4/3.14.203.8/tcp/4001/btfs/QmbsqP3GLrRRhGWwnXnb6gb7EFC9LAege333NBpn9cDXAv'
        lan_addr_1 = '/ip4/3.14.238.171/tcp/4001/btfs/QmRb1Vi7JeNMVE2QVvCuWFU2J2qt6rn4pLf31CHyjt9GbB'
        lan_addr_2 = '/ip4/3.18.120.107/tcp/4001/btfs/QmcmRdAHQYTtpbs9Ud5rNx6WzHmU9WcYCrBneCSyKhMr7H'

        self.node0.exec_btfs_command(self.btfs.with_args('bootstrap add %s' % lan_addr_0))
        self.node0.exec_btfs_command(self.btfs.with_args('bootstrap add %s' % lan_addr_1))
        self.node0.exec_btfs_command(self.btfs.with_args('bootstrap add %s' % lan_addr_2))
        #    $ btfs bootstrap list
        res = self.node0.exec_btfs_command(self.btfs.with_args('bootstrap list'))
        if (lan_addr_0 not in res) or (lan_addr_1 not in res) or(lan_addr_2 not in res):
            raise Exception('node0 bootstrap add fail')

        self.node2.exec_btfs_command(self.btfs.with_args('bootstrap add %s' % lan_addr_0))
        self.node2.exec_btfs_command(self.btfs.with_args('bootstrap add %s' % lan_addr_1))
        self.node2.exec_btfs_command(self.btfs.with_args('bootstrap add %s' % lan_addr_2))
        #    $ btfs bootstrap list
        res = self.node0.exec_btfs_command(self.btfs.with_args('bootstrap list'))
        if (lan_addr_0 not in res) or (lan_addr_1 not in res) or(lan_addr_2 not in res):
            raise Exception('node2 bootstrap add fail')





