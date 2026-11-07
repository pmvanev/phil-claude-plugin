terraform {
  required_version = ">= 1.11"

  backend "s3" {
    bucket       = "acme-orders-tfstate"
    key          = "staging/network/terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.80"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}
