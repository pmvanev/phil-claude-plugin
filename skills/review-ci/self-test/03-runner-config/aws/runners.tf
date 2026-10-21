# The runners' registration on GitLab, and the two pools' job instances.

resource "gitlab_user_runner" "open" {
  runner_type  = "group_type"
  group_id     = var.group_id
  description  = "open"
  untagged     = true
  access_level = "not_protected"
}

resource "gitlab_user_runner" "deploy" {
  runner_type  = "group_type"
  group_id     = var.group_id
  description  = "deploy"
  tag_list     = ["deploy"]
  untagged     = true
  access_level = "not_protected"
}

resource "aws_launch_template" "open" {
  name_prefix   = "runner-open-"
  image_id      = var.runner_ami
  instance_type = "c7i.xlarge"
  metadata_options {
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }
}

resource "aws_launch_template" "deploy" {
  name_prefix   = "runner-deploy-"
  image_id      = var.runner_ami
  instance_type = "c7i.large"
  iam_instance_profile {
    name = aws_iam_instance_profile.deploy.name
  }
  metadata_options {
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }
}

resource "aws_iam_instance_profile" "deploy" {
  name = "runner-deploy"
  role = aws_iam_role.deploy.name
}

# The deploy jobs' role: assumed by the deploy instances, and by GitLab OIDC for main's pipelines.
resource "aws_iam_role" "deploy" {
  name = "runner-deploy"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "ec2.amazonaws.com" }
        Action    = "sts:AssumeRole"
      },
      {
        Effect    = "Allow"
        Principal = { Federated = var.gitlab_oidc_provider_arn }
        Action    = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "gitlab.example.invalid:sub" = "project_path:acme/storefront:ref_type:branch:ref:main"
          }
        }
      }
    ]
  })
}

# Each pool's Auto Scaling group boots its launch template; the runner manager scales the group.
resource "aws_autoscaling_group" "open" {
  name                = "runner-open"
  min_size            = 0
  max_size            = 16
  vpc_zone_identifier = var.job_subnets
  launch_template {
    id      = aws_launch_template.open.id
    version = "$Latest"
  }
}

resource "aws_autoscaling_group" "deploy" {
  name                = "runner-deploy"
  min_size            = 0
  max_size            = 4
  vpc_zone_identifier = var.job_subnets
  launch_template {
    id      = aws_launch_template.deploy.id
    version = "$Latest"
  }
}

# The runner manager's config.toml, rendered for the gateway's cloud-init.
locals {
  config_toml = templatefile("${path.module}/config.toml.tftpl", {
    open_token   = gitlab_user_runner.open.token
    deploy_token = gitlab_user_runner.deploy.token
    open_asg     = aws_autoscaling_group.open.name
    deploy_asg   = aws_autoscaling_group.deploy.name
  })
}
