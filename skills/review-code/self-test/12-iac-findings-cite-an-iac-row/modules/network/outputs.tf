output "private_subnet_ids" {
  description = "Private subnet ids, keyed by availability zone."
  value       = { for az, subnet in aws_subnet.private : az => subnet.id }
}

output "vpc_id" {
  description = "Id of the VPC."
  value       = aws_vpc.this.id
}
