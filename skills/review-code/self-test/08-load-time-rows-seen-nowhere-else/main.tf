provider "aws" {
  region = "us-gov-west-1"
}

resource "aws_lambda_function" "api" {
  function_name = "ledger-api"
  runtime       = "python3.12"
  handler       = "app.handler"
  filename      = "build/api.zip"
  role          = aws_iam_role.api.arn
  memory_size   = 1769
  timeout       = 15
  publish       = true

  snap_start {
    apply_on = "PublishedVersions"
  }
}

resource "aws_lambda_alias" "api_live" {
  name             = "live"
  function_name    = aws_lambda_function.api.function_name
  function_version = aws_lambda_function.api.version
}

resource "aws_lambda_function_url" "api" {
  function_name      = aws_lambda_function.api.function_name
  qualifier          = aws_lambda_alias.api_live.name
  authorization_type = "AWS_IAM"
}

resource "aws_lambda_function" "web" {
  function_name = "ledger-web"
  runtime       = "python3.12"
  handler       = "web.serve"
  filename      = "build/web.zip"
  role          = aws_iam_role.web.arn
  memory_size   = 1024
  timeout       = 10
  publish       = true
}

resource "aws_lambda_alias" "web_live" {
  name             = "live"
  function_name    = aws_lambda_function.web.function_name
  function_version = aws_lambda_function.web.version
}

resource "aws_lambda_provisioned_concurrency_config" "web" {
  function_name                     = aws_lambda_function.web.function_name
  qualifier                         = aws_lambda_alias.web_live.name
  provisioned_concurrent_executions = 1
}

resource "aws_apigatewayv2_api" "ledger" {
  name          = "ledger"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "web" {
  api_id                 = aws_apigatewayv2_api.ledger.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.web.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "shell" {
  api_id    = aws_apigatewayv2_api.ledger.id
  route_key = "GET /"
  target    = "integrations/${aws_apigatewayv2_integration.web.id}"
}

resource "aws_apigatewayv2_route" "assets_route" {
  api_id    = aws_apigatewayv2_api.ledger.id
  route_key = "GET /assets/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.web.id}"
}

resource "aws_apigatewayv2_route" "health" {
  api_id    = aws_apigatewayv2_api.ledger.id
  route_key = "GET /health"
  target    = "integrations/${aws_apigatewayv2_integration.web.id}"
}
