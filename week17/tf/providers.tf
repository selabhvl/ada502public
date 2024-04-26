terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "3.100.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~>3.0"
    }
    time = {
      source  = "hashicorp/time"
      version = "0.9.1"
    }
    azuread = {
      source = "hashicorp/azuread"
      version = "2.48.0"
    }
    kubernetes = {
      source = "hashicorp/kubernetes"
      version = "2.29.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id   = var.azure_subscription
}

provider "kubernetes" {
  host                   = "${azurerm_kubernetes_cluster.experiment_cluster.kube_admin_config.0.host}"
  client_certificate     = "${base64decode(azurerm_kubernetes_cluster.experiment_cluster.kube_admin_config.0.client_certificate)}"
  client_key             = "${base64decode(azurerm_kubernetes_cluster.experiment_cluster.kube_admin_config.0.client_key)}"
  cluster_ca_certificate = "${base64decode(azurerm_kubernetes_cluster.experiment_cluster.kube_admin_config.0.cluster_ca_certificate)}"
}
