terraform {
  backend "s3" {
    bucket       = "acme-billing-tfstate"
    key          = "network/terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "this" {
  cidr_block           = "10.30.0.0/16"
  enable_dns_hostnames = true

  tags = {
    Name    = "billing-prod-vpc"
    Account = "777788889999"
  }
}

resource "aws_subnet" "private" {
  for_each = {
    "us-east-1a" = "10.30.1.0/24"
    "us-east-1b" = "10.30.2.0/24"
    "us-east-1c" = "10.30.3.0/24"
  }

  vpc_id            = aws_vpc.this.id
  cidr_block        = each.value
  availability_zone = each.key

  tags = {
    Name = "billing-prod-private-${each.key}"
  }
}
