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
    def __init__(self, policy_client):
        self.policy_client = policy_client


class AssignmentEngine(PolicyEngine):
    def __init__(self, policy_client):
        super().__init__(policy_client)

    # assigns a policy
    def assign_policy(self, is_sub):
        # Create details for the assignment
        # isn't needed probably
        # policy_assignment_details = PolicyAssignment(policy_definition_id="/providers/Microsoft.Authorization/policyDefinitions/06a78e20-9358-41c9-923c-fb736d382a4d")

        if is_sub:
            # Create new policy assignment
            response = self.policy_client.policy_assignments.create("/subscriptions/" + subscription_id,
                                                                       "audit-vm-manageddisks", {'policy_definition_id': "/providers/Microsoft.Authorization/policyDefinitions/06a78e20-9358-41c9-923c-fb736d382a4d",
                                                                                                 'description': "Shows all virtual machines not using managed disks"})
        else:
            response = self.policy_client.policy_assignments.create(
                "/providers/Microsoft.Management/managementgroups/" + management_group_id,
                "audit-vm-manageddisks", {
                    'policy_definition_id': "/providers/Microsoft.Authorization/policyDefinitions/06a78e20-9358-41c9-923c-fb736d382a4d"})

        return response

    # deletes a policy assignment
    def delete_assignment(self, assignment_name, is_sub):
        if is_sub:
            response = self.policy_client.policy_assignments.delete("/subscriptions/" + subscription_id, assignment_name)
        else:
            response = self.policy_client.policy_assignments.delete(
                "/providers/Microsoft.Management/managementgroups/" + management_group_id, assignment_name)
        return response


class DefinitionEngine(PolicyEngine):
    def __init__(self, policy_client):
        super().__init__(policy_client)

    # create or update a policy definition from a template
    def create_policy_definition(self, policy_name, is_sub):
        if is_sub:
            with open("definitions/" + policy_name) as f:
                response = self.policy_client.policy_definitions.create_or_update(policy_name.split(".")[0], json.load(f))
        else:
            with open("definitions/" + policy_name) as f:
                response = self.policy_client.policy_definitions.create_or_update_at_management_group(policy_name.split(".")[0], management_group_id, json.load(f))
        return response

    # delete a policy definition
    def delete_policy_definition(self, policy_name, is_sub):
        if is_sub:
            response = self.policy_client.policy_definitions.delete(policy_name)
        else:
            response = self.policy_client.policy_definitions.delete_at_management_group(policy_name, management_group_id)
        return response


class InitiativeEngine(PolicyEngine):
    def __init__(self, policy_client):
        super().__init__(policy_client)

    def create_initiative(self, initiative_name, is_sub):
        if is_sub:
            with open("initiatives/" + initiative_name) as f:
                response = self.policy_client.policy_set_definitions.create_or_update(initiative_name.split(".")[0], json.load(f))
        else:
            with open("initiatives/" + initiative_name) as f:
                response = self.policy_client.policy_set_definitions.create_or_update_at_management_group(initiative_name.split(".")[0], management_group_id, json.load(f))

        return response

    def delete_initiative(self, is_sub):
        if is_sub:
            self.policy_client.policy_set_definitions.delete("test_initiative")
        else:
            self.policy_client.policy_set_definitions.delete_at_management_group("test_initiative", management_group_id)


def main(func=6):
    try:
        credentials = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
        policy_client = PolicyClient(credentials, subscription_id)
        # assign policy
        if func == 1:
            engine = AssignmentEngine(policy_client)
            print(engine.assign_policy(False))
        # delete policy assignment
        elif func == 2:
            engine = AssignmentEngine(policy_client)
            print(engine.delete_assignment("audit-vm-manageddisks", True))
        # create policy definition based on template
        elif func == 3:
            engine = DefinitionEngine(policy_client)
            definitions = os.listdir("definitions")
            for definition in definitions:
                print(engine.create_policy_definition(definition, False))
        # delete policy definition by name
        elif func == 4:
            engine = DefinitionEngine(policy_client)
            print(engine.delete_policy_definition("hello", True))
        elif func == 5:
            engine = InitiativeEngine(policy_client)
            initiatives = os.listdir("initiatives")
            for initiative in initiatives:
                print(engine.create_initiative(initiative, False))
            # engine.create_initiative(True)
        elif func == 6:
            engine = InitiativeEngine(policy_client)
            engine.delete_initiative(False)
        else:
            pass

    except Exception as e:
        logging.error('Error creating policy: ', exc_info=True)
        raise e


if __name__ == "__main__":
    main()
