variable "resource_group_name" {
  type = string
  description = "RG name"
}

variable "past_user_oid" {
  type = string
  description = "The Object UUID of my past@hvl.no user"
}

variable "resource_group_location" {
  type = string 
  description = "RG location"
  default = "norwayeast"
}

variable "cluster_name" {
  type = string 
  description = "AKS cluster name"
}

variable "registry_name" {
  type = string
  description = "ACR registry name"
}

variable "cluster_vm_size" {
  type = string 
  description = "AKS VM default size"
  default = "standard_a2_v2"
}

variable "cluster_vm_count" {
  type = number
  description = "No of AKS Vms"
  default = 1
}

variable "azure_subscription" {
  type = string
  description = "Azure Subscription"
}

variable "tenant" {
  type = string 
  description = "The tenant id of my subscription, i.e. @hvl.no"
}

variable "aks_sp_app_id" {
  type = string
}
variable "aks_sp_secret" {
  type = string 
  sensitive = true
}
variable "aks_sp_tenant" {
  type = string
}
variable "aks_sp_object_id" {
  type = string
}

variable "groups" {
  type = list(object({
    group_no = string 
    group_sp_oid = string
  }))
  description = "List of pairs associating group numbers and their service principals"
  default = []
}
