# -*- coding: utf-8 -*-

"""
    sartoris.testsuite
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013 by Wikimedia Foundation.
    :license: BSD, see LICENSE for more details.
"""

import unittest
from collections import namedtuple
from sartoris.config import log
from sartoris.sartoris import Sartoris, SartorisError, exit_codes
from dulwich.repo import Repo
from os import mkdir, chdir
from os.path import exists
from shutil import rmtree

from sartoris.config import configure


# Create the initial singleton
config = configure()
Sartoris(path=config['deploy.test_repo'],
         client_path=config['deploy.test_repo'])


def setup_deco(test_method):
    """
    Performs setup and teardown calls for all tests to decouple the state if
    the repo from this testing module.
    """
    def setup_wrap(self):
        init_tmp_repo()
        try:
            test_method(self)
        finally:
            teardown_tmp_repo()
    setup_wrap.__name__ = test_method.__name__
    return setup_wrap


def init_tmp_repo():
    """
    Create a test repo, change to directory
    """

    log.info(__name__ + ':: Creating test repo.')

    if exists(config['deploy.test_repo']):
        rmtree(config['deploy.test_repo'])

    mkdir(config['deploy.test_repo'])
    Repo.init(config['deploy.test_repo'])
    chdir(config['deploy.test_repo'])


def teardown_tmp_repo():
    """
    Remove the test repo
    """

    log.info(__name__ + ':: Tearing down test repo.')

    chdir(config['deploy.test_repo'])
    rmtree(config['deploy.test_repo'])


class TestSartorisInit(unittest.TestCase):
    """ Test cases for Sartoris initialization and config """
    def test_conf_hook_dir(self):
        s = Sartoris()
        assert 'top_dir' in s.config

    def test_conf_top_dir(self):
        s = Sartoris()
        assert 'hook_dir' in s.config

    def test_conf_repo_name(self):
        s = Sartoris()
        assert 'repo_name' in s.config

    def test_conf_deploy_file(self):
        s = Sartoris()
        assert 'deploy_file' in s.config

    def test_singleton(self):
        s1 = Sartoris()
        s2 = Sartoris()
        assert s1 == s2


class TestSartorisFunctionality(unittest.TestCase):

    @setup_deco
    def test_abort(self):
        """
        abort - test to ensure that ``abort`` method functions
        without exception
        """
        sartoris_obj = Sartoris()

        try:
            sartoris_obj.start(None)
            sartoris_obj.abort(None)

            # TODO - check lock file & commit

        except SartorisError:
            assert False

    @setup_deco
    def test_diff(self):
        """
        diff - test to ensure that ``diff`` method functions
        without exception
        """
        sartoris_obj = Sartoris()
        try:
            sartoris_obj.diff(None)
        except SartorisError:
            assert False

    @setup_deco
    def test_log_deploys(self):
        """
        log_deploys - test to ensure that ``log_deploys`` method functions
        without exception
        """
        sartoris_obj = Sartoris()
        try:
            sartoris_obj.log_deploys(namedtuple('o', 'count')(1))
        except SartorisError:
            assert False

    @setup_deco
    def test_revert(self):
        """
        revert - test to ensure that ``revert`` method functions
        without exception
        """
        sartoris_obj = Sartoris()
        try:
            sartoris_obj.revert(namedtuple('o', 'force')(False))
        except SartorisError:
            assert False

    @setup_deco
    def test_show_tag(self):
        """
        start - test to ensure that start method functions
        without exception
        """
        sartoris_obj = Sartoris()
        try:
            sartoris_obj.start(None)
            sartoris_obj.sync(None)
            sartoris_obj.show_tag(None)

        except SartorisError:
            assert False

    @setup_deco
    def test_start(self):
        """
        start - test to ensure that ``start`` method functions
        without exception
        """
        sartoris_obj = Sartoris()
        try:
            sartoris_obj.start(None)
        except SartorisError:
            assert False

    @setup_deco
    def test_sync(self):
        """
        sync - test to ensure that ``sync`` method functions
        without exception
        """
        sartoris_obj = Sartoris()
        try:
            sartoris_obj.start(None)
            sartoris_obj.sync(None)

            # TODO - check tag and deploy file
        except SartorisError:
            assert False

    @setup_deco
    def test_deploy_in_progress(self):
        """
        deploy_in_progress - test to ensure that when the ``start`` method
        is called when a deployment is in progress Sartoris exits with error
        """
        sartoris_obj = Sartoris()

        # TODO - ensure that the repo is "fresh"

        # Call ``start`` twice
        try:
            sartoris_obj.start(None)
            sartoris_obj.start(None)
        except SartorisError as e:
            if not e.msg == exit_codes[2]:
                assert False
            return
        assert False


class TestSartorisDulwichDeps(unittest.TestCase):
    """
    Class to test Sartoris dulwich dependencies.  Utilize test repos
    """

    @setup_deco
    def test_dulwich_tag(self):
        """
        Tests method Sartoris::_dulwich_tag

            1. Call _dulwich_tag
            2. Check most recent tag to verify tag exists
        """
        s = Sartoris()
        tag = 'test_tag'
        s._dulwich_tag(tag, s._make_author())
        tags = s._dulwich_get_tags()
        assert tags.keys()[0] == tag

    @setup_deco
    def test_dulwich_reset_to_tag(self):
        """
        Tests method Sartoris::_dulwich_reset_to_tag
        """

        #   1. Create two dummy tags and commits
        #   2. Call _dulwich_reset_to_tag
        #   3. Ensure _repo['HEAD'] matches _repo['refs/tags/' + tag]

        assert False

    @setup_deco
    def test_dulwich_stage(self):
        """
        Tests method Sartoris::_dulwich_stage
        """

        #   1. Create a dummy file - use object store
        #   2. Call _dulwich_stage
        #   3. Use dulwich.diff_tree.tree_changes to ensure changes are staged

        assert False

    @setup_deco
    def test_dulwich_commit(self):
        """
        Tests method Sartoris::_dulwich_commit
        """

        #   1. Follow steps in test_dulwich_stage
        #   2. Perform commit
        #   3. Ensure that _repo['HEAD'] matches the commit.id

        assert False
