terraform {
required_providers {
azurerm = {
source = "hashicorp/azurerm"
version = ">= 2.49"
}
}
 backend "azurerm" {
        resource_group_name  = "tfstate"
        storage_account_name = "terraformstatejbf"
        container_name       = "terraformstate"
        key                  = "terraform.tfstate"
    }
}
provider "azurerm" {
features {}
}
data "azurerm_resource_group" "main" {
name = "Capita2_JorgeFerrer_ProjectExercise"
}

resource "azurerm_app_service_plan" "main" {
name = "terraformed-asp"
location = var.location
resource_group_name = data.azurerm_resource_group.main.name
kind = "Linux"
reserved = true
sku {
    tier = "Basic"
    size = "B1"
    }
}
resource "azurerm_app_service" "main" {
name = "${var.APP-PREFIX}-devops-course-jbf"
location = var.location
resource_group_name = data.azurerm_resource_group.main.name
app_service_plan_id = azurerm_app_service_plan.main.id
site_config {
    app_command_line = ""
    linux_fx_version = "DOCKER|sgipower/todo-app:latest"
    }
app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "MONGO_CONNECTION_STRING" = "mongodb://${azurerm_cosmosdb_account.main.name}:${azurerm_cosmosdb_account.main.primary_key}@${azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255/DefaultDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000"
    "DOCKER_ENABLE_CI" = "true"
    "GITHUB_CLIENTID" = var.CLIENTID
    "GITHUB_CLIENTSECRET" = var.CLIENTSECRET
    "OAUTHLIB_INSECURE_TRANSPORT"= "true"
    "PORT" = "8080"
    "SECRET_KEY" = "secret-key"
    "TRELLO_BOARD" = "60eacfe12a6b3c534957c408"
    "LOG_LEVEL" = var.loglevel
    }
}

resource "azurerm_cosmosdb_account" "main" {
  name                = "${var.APP-PREFIX}-db-course-jbf"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  capabilities {
    name = "EnableServerless"
  }

 consistency_policy {
    consistency_level = "Session"
  }

   geo_location {
    location          = var.location
    failover_priority = 0
  }
    capabilities {
    name = "EnableMongo"
  }
   lifecycle {
    //prevent_destroy = true
  }
}