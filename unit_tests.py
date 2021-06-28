"""Unit Test suite for github action workflow"""
import policy_engine
import unittest
from unittest import mock

import os
from azure.identity import ClientSecretCredential

# import dotenv to gain the ability to get environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()


class PolicyTestCase(unittest.TestCase):
    def setUp(self):
        client_id = os.environ.get("AZURE_CLIENT_ID")
        client_secret = os.environ.get("AZURE_CLIENT_SECRET")
        tenant_id = os.environ.get("AZURE_TENANT_ID")

        credentials = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)

        self.inst = policy_engine.PolicyEngine(credentials)

    def test_assign_policy_passes(self):
        self.assertTrue("Shows all virtual machines not using managed disks" in str(self.inst.assign_policy()))

    def test_invalid_credentials(self):
        self.inst.assign_policy = mock.Mock(side_effect=Exception('This is broken'))

        with self.assertRaises(Exception) as context:
            self.inst.assign_policy()

        self.assertTrue('This is broken' in str(context.exception))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
