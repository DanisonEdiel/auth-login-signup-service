# Elastic IP para instancias EC2
resource "aws_eip" "ec2_eip" {
  count = var.desired_capacity # Crear tantas EIPs como instancias deseadas
  
  domain = "vpc"
  
  tags = {
    Name        = "${var.app_name}-eip-${count.index}"
    Environment = var.environment
  }
}

# Script de ciclo de vida para asociar EIPs a instancias EC2 cuando se lanzan
resource "aws_autoscaling_lifecycle_hook" "ec2_launch_hook" {
  name                   = "${var.app_name}-launch-hook"
  autoscaling_group_name = aws_autoscaling_group.this.name
  default_result         = "CONTINUE"
  heartbeat_timeout      = 300
  lifecycle_transition   = "autoscaling:EC2_INSTANCE_LAUNCHING"
}

# Política de IAM para permitir asociar/desasociar EIPs
resource "aws_iam_policy" "eip_policy" {
  name        = "${var.app_name}-eip-policy"
  description = "Permite asociar/desasociar Elastic IPs"
  
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "ec2:AssociateAddress",
          "ec2:DisassociateAddress",
          "ec2:DescribeAddresses",
          "autoscaling:CompleteLifecycleAction"
        ],
        Effect   = "Allow",
        Resource = "*"
      }
    ]
  })
}

# Función Lambda para asociar EIPs a instancias EC2
resource "aws_lambda_function" "associate_eip" {
  function_name = "${var.app_name}-associate-eip"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  runtime       = "nodejs14.x"
  timeout       = 60
  
  environment {
    variables = {
      EIP_IDS = jsonencode([for eip in aws_eip.ec2_eip : eip.id])
    }
  }
  
  # Código de la función Lambda (simplificado)
  filename = "${path.module}/lambda_function.zip"
  
  depends_on = [
    aws_eip.ec2_eip
  ]
}

# Rol de IAM para la función Lambda
resource "aws_iam_role" "lambda_role" {
  name = "${var.app_name}-lambda-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Adjuntar política al rol de Lambda
resource "aws_iam_role_policy_attachment" "lambda_eip_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.eip_policy.arn
}

# Evento de CloudWatch para activar la función Lambda cuando se lanza una instancia
resource "aws_cloudwatch_event_rule" "asg_launch" {
  name        = "${var.app_name}-asg-launch"
  description = "Captura eventos de lanzamiento de instancias EC2"
  
  event_pattern = jsonencode({
    source      = ["aws.autoscaling"],
    detail-type = ["EC2 Instance-launch Lifecycle Action"]
    detail = {
      AutoScalingGroupName = [aws_autoscaling_group.this.name]
    }
  })
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.asg_launch.name
  target_id = "InvokeLambda"
  arn       = aws_lambda_function.associate_eip.arn
}

# Permiso para que CloudWatch invoque la función Lambda
resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.associate_eip.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.asg_launch.arn
}
