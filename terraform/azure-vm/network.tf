resource "azurerm_virtual_network" "app" {
  name                = "vnet-eastus-1"
  location            = azurerm_resource_group.app.location
  resource_group_name = azurerm_resource_group.app.name
  address_space       = ["172.16.0.0/16"]
}

resource "azurerm_subnet" "app" {
  name                 = "snet-eastus-1"
  resource_group_name  = azurerm_resource_group.app.name
  virtual_network_name = azurerm_virtual_network.app.name
  address_prefixes     = ["172.16.0.0/24"]

  default_outbound_access_enabled               = true
  private_endpoint_network_policies             = "Disabled"
  private_link_service_network_policies_enabled = true
}