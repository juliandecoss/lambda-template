resource "aws_lambda_function" "lambda-name" {
  function_name = "my-lambda-name"

  # The bucket name as created earlier with "aws s3api create-bucket"
  s3_bucket = var.s3_bucket
  s3_key    = "${var.lambda_name}/v${var.app_version}/lambda-go.zip"

  # "main" is the filename within the zip file (main.js) and "handler"
  # is the name of the property under which the handler function was
  # exported in that file.
  handler = "main"
  runtime = "go1.x"
  #handler       = "index.handler"
  #runtime       = "python3.8"
  #versioning    = true
  memory_size   = 128
  #timeout       = 600

  role = aws_iam_role.lambda_exec.arn

  environment {
    variables = {
      # WHATSAPP_TOKEN = var.whatsapp_token
    }
  }

}

# IAM role which dictates what other AWS services the Lambda function
# may access.
resource "aws_iam_role" "lambda_exec" {
  name = "lambda-name-policy"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF

# Política adicional para permitir escritura en CloudWatch Logs
  inline_policy {
    name = "lambda-name-cloudwatch-logs-policy"

    policy = jsonencode({
      Version = "2012-10-17",
      Statement = [
        {
          Action = [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ],
          Effect   = "Allow",
          Resource = "*"
        }
      ]
    })
  }
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda-name.function_name
  principal     = "apigateway.amazonaws.com"

  # The /*/* portion grants access from any method on any resource
  # within the API Gateway "REST API".
  source_arn = "${aws_api_gateway_rest_api.lambda_name.execution_arn}/*/*"
}

resource "aws_cloudwatch_log_group" "log_group" {
  name              = "/aws/lambda/${aws_lambda_function.lambda-name.function_name}"
  retention_in_days = var.retention_in_days
}

#Add a layer
# resource "aws_lambda_layer_version" "lambda_requirements_layer" {
#   filename   = "./build/layer.zip"
#   layer_name = "t01-use1-events-platform-layer-requirements-prd"

#   compatible_runtimes = ["python3.8"]
# }

# CREATE A CRON JOB TO INVOKE LAMBDA missing permissions
#cron(00 12 ? * MON *)
# resource "aws_cloudwatch_event_rule" "send_login_reporter_for_product" {
#   name                = "send-login-reporter-for-product"
#   description         = "Send Idp metrics every friday at 17:03:00 MX time"
#   schedule_expression = "cron(03 23 ? * FRI *)"
# }

# resource "aws_cloudwatch_event_target" "lambda_send_login_reporter_for_product" {
#   rule      = aws_cloudwatch_event_rule.send_login_reporter_for_product.name
#   target_id = "login_reporter"
#   arn       = module.login_reporter.arn
# }

# resource "aws_lambda_permission" "permission_login_reporter" {
#   statement_id  = "AllowExecutionFromCloudWatch"
#   action        = "lambda:InvokeFunction"
#   function_name = "login-reporter"
#   principal     = "events.amazonaws.com"
#   source_arn    = aws_cloudwatch_event_rule.send_login_reporter_for_product.arn
# }

# resource "aws_lambda_function_event_invoke_config" "retry_attemps" {
#   function_name                = "login-reporter"
#   maximum_retry_attempts       = 1
#   maximum_event_age_in_seconds = 900
# }