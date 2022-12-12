#!/bin/sh
set -e

export resource_group_name=$1
export azure_location=$2
export azure_storage_account=$3

echo "Creating group $resource_group_name"
az group create -n "$resource_group_name" -l "$azure_location"
echo "Group $resource_group_name created or already exists"

echo "Creating storage account $azure_storage_account"
az storage account create -n "$azure_storage_account" -g "$resource_group_name" -l "$azure_location" --sku Standard_LRS
echo "Storage account $azure_storage_account created or already exists"

echo "Enabling versioning for storage account $azure_storage_account"
az storage account blob-service-properties update \
    --resource-group "$resource_group_name" \
    --account-name "$azure_storage_account" \
    --enable-versioning true
echo "Versioning enabled for storage account $azure_storage_account"

echo "Creating terraform container"
az storage container create -n "terraform" --account-name "$azure_storage_account"
echo "Terraform container created or already exists"

echo "Creating backend.conf"
{
  echo "resource_group_name  = \"$resource_group_name\""
  echo "storage_account_name = \"$azure_storage_account\""
  echo "container_name       = \"terraform\""
  echo "key                  = \"terraform.tfstate\""
} > backend.conf
echo "backend.conf created"

echo "Creating terraform.tfvars"
envsubst < terraform-template.tfvars > terraform.tfvars
echo "terraform.tfvars created"

echo "Init terraform"
terraform init -backend-config=backend.conf
echo "Terraform init completed"
