variable "group_no" {
  type = string
}

variable "group_sp_oid" {
  type = string
}

variable "aks_cluster_id" {
  type = string
}

variable "acr_id" {
  type = string
}

resource "kubernetes_namespace_v1" "group_ns" {
  metadata {
    name = var.group_no
  }
}

resource "kubernetes_role_v1" "group_role" {
  metadata {
    name = "${var.group_no}-role"
    namespace = var.group_no
  }

  rule {
    api_groups     = [""]
    resources      = ["secrets", "configmaps", "pods", "deployment.apps", "statefulset", "services", "endpoints", "persistentvolumeclaims", "replicationcontrollers"]
    verbs = ["get", "list", "watch", "create", "delete"]
  }

  rule {
    api_groups = [""]
    resources  = ["events", "resourcequotas"]
    verbs      = ["get", "list", "watch"]
  }
}

resource "kubernetes_role_binding_v1" "group_role_binding" {
  metadata {
    name = "${var.group_no}-role-binding"
    namespace = var.group_no
  }
  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "Role"
    name      = "${var.group_no}-role"
  }
  subject {
    kind      = "User"
    name      = var.group_sp_oid
    api_group = "rbac.authorization.k8s.io"
  }
}

resource "kubernetes_resource_quota_v1" "group_quota" {
   metadata {
       name = "${var.group_no}-quota"
      namespace = var.group_no
   }
   spec {
    hard = {
      "services.loadbalancers" = "1"
    }
   }
}

resource "azurerm_role_assignment" "group_sp_acr_push" {
  # the object id of the Service Principal, which I have used 
  principal_id                     = var.group_sp_oid
  role_definition_name             = "AcrPush"
  scope                            = var.acr_id
  skip_service_principal_aad_check = true
}

resource "azurerm_role_assignment" "group_sp_aks_access" {
  # the object id of the Service Principal, which I have used 
  principal_id                     = var.group_sp_oid
  role_definition_name             = "Reader"
  scope                            = var.aks_cluster_id
  skip_service_principal_aad_check = true
}

resource "azurerm_role_assignment" "group_sp_aks_get_credential" {
  # the object id of the Service Principal, which I have used 
  principal_id                     = var.group_sp_oid
  role_definition_name             = "Azure Kubernetes Service Cluster User Role"
  scope                            = var.aks_cluster_id
  skip_service_principal_aad_check = true
}


resource "azurerm_role_assignment" "group_sp_acr_access" {
  # the object id of the Service Principal, which I have used 
  principal_id                     = var.group_sp_oid
  role_definition_name             = "Reader"
  scope                            = var.acr_id
  skip_service_principal_aad_check = true
}
