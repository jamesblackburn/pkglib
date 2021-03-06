from pkg_resources import resource_filename, get_distribution  # @UnresolvedImport
from pkglib.testing.util import PkgTemplate
from distutils.dir_util import copy_tree
import pytest


def test_profile_profiles_tests(pytestconfig):
    test_dir = resource_filename('pkglib.testing', '../../tests/integration/pytest/profile')
    with PkgTemplate(name='acme.foo') as pkg:
        pkg.install_package('pytest-cov')
        copy_tree(test_dir, pkg.trunk_dir)
        output = pkg.run_with_coverage(['-m', 'pytest', '--profile', 'tests/unit/test_example.py'],
                                       pytestconfig, cd=pkg.trunk_dir)
    assert 'test_example.py:1(test_foo)' in output


def _has_distribution(dist):
    try:
        return get_distribution(dist) is not None
    except:
        return False


@pytest.mark.skipif("not _has_distribution('gprof2dot')")
def test_profile_generates_svg(pytestconfig):
    test_dir = resource_filename('pkglib.testing', '../../tests/integration/pytest/profile')
    with PkgTemplate(name='acme.foo') as pkg:
        pkg.install_package('pytest-cov')
        pkg.install_package('pkglib.testing')
        copy_tree(test_dir, pkg.trunk_dir)
        output = pkg.run_with_coverage(['-m', 'pytest', '--profile-svg', 'tests/unit/test_example.py'],
                                       pytestconfig, cd=pkg.trunk_dir)
    assert 'test_example.py:1(test_foo)' in output
    assert 'SVG' in output
    assert any('test_example:1:test_foo' in line for line in open(pkg.trunk_dir / 'prof/combined.svg'))
