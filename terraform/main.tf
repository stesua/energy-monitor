terraform {
  backend "azurerm" { }

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.35.0"
    }
  }
}

provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "energy_monitor" {
  name = var.azure_resource_group_name
}

data "azurerm_storage_account" "energy_monitor" {
  name                = var.azure_storage_account
  resource_group_name = data.azurerm_resource_group.energy_monitor.name
}

resource "azurerm_storage_container" "raspberry" {
  name                  = "raspberry"
  storage_account_name  = data.azurerm_storage_account.energy_monitor.name
  container_access_type = "private"
}

resource "azurerm_storage_blob" "influxdb_backups" {
  name                   = "influxdb-backups/.dir"
  storage_account_name   = data.azurerm_storage_account.energy_monitor.name
  storage_container_name = azurerm_storage_container.raspberry.name
  type                   = "Block"
  source                 = ""
}
