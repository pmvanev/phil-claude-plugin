variable "account_id" {
  type        = string
  description = "AWS account the network belongs to."
  default     = "111122223333"
}

variable "cidr_block" {
  type        = string
  description = "CIDR block of the VPC."
}

variable "name" {
  type        = string
  description = "Prefix for every resource name."
}

variable "private_subnets" {
  type        = map(string)
  description = "Private subnet CIDR blocks, keyed by availability zone."
}

variable "region" {
  type        = string
  description = "AWS region to deploy into."
}
