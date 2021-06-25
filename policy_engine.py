import os
import sys
import logging
import json

# import dotenv to gain the ability to get environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()

from azure.mgmt.resource.policy import PolicyClient
from azure.mgmt.resource import ResourceManagementClient

from azure.mgmt.resource.policy.models import PolicyAssignment

from azure.identity import ClientSecretCredential


logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s')

LOCATION = 'eastus'
GROUP_NAME = 'sample'

client_id = os.environ.get("AZURE_CLIENT_ID")
client_secret = os.environ.get("AZURE_CLIENT_SECRET")
tenant_id = os.environ.get("AZURE_TENANT_ID")
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")


class PolicyEngine:
    def __init__(self):
        self.credentials = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)

    def assign_policy(self):
        policy_client = PolicyClient(self.credentials, subscription_id)

        # Create details for the assignment
        policyAssignmentDetails = PolicyAssignment(display_name="Audit VMs without managed disks Assignment",
                                                   policy_definition_id="/providers/Microsoft.Authorization/policyDefinitions/06a78e20-9358-41c9-923c-fb736d382a4d",
                                                   scope="/subscriptions/" + subscription_id,
                                                   description="Shows all virtual machines not using managed disks")

        # Create new policy assignment
        policyAssignment = policy_client.policy_assignments.create("/subscriptions/" + subscription_id,
                                                                   "audit-vm-manageddisks", policyAssignmentDetails)

        # Show results
        print(policyAssignment)

    def delete_assignment(self):
        policy_client = PolicyClient(self.credentials, subscription_id)

        policy_client.policy_assignments.delete("/subscriptions/" + subscription_id, "audit-vm-manageddisks")

    def create_resource_group(self):
        resource_client = ResourceManagementClient(self.credentials, subscription_id)
        resource_client.resource_groups.create_or_update(GROUP_NAME, {'location': LOCATION})

    def create_policy_definition(self):
        policy_client = PolicyClient(self.credentials, subscription_id)
        with open("definitions/AuditStorageAccounts.json") as f:
            policy_client.policy_definitions.create_or_update("hello", json.load(f))

    def delete_policy_definition(self):
        policy_client = PolicyClient(self.credentials, subscription_id)
        policy_client.policy_definitions.delete("hello")


def main(func=5):
    try:
        engine = PolicyEngine()
        # assign policy
        if func == 1:
            engine.assign_policy()
        # delete policy assignment
        elif func == 2:
            engine.delete_assignment()
        # create resource group
        elif func == 3:
            engine.create_resource_group()
        # create policy definition based on template
        elif func == 4:
            engine.create_policy_definition()
        # delete policy definition by name
        elif func == 5:
            engine.delete_policy_definition()
        else:
            pass

    except Exception as e:
        logging.error('Error creating policy: ', exc_info=True)
        raise e


if __name__ == "__main__":
    # import argparse
    #
    # parser = argparse.ArgumentParser(description="Specify Policy Engine Function")
    # # parser.add_argument("--function", required=True, help="which function to use")
    # args = parser.parse_args()

    main()
