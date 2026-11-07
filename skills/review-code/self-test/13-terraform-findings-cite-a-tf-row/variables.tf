variable "enable_nat" {
  type        = bool
  description = "Whether to create a NAT gateway's elastic IP."
  default     = false
}

variable "environment" {
  type = string
}

variable "replica_count" {
  type        = number
  description = "Identical read replicas of the order cache."
  default     = 2
}

variable "subnet_cidrs" {
  description = "Private subnet CIDR blocks, one subnet each."
}
