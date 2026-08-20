resource "azurerm_public_ip" "app" {
  name                = "vm-k8s-notes-ai-dev-ip"
  location            = azurerm_resource_group.app.location
  resource_group_name = azurerm_resource_group.app.name

  allocation_method       = "Static"
  sku                     = "Standard"
  sku_tier                = "Regional"
  ip_version              = "IPv4"
  idle_timeout_in_minutes = 4
  zones                   = ["1"]

  tags = {
    name = "k8-note-project"
  }
}