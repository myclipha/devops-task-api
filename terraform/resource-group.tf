resource "azurerm_resource_group" "main" {
  name     = "rg-devops-task-api"
  location = "canadacentral"

  tags = {
    project     = "devops-task-api"
    environment = "dev"
  }
}
