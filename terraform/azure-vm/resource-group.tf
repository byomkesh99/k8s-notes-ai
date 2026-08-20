resource "azurerm_resource_group" "app" {
  name     = "foundry_play_RG"
  location = "eastus"

  tags = {
    name = "Foundry_play"
  }
}
