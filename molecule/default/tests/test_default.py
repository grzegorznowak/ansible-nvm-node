import os


import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_node_version_ok(host):
    cmd = host.run("node -v")
    assert cmd.stderr == ''
    assert cmd.stdout == 'v8.11.3'


def test_global_gulp_version_ok(host):
    cmd = host.run("gulp -v")
    assert cmd.stderr == ''
    assert 'CLI version 2.0.1' in cmd.stdout

    cmd = host.run("sudo -u www-data which gulp")
    assert cmd.stderr == ''
    assert cmd.stdout == '/usr/bin/gulp'


def test_npm_ok(host):
    cmd = host.run("npm -v")
    assert cmd.stdout == '5.6.0'


def test_user_npm_ok(host):
    with host.sudo("nvm_tester"):
        host.check_output("whoami")
        cmd = host.run("npm -v")
        assert cmd.stdout == '5.6.0'


def test_user_node_version_ok(host):
    with host.sudo("nvm_tester"):
        cmd = host.run("node -v")
        assert cmd.stderr == ''
        assert cmd.stdout == 'v8.11.3'
