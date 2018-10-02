import os


import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_node_version_ok(host):
    cmd = host.run("node -v")
    assert cmd.stderr == ''
    assert cmd.stdout == 'v8.11.3'

def test_npm_ok(host):
    cmd = host.run("npm -v")
    assert cmd.stderr == ''
