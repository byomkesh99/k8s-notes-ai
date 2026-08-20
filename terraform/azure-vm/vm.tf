resource "azurerm_linux_virtual_machine" "app" {
  name                = "vm-k8s-notes-ai-dev"
  location            = azurerm_resource_group.app.location
  resource_group_name = azurerm_resource_group.app.name
  size                = "Standard_B2s"
  zone                = "1"

  computer_name                   = "vm-k8s-notes-ai-dev"
  admin_username                  = "azureuser"
  disable_password_authentication = true

  network_interface_ids = [
    azurerm_network_interface.app.id,
  ]

  admin_ssh_key {
    username   = "azureuser"
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCaaktyv+WQWF86PUIgBhoyULlLgvw7fnBAsske0F4vAgtGhWzHbRnFVoSuUHlLKAIHtW+k0F1ALiKilOeOKm8gA2xU4qiGHg84Gjx+k4vJYCcGzuM1L3dcBaoZnqPj7Dc2iZyUjpeSS18EFcI3vcYg8X1mKM0wvaWmKn+AUo3FGAuuhhrm+sstD9WNBMUkgWb/UO5FT1AYK1LWdnxa5mmQX0BmZh83bSjq57e51QF4AzVwSKW1HGXe0W7OtYFzVHjVSQmTF6RCAzS4Ipu5mkGj7ErO7Usj0prPqcL2QmVSv+xgHRCYx3BmmR1YWE92aVrOSUxc6gsaKXjGYPrTdXX/8IwWAue6kPQLSMHwtUogK12SaQG/fOXsO2t2hE6ad393Tbbmg7iCMSGOkgD/D5Vl7fQkGSxTRVONRd8dyEqED7RmqGXovuFuXo6u3hxebxRwNv8vGul6YUh5/h/1G3W3SEjI39nGzbqIRbUtFwe83oGApb6UfWGe7lLskCRV8h0= generated-by-azure"
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
    disk_size_gb         = 30
  }

  source_image_reference {
    publisher = "canonical"
    offer     = "ubuntu-24_04-lts"
    sku       = "server"
    version   = "latest"
  }

  boot_diagnostics {}

  additional_capabilities {
    hibernation_enabled = false
    ultra_ssd_enabled   = false
  }

  secure_boot_enabled = true
  vtpm_enabled        = true

  patch_mode            = "ImageDefault"
  patch_assessment_mode = "ImageDefault"

  tags = {
    name = "k8-note-project"
  }
}
