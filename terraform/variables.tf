variable "project" {
  type        = string
  description = "The Google Cloud Platform project name"
}

variable "service" {
  description = "Name of the service"
  type        = string
  default     = "examsched"
}

variable "region" {
  default = "europe-west3"
  type    = string
}

variable "instance_name" {
  description = "Name of the postgres instance (PROJECT_ID:REGION:INSTANCE_NAME))"
  type        = string
  default     = "psql"
}