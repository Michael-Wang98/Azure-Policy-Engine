import os
import sys
import logging
import policy_engine
from azure.mgmt.resource.policy import PolicyClient
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


def main(func=4):
    try:
        credentials = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
        policy_client = PolicyClient(credentials, subscription_id)
        # assign policy
        if func == 1:
            engine = policy_engine.AssignmentEngine(policy_client, subscription_id, management_group_id)
            assignments = os.listdir("assignments")
            for assignment in assignments:
                print(engine.assign_policy(assignment, False))
        # delete policy assignment
        elif func == 2:
            engine = policy_engine.AssignmentEngine(policy_client, subscription_id, management_group_id)
            print(engine.delete_assignment("audit-vm-manageddisks", True))
        # create policy definition based on template
        elif func == 3:
            engine = policy_engine.DefinitionEngine(policy_client, subscription_id, management_group_id)
            definitions = os.listdir("definitions")
            for definition in definitions:
                print(engine.create_policy_definition(definition, False))
        # delete policy definition by name
        elif func == 4:
            engine = policy_engine.DefinitionEngine(policy_client, subscription_id, management_group_id)
            print(engine.delete_policy_definition("hello", True))
        # create policy initiative
        elif func == 5:
            engine = policy_engine.InitiativeEngine(policy_client, subscription_id, management_group_id)
            initiatives = os.listdir("initiatives")
            for initiative in initiatives:
                print(engine.create_initiative(initiative, False))
        # delete policy initiative by name
        elif func == 6:
            engine = policy_engine.InitiativeEngine(policy_client, subscription_id, management_group_id)
            engine.delete_initiative("test_initiative", False)
        else:
            pass

    except Exception as e:
        logging.error('Error creating policy: ', exc_info=True)
        raise e


if __name__ == "__main__":
    main()
