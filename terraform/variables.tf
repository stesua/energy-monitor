variable "azure_resource_group_name" {
  description = "The unique name of azure resource group"
  type = string
}

variable "azure_location" {
  description = "The location of azure resources, see azure documentation for list of values"
  type = string
  default = "Europe West"
}

variable "azure_storage_account" {
  description = "The azure storage account unique name"
  type = string
}
