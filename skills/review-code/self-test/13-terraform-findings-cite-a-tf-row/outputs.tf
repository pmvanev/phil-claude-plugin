output "private_subnet_ids" {
  description = "Ids of the private subnets, in the order of var.subnet_cidrs."
  value       = aws_subnet.private[*].id
}

output "vpc_id" {
  description = "Id of the orders VPC."
  value       = aws_vpc.main.id
}
