import btfs_node
import btfs_cross_regions
import sys
from common import result
from common import component
from common import rlog

#btfs version to be tested
version = '0.0.4'

#Command execution interval(uint s)
btfs_cmd_interval = 10

#btfs binary to be installed
binary = '/Users/tron/btfs-test/btfs-binary'

#tron private key to test $btfs init -i=<tron-private-key>
private_key = 'c4e84f79f766fbcb9afb88e4e1cb519ab6fb579fb7329a7860f8f6bade4ea0d7'

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





def nodes_init(private_key=None):
    #init hk node
    node0 = btfs_node.BtfsNode(node0_hostname, node0_username, key_filename=node0_identity_file)
    node0.set_version(version)
    node0.set_private_key(private_key)
    node0.set_btfs_cmd_interval(btfs_cmd_interval)

    #init west us node
    node1 = btfs_node.BtfsNode(node1_hostname, node1_username, key_filename=node1_identity_file)
    node1.set_version(version)
    node1.set_private_key(private_key)
    node0.set_btfs_cmd_interval(btfs_cmd_interval)

    #init east us node
    node2 = btfs_node.BtfsNode(node2_hostname, node2_username, key_filename=node2_identity_file)
    node2.set_version(version)
    node2.set_private_key(private_key)
    node0.set_btfs_cmd_interval(btfs_cmd_interval)

    return node0, node1, node2

@component
def nodes_reset(node0, node1, node2):
    """Initialize three nodes"""
    node0.reset()
    node1.reset()
    node2.reset()

@component
def nodes_install_btfs(node0, node1, node2):
    """Install BTFS to all nodes"""
    node0.install_btfs_from_binary(binary)
    node1.install_btfs_from_binary(binary)
    node2.install_btfs_from_binary(binary)

@component
def nodes_start_daemon(node0, node1, node2):
    """Start BTFS daemon for all nodes"""
    node0.start_daemon()
    node1.start_daemon()
    node2.start_daemon()

@component
def stop_daemon(node0, node1, node2):
    """Stop BTFS daemon for all nodes"""
    node0.stop_daemon()
    node1.stop_daemon()
    node2.stop_daemon()

def node_exit(node0, node1, node2):
    node0.close()
    node1.close()
    node2.close()

def basic_test(node0, node1, node2):
    #init cross regions class
    regions = btfs_cross_regions.Regions(node0, node1, node2)

    #0.nodes reset
    nodes_reset(node0, node1, node2)

    #1.Install BTFS (Linux)"""
    nodes_install_btfs(node0, node1, node2)

    #2.Show version (Linux)
    node0.version_test()

    #3.Show and change config (Linux)'
    node0.config_test()

    #4.Start BTFS daemon (Linux)
    nodes_start_daemon(node0, node1, node2)

    #5.Add and get file on one node (Linux)
    node0.one_node_get_set_file_test()

    #6.Add and get file on two nodes in different regions (Linux)
    regions.two_nodes_add_get_file()

    #7.Add and cat file on one node (Linux)
    node0.one_node_add_and_cat_file()

    #8.Test Case Name: Add and cat file on two nodes in different regions (Linux)
    regions.two_nodes_add_and_cat_file()

    #9.Test Case Name: Add and cat a large file(5MB) on two nodes in different regions (Linux)
    regions.two_nodes_add_and_cat_large_file()

    #10.Test Case Name: Add and pin file on two nodes in different regions (Linux)
    regions.two_nodes_add_and_pin_file()

    #11.Test Case Name: Pin and Remove pin file on two nodes in different regions (Linux)
    regions.two_nodes_pin_and_remove_pin_file()

    #12.Test Case Name: Add and list directory and file on one node (Linux)
    node0.one_node_add_and_list_dir()

    #13.Test Case Name: Mount and unmount BTFS to local file system (Linux)
    node0.mount_and_unmount_btfs_to_local_fs()

    #14.Test Case Name: Publish and resolve IPNS names  (Linux)
    node0.publish_and_resolve_ipns_names()

    #15.Test Case Name: Show stats (Linux)
    node0.show_stats()

    #16.Test Case Name: Add file and get DAG (Linux)
    node0.add_file_and_get_dag()

    #17.Test Case Name: API - show node id (Linux)
    node0.api_show_node_id()

    #18.Test Case Name: API - add and get file on one node (Linux)
    node0.one_node_api_add_and_get_file()

    #19.Test Case Name: Swarm - cross network connection in different regions (Linux)
    regions.three_nodes_swarm_cross_network_connection()

    #20.key gen ecdsa key pair to publish
    node0.one_node_key_gen_ecdsa()

    #21.stop BTFS daemon (Linux)
    stop_daemon(node0, node1, node2)




def one_node_test():

    node = btfs_node.BtfsNode(node0_hostname, node0_username, key_filename=node0_identity_file)
    node.set_version(version)
    node.set_btfs_cmd_interval(btfs_cmd_interval)


    #Initialize node test environment"""
    node.reset()

    #1.Install BTFS (Linux)"""
    node.install_btfs_from_binary(binary)

    #2.Show version (Linux)
    node.version_test()

    #3.Show and change config (Linux)'
    node.config_test()

    #4.Start BTFS daemon (Linux)
    node.start_daemon()


    #5.Add and get file on one node (Linux)
    node.one_node_get_set_file_test()

    #7.Add and cat file on one node (Linux)
    node.one_node_add_and_cat_file()

    #12.Test Case Name: Add and list directory and file on one node (Linux)
    node.one_node_add_and_list_dir()

    #13.Test Case Name: Mount and unmount BTFS to local file system (Linux)
    node.mount_and_unmount_btfs_to_local_fs()

    #14.Test Case Name: Publish and resolve IPNS names  (Linux)
    node.publish_and_resolve_ipns_names()

    #15.Test Case Name: Show stats (Linux)
    node.show_stats()

    #16.Test Case Name: Add file and get DAG (Linux)
    node.add_file_and_get_dag()

    #17.Test Case Name: API - show node id (Linux)
    node.api_show_node_id()

    #18.Test Case Name: API - add and get file on one node (Linux)
    node.one_node_api_add_and_get_file()

    #20.key gen ecdsa key pair to publish"""
    node.one_node_key_gen_ecdsa()

    #21.stop BTFS daemon (Linux)
    node.stop_daemon()

    node.close()


def cross_regions_test():
    #nodes init
    node0, node1, node2 = nodes_init()

    #nodes reset
    nodes_reset(node0, node1, node2)

    #nodes install btfs
    nodes_install_btfs(node0, node1, node2)

    #nodes_start_daemon
    nodes_start_daemon(node0, node1, node2)

    #init cross regions class
    regions = btfs_cross_regions.Regions(node0, node1, node2)

    #6.Add and get file on two nodes in different regions (Linux)
    regions.two_nodes_add_get_file()

    #8.Test Case Name: Add and cat file on two nodes in different regions (Linux)
    regions.two_nodes_add_and_cat_file()

    #9.Test Case Name: Add and cat a large file(5MB) on two nodes in different regions (Linux)
    regions.two_nodes_add_and_cat_large_file()

    #10.Test Case Name: Add and pin file on two nodes in different regions (Linux)
    regions.two_nodes_add_and_pin_file()

    #11.Test Case Name: Pin and Remove pin file on two nodes in different regions (Linux)
    regions.two_nodes_pin_and_remove_pin_file()

    #19.Test Case Name: Swarm - cross network connection in different regions (Linux)
    regions.three_nodes_swarm_cross_network_connection()



def main():
    #node init
    node0, node1, node2 = nodes_init()

    #basic test
    basic_test(node0, node1, node2)

    #node exit,test_end
    node_exit(node0, node1, node2)
    rlog.test_end()

    rlog.print_info('\nInitialize btfs with tron private key and retest all test cases...')
    #node init
    node0, node1, node2 = nodes_init(private_key=private_key)

    #basic test
    basic_test(node0, node1, node2)

    #node exit,test end
    node_exit(node0, node1, node2)
    rlog.test_end()




if __name__ == "__main__":
    sys.exit(main())
    #sys.exit(one_node_test())
    #sys.exit(cross_regions_test())


