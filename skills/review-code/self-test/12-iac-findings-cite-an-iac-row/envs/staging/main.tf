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

module "network" {
  source = "../../modules/network"

  account_id = "444455556666"
  cidr_block = "10.20.0.0/16"
  name       = "billing-staging"
  region     = "us-east-1"
  private_subnets = {
    "us-east-1a" = "10.20.1.0/24"
    "us-east-1b" = "10.20.2.0/24"
  }
}
