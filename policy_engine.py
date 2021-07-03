"""Policy Engine"""
import os
import sys
import logging
import json
from azure.mgmt.resource.policy import PolicyClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.policy.models import PolicyAssignment
from azure.identity import ClientSecretCredential
from dotenv import load_dotenv  # import dotenv to get environment variables from .env file
load_dotenv()

# get environment variables
client_id = os.environ.get("AZURE_CLIENT_ID")
client_secret = os.environ.get("AZURE_CLIENT_SECRET")
tenant_id = os.environ.get("AZURE_TENANT_ID")
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
management_group_id = os.environ.get("MANAGEMENT_GROUP_ID")


logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s')


# policy engine class which currently contains example uses for the policy client functions pertaining to policy
class PolicyEngine:
    def __init__(self, credentials):
        self.credentials = credentials

    # assigns a policy
    def assign_policy(self):
        policy_client = PolicyClient(self.credentials, subscription_id)

        # Create details for the assignment
        # isn't needed probably
        # policy_assignment_details = PolicyAssignment(policy_definition_id="/providers/Microsoft.Authorization/policyDefinitions/06a78e20-9358-41c9-923c-fb736d382a4d")

        # Create new policy assignment
        response = policy_client.policy_assignments.create("/subscriptions/" + subscription_id,
                                                                   "audit-vm-manageddisks", {'policy_definition_id': "/providers/Microsoft.Authorization/policyDefinitions/06a78e20-9358-41c9-923c-fb736d382a4d",
                                                                                             'description': "Shows all virtual machines not using managed disks"})
        return response

    # deletes a policy assignment
    def delete_assignment(self):
        policy_client = PolicyClient(self.credentials, subscription_id)

        response = policy_client.policy_assignments.delete("/subscriptions/" + subscription_id, "audit-vm-manageddisks")
        return response

    # create or update a policy definition from a template
    def create_policy_definition(self, policy_name):
        policy_client = PolicyClient(self.credentials, subscription_id)

        with open("definitions/" + policy_name) as f:
            response = policy_client.policy_definitions.create_or_update(policy_name.split(".")[0], json.load(f))

        # definitions = os.listdir("definitions")
        # for definition in definitions:
        #     with open("definitions/" + definition) as f:
        #         response = policy_client.policy_definitions.create_or_update("hello", json.load(f))
        return response

    # delete a policy definition
    def delete_policy_definition(self, policy_name):
        policy_client = PolicyClient(self.credentials, subscription_id)
        response = policy_client.policy_definitions.delete(policy_name)
        return response

    # work in progress, create definition at management group
    def create_manage(self, policy_name):
        policy_client = PolicyClient(self.credentials, subscription_id)
        with open("definitions/" + policy_name) as f:
            response = policy_client.policy_definitions.create_or_update_at_management_group(policy_name.split(".")[0], management_group_id, json.load(f))

        return response

    def delete_manage(self, policy_name):
        policy_client = PolicyClient(self.credentials, subscription_id)
        with open("definitions/" + policy_name) as f:
            response = policy_client.policy_definitions.delete_at_management_group(policy_name.split(".")[0],
                                                                                             management_group_id)

        return response

    # assigns a policy
    def assign_management(self):
        policy_client = PolicyClient(self.credentials, subscription_id)

        # Create details for the assignment
        # isn't needed probably
        # policy_assignment_details = PolicyAssignment(policy_definition_id="/providers/Microsoft.Authorization/policyDefinitions/06a78e20-9358-41c9-923c-fb736d382a4d")

        # Create new policy assignment
        response = policy_client.policy_assignments.create("/providers/Microsoft.Management/managementgroups/" + management_group_id,
                                                           "audit-vm-manageddisks", {
                                                               'policy_definition_id': "/providers/Microsoft.Authorization/policyDefinitions/06a78e20-9358-41c9-923c-fb736d382a4d"})
        return response

    # deletes a policy assignment
    def delete_management(self):
        policy_client = PolicyClient(self.credentials, subscription_id)

        response = policy_client.policy_assignments.delete("/providers/Microsoft.Management/managementgroups/" + management_group_id, "audit-vm-manageddisks")
        return response


def main(func=9):
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
            definitions = os.listdir("definitions")
            for definition in definitions:
                print(engine.create_policy_definition(definition))
        # delete policy definition by name
        elif func == 5:
            print(engine.delete_policy_definition("hello"))
        elif func == 6:
            engine.create_manage("AuditStorageAccounts.json")
        elif func == 7:
            engine.delete_manage("AuditStorageAccounts.json")
        elif func == 8:
            engine.assign_management()
        elif func == 9:
            engine.delete_management()
        else:
            pass

    except Exception as e:
        logging.error('Error creating policy: ', exc_info=True)
        raise e


if __name__ == "__main__":
    main()
