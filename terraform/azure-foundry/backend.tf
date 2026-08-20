terraform {
  backend "azurerm" {
    resource_group_name  = "tfstate-day04-bd"
    storage_account_name = "day04tfstate9913"
    container_name       = "k8s-notes-tfstate"
    key                  = "azure-foundry.terraform.tfstate"

    use_cli          = true
    use_azuread_auth = true
    tenant_id        = "50b3b208-9642-4394-bf3f-58b5dfd07635"
  }
}
