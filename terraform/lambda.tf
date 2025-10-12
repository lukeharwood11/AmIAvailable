resource "aws_iam_role" "lambda_role" {
  name = "amia-api-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Attach the basic execution role policy for CloudWatch Logs access
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# IAM policy for Lambda to access Secrets Manager
resource "aws_iam_role_policy" "lambda_secrets_policy" {
  name = "amia-lambda-secrets-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resource = [
          aws_secretsmanager_secret.api_secrets.arn
        ]
      }
    ]
  })
}


# Secrets Manager secret for API configuration
resource "aws_secretsmanager_secret" "api_secrets" {
  name        = "amia-api-secrets"
  description = "Secrets for the Amia API Lambda function"

  tags = local.tags
}

# Secret version with actual values
resource "aws_secretsmanager_secret_version" "api_secrets_version" {
  secret_id = aws_secretsmanager_secret.api_secrets.id
  secret_string = jsonencode({
    "OPENAI__API_KEY"            = openai_project_service_account.amia.api_key
    "GOOGLE__CLIENT_SECRET"      = var.google_client_secret
    "SUPABASE__SERVICE_ROLE_KEY" = var.supabase_service_role_key
    "DATABASE__USERNAME"         = var.database_username
    "DATABASE__PASSWORD"         = var.database_password
  })
}

resource "aws_lambda_function" "api" {
  function_name = "amia-api"
  role          = aws_iam_role.lambda_role.arn
  image_uri     = var.api_image_uri
  package_type  = "Image"
  timeout       = 30  # 30 seconds timeout
  memory_size   = 512 # 512 MB memory
  # publish       = true  # Required for provisioned concurrency

  environment {
    variables = {
      SECRETS_MANAGER_SECRET_NAME = aws_secretsmanager_secret.api_secrets.name
      ENVIRONMENT                 = "prod"
      GOOGLE__CLIENT_ID           = var.google_client_id
      SUPABASE__ANON_KEY          = var.supabase_anon_key
      SUPABASE__URL               = var.supabase_url
    }
  }
}

# # create an alias for the lambda function
# resource "aws_lambda_alias" "api" {
#   name             = "latest"
#   function_name    = aws_lambda_function.api.function_name
#   function_version = aws_lambda_function.api.version
# }

# # create a provisioned concurrency configuration for the lambda function
# resource "aws_lambda_provisioned_concurrency_config" "api" {
#   function_name    = aws_lambda_function.api.function_name
#   provisioned_concurrent_executions = 1
#   qualifier = aws_lambda_alias.api.name
# }