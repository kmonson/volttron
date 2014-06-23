import unittest
import os
import shutil
import sys

from collections import namedtuple
from wheel.install import WheelFile

from volttron.platform.packaging import create_package
from volttron.platform.packaging import AgentPackageError

# Temporary path for working during running of package/unpackage tests.
TMP_AGENT_DIR = '/tmp/agent-dir'

class TestPackaging(unittest.TestCase):

    
    def setUp(self):
        '''
        Recreates the temporary agent directory before each run
        '''
        if os.path.exists(TMP_AGENT_DIR):
            shutil.rmtree(TMP_AGENT_DIR)
        os.makedirs(TMP_AGENT_DIR)
        
        self.fixtureDir = os.path.join(os.path.dirname(__file__), "fixtures")

    def test_can_create_an_initial_package(self):
        '''
        Tests that a proper wheel package is created from the create_package method of
        the AgentPackage class.
        '''
        agent_name = "test-agent-package"
        agent_to_package = os.path.join(self.fixtureDir, agent_name)
        
        package_name = create_package(agent_to_package)
        
        self.assertIsNotNone(package_name, "Invalid package name {}".format(package_name))
        # Wheel is in the correct location.
        print(package_name)
        self.assertTrue(os.path.exists(package_name))
        #self.assertTrue(os.path.exists(os.path.join(TMP_AGENT_DIR, package_name)))
        self.assertTrue(agent_name in package_name)
        
        # TODO Verify zip structure.
        whl = WheelFile(package_name)
        
        #print(whl.check_version())
        print("datadir_name:",whl.datadir_name)
        print('distinfo_name',whl.distinfo_name)
        print('context', whl.context())
        print('arity', whl.arity)
        print('compatibility_tags', whl.compatibility_tags)
        print('compatible',whl.compatible)
        
        
        
    
    
    def test_raises_error_if_agent_dir_not_exists(self):
        '''
        This test passes under the following conditions:
            1. An AgentPackageError is thrown if the passed agent directory 
               doesen't exists.
        '''
        # 
        fake_agent = '/tmp/Fake'
        if os.path.exists(fake_agent):
            shutil.rmtree(fake_agent, True)
            
        self.assertRaises(AgentPackageError, lambda: create_package(fake_agent))
        

