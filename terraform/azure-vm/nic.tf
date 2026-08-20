resource "azurerm_network_interface" "app" {
  name                = "vm-k8s-notes-ai-dev276"
  location            = azurerm_resource_group.app.location
  resource_group_name = azurerm_resource_group.app.name

  accelerated_networking_enabled = false
  ip_forwarding_enabled          = false

  ip_configuration {
    name                          = "ipconfig1"
    primary                       = true
    subnet_id                     = azurerm_subnet.app.id
    private_ip_address_allocation = "Dynamic"
    private_ip_address_version    = "IPv4"
    public_ip_address_id          = azurerm_public_ip.app.id
  }

  tags = {
    name = "k8-note-project"
  }
}

resource "azurerm_network_interface_security_group_association" "app" {
  network_interface_id      = azurerm_network_interface.app.id
  network_security_group_id = azurerm_network_security_group.app.id
}