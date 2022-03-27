# Azure-Policy-Engine

Microsoft Azure Policy is a useful tool to enforce organizational standards and ensure compliance but managing policy purely though the Azure Portal is labour intensive and repetitive which makes a programmatic solution that manages Azure Policy useful. The Policy Engine is a software tool to interface with Azure Policy without having to use the Portal, Azure CLI or REST API calls which are all slower than a pure Python3 solution using the Azure SDK for Python. Create/Manage/Delete Azure Policies at specific scopes with a few simple commands. The Policy Engine comes with a github actions workflow which ensures the code is properly linted and passes a suite of unit and integration tests on commit.

## Installation

1. Clone the repo
```
git clone https://github.com/Michael-Wang98/Azure-Policy-Engine.git
```
2. Create a .env file in the local directory and enter the Azure credentials of the client using the policy engine according to the template shown below links to documentation for getting these values below

```
AZURE_CLIENT_ID = <YOUR_CLIENT_ID_HERE>
AZURE_CLIENT_SECRET = <YOUR_CLIENT_SECRET_HERE>
AZURE_TENANT_ID = <YOUR_TENANT_ID_HERE>
AZURE_SUBSCRIPTION_ID = <YOUR_SUBSCRIPTION_ID_HERE>
```

3. Install dependencies as specified in the requirements.txt file 

## Technologies
Project is created with:

* Python3.8

* Azure SDK

## Usage

Work in Progress

## Roadmap

- Add functionality for Azure Policy Initiatives
- Expand test suite
- Specify structure to arrange policy definition templates and initiative templates

## License
Distributed under the MIT License. See LICENSE for more information.

## Useful Links

[What is Azure Policy?](https://docs.microsoft.com/en-us/azure/governance/policy/overview)

[How to get Azure Client ID](https://docs.microsoft.com/en-us/azure/storage/common/storage-auth-aad-app?tabs=dotnet#register-your-application-with-an-azure-ad-tenant)

[How to get Azure Client Secret](https://docs.microsoft.com/en-us/azure/storage/common/storage-auth-aad-app?tabs=dotnet#create-a-client-secret)

[How to get Azure Tenant ID](https://docs.microsoft.com/en-us/azure/active-directory/fundamentals/active-directory-how-to-find-tenant)

[How to get Azure Subscription ID](https://docs.microsoft.com/en-us/azure/media-services/latest/setup-azure-subscription-how-to?tabs=portal)

