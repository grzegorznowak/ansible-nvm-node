import os
import time


import testinfra.utils.ansible_runner

# let the which-checking crontab run
# anyone know better way of checking what cron thinks ? Please, do let me know!
time.sleep(61)

# man handle the damn 20.04's sudo bug...
FOCAL_BUG_STR = 'sudo: setrlimit(RLIMIT_CORE): Operation not permitted\n'

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_node_version_ok(host):
    cmd = host.run("node -v")
    assert cmd.stderr == ''
    assert cmd.stdout.rstrip() == 'v10.16.3'


def test_global_libraries(host):
    cmd = host.run("gulp -v")
    assert cmd.stderr == ''
    assert 'CLI version' in cmd.stdout

    cmd = host.run("lighthouse --version")
    assert cmd.stderr == ''
    assert cmd.stdout != ''

    cmd = host.run("yarn --version")
    assert cmd.stderr == ''
    assert cmd.stdout.rstrip() == '1.9.4'

    # first run does (and outputs) some extra stuff, so let's be over it now
    nop_cmd = host.run("pm2 --version")

    # let's assert something anyway to please the Flake
    assert nop_cmd.stderr == ''

    cmd = host.run("pm2 --version")
    assert cmd.stderr == ''
    assert cmd.stdout.rstrip() == '3.1.2'

    with host.sudo("nvm_tester"):
        cmd = host.run("which lighthouse")
        assert cmd.stderr == '' or cmd.stderr == FOCAL_BUG_STR
        assert cmd.stdout.rstrip() == '/usr/bin/lighthouse'

        cmd = host.run("which gulp")
        assert cmd.stderr == '' or cmd.stderr == FOCAL_BUG_STR
        assert cmd.stdout.rstrip() == '/usr/bin/gulp'

        cmd = host.run("which yarn")
        assert cmd.stderr == '' or cmd.stderr == FOCAL_BUG_STR
        assert cmd.stdout.rstrip() == '/usr/bin/yarn'

        cmd = host.run("which pm2")
        assert cmd.stderr == '' or cmd.stderr == FOCAL_BUG_STR
        assert cmd.stdout.rstrip() == '/usr/bin/pm2'


def test_cron_environment_for_global_libs(host):

    # make sure cron sees global libraries in correct locations
    assert host.run("cat /tmp/which_gulp").stdout.rstrip() == \
           '/usr/bin/gulp'
    assert host.run("cat /tmp/which_lighthouse").stdout.rstrip() == \
           '/usr/bin/lighthouse'
    assert host.run("cat /tmp/which_lighthouse").stdout.rstrip() == \
           '/usr/bin/lighthouse'


def test_user_node_version_ok(host):
    with host.sudo("nvm_tester"):
        cmd = host.run("node -v")
        assert cmd.stderr == '' or cmd.stderr == FOCAL_BUG_STR
        assert cmd.stdout.rstrip() == 'v10.16.3'


def test_npm_ok(host):
    cmd = host.run("npm -v")
    assert cmd.stdout.rstrip() == '6.9.0'


def test_user_npm_ok(host):
    with host.sudo("nvm_tester"):
        host.check_output("whoami")
        cmd = host.run("npm -v")
        assert cmd.stdout.rstrip() == '6.9.0'
