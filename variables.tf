variable "APP-PREFIX" {
    type        = string
    sensitive   = false
}
variable "location" {
    description = "The Azure location where all resources in this deployment should be created"
    default = "uksouth"
}

variable "CLIENTID" {
    type        = string
    sensitive   = true
}
variable "CLIENTSECRET" {
    type        = string
    sensitive   = true
}
variable "loglevel" {
    description = "level for the logs."
    default = "ERROR"
}