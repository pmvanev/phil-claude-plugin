resource "aws_vpc" "main" {
  cidr_block = "10.40.0.0/16"

  tags = {
    Name        = "orders"
    Environment = var.environment
    Name        = "orders-${var.environment}-vpc"
  }
}

resource "aws_subnet" "private" {
  count = length(var.subnet_cidrs)

  vpc_id     = aws_vpc.main.id
  cidr_block = var.subnet_cidrs[count.index]

  tags = {
    Name = "orders-private-${count.index}"
  }
}

resource "aws_eip" "nat" {
  count = var.enable_nat ? 1 : 0

  domain = "vpc"
}

resource "aws_elasticache_cluster" "replica" {
  count = var.replica_count

  cluster_id      = "orders-replica-${count.index}"
  engine          = "redis"
  node_type       = "cache.t4g.micro"
  num_cache_nodes = 1
}

module "dns" {
  source = "git::https://github.com/acme/terraform-aws-dns.git"

  zone_name = "orders.internal"
  vpc_id    = aws_vpc.main.id
}
