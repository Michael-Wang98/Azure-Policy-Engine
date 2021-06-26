import os
import sys
import logging
import json

from azure.mgmt.resource.policy import PolicyClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.policy.models import PolicyAssignment
from azure.identity import ClientSecretCredential

# import dotenv to gain the ability to get environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()




logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s')

LOCATION = 'eastus'
GROUP_NAME = 'sample'

# get the environment variables
client_id = os.environ.get("AZURE_CLIENT_ID")
client_secret = os.environ.get("AZURE_CLIENT_SECRET")
tenant_id = os.environ.get("AZURE_TENANT_ID")
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")


class PolicyEngine:
    def __init__(self, credentials):
        self.credentials = credentials

    def assign_policy(self):
        policy_client = PolicyClient(self.credentials, subscription_id)

        # Create details for the assignment
        policy_assignment_details = PolicyAssignment(display_name="Audit VMs without managed disks Assignment",
                                                   policy_definition_id="/providers/Microsoft.Authorization/policyDefinitions/06a78e20-9358-41c9-923c-fb736d382a4d",
                                                   scope="/subscriptions/" + subscription_id,
                                                   description="Shows all virtual machines not using managed disks")

        # Create new policy assignment
        response = policy_client.policy_assignments.create("/subscriptions/" + subscription_id,
                                                                   "audit-vm-manageddisks", policy_assignment_details)

        return response

    def delete_assignment(self):
        policy_client = PolicyClient(self.credentials, subscription_id)

        response = policy_client.policy_assignments.delete("/subscriptions/" + subscription_id, "audit-vm-manageddisks")
        return response

    def create_resource_group(self):
        resource_client = ResourceManagementClient(self.credentials, subscription_id)
        response = resource_client.resource_groups.create_or_update(GROUP_NAME, {'location': LOCATION})
        return response

    def create_policy_definition(self):
        policy_client = PolicyClient(self.credentials, subscription_id)
        with open("definitions/AuditStorageAccounts.json") as f:
            response = policy_client.policy_definitions.create_or_update("hello", json.load(f))
        return response

    def delete_policy_definition(self):
        policy_client = PolicyClient(self.credentials, subscription_id)
        response = policy_client.policy_definitions.delete("hello")
        return response


def main(func=1):
    try:
        credentials = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)

        engine = PolicyEngine(credentials)
        # assign policy
        if func == 1:
            print(engine.assign_policy())
        # delete policy assignment
        elif func == 2:
            print(engine.delete_assignment())
        # create resource group
        elif func == 3:
            print(engine.create_resource_group())
        # create policy definition based on template
        elif func == 4:
            print(engine.create_policy_definition())
        # delete policy definition by name
        elif func == 5:
            print(engine.delete_policy_definition())
        else:
            pass

    except Exception as e:
        logging.error('Error creating policy: ', exc_info=True)
        raise e


if __name__ == "__main__":
    main()
