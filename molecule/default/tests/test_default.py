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

# unfortunately the tests below don't work reliably yet.
# There is something specific in the
# testinfra's sudo command that make it not use the proper environment.
# pausing on that for now as having more urgent things to pursue
#
# def test_users_can_see_gulp_that_is_already_installed(host):

    # act as a user
    # with host.sudo("nvm_tester"):
    #     # cmd = host.run("gulp -v")
    #     # assert not cmd.stderr == ''
    #     #
    #     # host.run("npm install gulp -g")
    #
    #     cmd = host.run("gulp -v")
    #     assert cmd.stderr == ''


# def test_user_can_install_npm_package_globally_and_root_can_use_it(host):
#
#     # act as a user
#     with host.sudo("nvm_tester"):
#
#         cmd = host.run("npm install stylelint -g")
#         assert cmd.stderr == ''
#
#         cmd = host.run("stylelint -v")
#         assert cmd.stderr == ''
#
#     cmd = host.run("stylelint -v")
#     assert cmd.stderr == ''
