"""Unit Test suite for github action workflow"""
import policy_engine
import unittest
from unittest import mock
from azure.mgmt.resource.policy import PolicyClient

import os
from azure.identity import ClientSecretCredential

# import dotenv to gain the ability to get environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()

client_id = os.environ.get("AZURE_CLIENT_ID")
client_secret = os.environ.get("AZURE_CLIENT_SECRET")
tenant_id = os.environ.get("AZURE_TENANT_ID")
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
management_group_id = os.environ.get("MANAGEMENT_GROUP_ID")


class PolicyTestCase(unittest.TestCase):
    def setUp(self):
        credentials = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
        policy_client = PolicyClient(credentials, subscription_id)
        self.inst = policy_engine.PolicyEngine(policy_client)

    def test_assign_policy_passes(self):
        self.assertTrue("Shows all virtual machines not using managed disks" in str(self.inst.assign_policy(True)))

    def test_invalid_credentials(self):
        self.inst.assign_policy = mock.Mock(side_effect=Exception('This is broken'))

        with self.assertRaises(Exception) as context:
            self.inst.assign_policy(True)

        self.assertTrue('This is broken' in str(context.exception))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
