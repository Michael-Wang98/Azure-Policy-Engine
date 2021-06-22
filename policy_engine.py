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


def main(func=1):
    try:
        credentials = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)

        # assign policy
        if func == 1:
            policy_client = PolicyClient(credentials, subscription_id)

            # Create details for the assignment
            policyAssignmentDetails = PolicyAssignment(display_name="Audit VMs without managed disks Assignment", policy_definition_id="/providers/Microsoft.Authorization/policyDefinitions/06a78e20-9358-41c9-923c-fb736d382a4d", scope="/subscriptions/" + subscription_id, description="Shows all virtual machines not using managed disks")

            # Create new policy assignment
            policyAssignment = policy_client.policy_assignments.create("/subscriptions/" + subscription_id, "audit-vm-manageddisks", policyAssignmentDetails)

            # Show results
            print(policyAssignment)
        # delete policy assignment
        elif func == 2:

            policy_client = PolicyClient(credentials, subscription_id)

            policy_client.policy_assignments.delete("/subscriptions/" + subscription_id, "audit-vm-manageddisks")

        # create resource group
        elif func == 4:
            resource_client = ResourceManagementClient(credentials, subscription_id)
            resource_client.resource_groups.create_or_update(GROUP_NAME, {'location': LOCATION})

        # create policy definition based on template
        elif func == 5:
            policy_client = PolicyClient(credentials, subscription_id)
            with open("definitions/AuditStorageAccounts.json") as f:
                policy_client.policy_definitions.create_or_update("hello", json.load(f))

        # delete policy definition by name
        elif func == 6:
            policy_client = PolicyClient(credentials, subscription_id)
            policy_client.policy_definitions.delete("hello")
        else:
            pass

    except Exception as e:
        logging.error('Error creating policy: ', exc_info=True)
        raise e


if __name__ == "__main__":
    import argparse
    main(5)
