import os
import pytest
import subprocess
import testinfra

@pytest.fixture(scope='session')
def host(request):
    subprocess.check_call(['docker', 'build', '-t', 'image-under-test', '.'])
    docker_id = subprocess.check_output(['docker', 'run', '--rm', '-d', '--entrypoint=/usr/bin/tail', '-t', 'image-under-test']).decode().strip()
    
    yield testinfra.get_host("docker://" + docker_id)
    
    # teardown
    subprocess.check_call(['docker', 'rm', '-f', docker_id])

def test_system(host):
    assert host.system_info.distribution == 'alpine'
    assert host.system_info.release.startswith('3.8.')

def test_user(host):
    assert host.user('etesync').exists
    assert host.user('etesync').shell == '/bin/false'

def test_app_folder(host):
    folder = '/app'
    assert host.file(folder).exists
    assert host.file(folder).user == 'etesync'
    assert host.file(folder).group == 'root'
    assert oct(host.file(folder).mode) == '0o500'

@pytest.mark.parametrize('package', [
    ('python3'),
    ('py-tz'),
])
def test_installed_dependencies(host, package):
    assert host.package(package).is_installed