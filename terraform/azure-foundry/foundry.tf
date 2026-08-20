resource "azurerm_cognitive_account" "foundry" {
  name                = "foundryplay082026"
  resource_group_name = "foundry_play_RG"
  location            = "eastus"
  kind                = "AIServices"
  sku_name            = "S0"

  custom_subdomain_name         = "foundryplay082026"
  public_network_access_enabled = true
  local_auth_enabled            = true

  project_management_enabled = true

  identity {
    type = "SystemAssigned"
  }

  network_acls {
    default_action = "Allow"
  }

  tags = {
    name = "Foundry_play"
  }
}

resource "azurerm_cognitive_deployment" "chat" {
  name                 = "k8s-chat"
  cognitive_account_id = azurerm_cognitive_account.foundry.id

  model {
    format  = "OpenAI"
    name    = "gpt-4.1-mini"
    version = "2025-04-14"
  }

  sku {
    name     = "GlobalStandard"
    capacity = 250
  }
}

resource "azurerm_cognitive_deployment" "embeddings" {
  name                 = "k8s-embeddings"
  cognitive_account_id = azurerm_cognitive_account.foundry.id

  model {
    format  = "OpenAI"
    name    = "text-embedding-3-small"
    version = "1"
  }

  sku {
    name     = "GlobalStandard"
    capacity = 150
  }
}
