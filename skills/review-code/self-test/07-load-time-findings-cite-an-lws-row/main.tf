provider "aws" {
  region = "us-east-1"
}

resource "aws_lambda_function" "api" {
  function_name = "reports-api"
  runtime       = "python3.12"
  handler       = "handler.handler"
  filename      = "build/api.zip"
  memory_size   = 1769
  role          = aws_iam_role.api.arn

  vpc_config {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [aws_security_group.reports_db_clients.id]
  }
}

resource "aws_lambda_function" "shell" {
  function_name = "reports-shell"
  runtime       = "python3.12"
  handler       = "web_shell.serve"
  filename      = "build/shell.zip"
  role          = aws_iam_role.shell.arn
}

resource "aws_lambda_function" "thumbnailer" {
  function_name = "reports-thumbnailer"
  runtime       = "python3.12"
  handler       = "thumbnailer.handler"
  filename      = "build/thumbnailer.zip"
  role          = aws_iam_role.thumbnailer.arn
}

resource "aws_apigatewayv2_integration" "api" {
  api_id                 = aws_apigatewayv2_api.web.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.api.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "api" {
  api_id    = aws_apigatewayv2_api.web.id
  route_key = "ANY /api/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.api.id}"
}

resource "aws_apigatewayv2_integration" "shell" {
  api_id                 = aws_apigatewayv2_api.web.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.shell.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "assets" {
  api_id    = aws_apigatewayv2_api.web.id
  route_key = "GET /assets/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.shell.id}"
}

resource "aws_apigatewayv2_route" "shell_root" {
  api_id    = aws_apigatewayv2_api.web.id
  route_key = "GET /"
  target    = "integrations/${aws_apigatewayv2_integration.shell.id}"
}
