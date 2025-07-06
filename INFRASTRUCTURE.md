# Auth Login Signup Service - Infrastructure

This document describes the infrastructure of the authentication and user registration service.

## Current Structure

- `terraform-ec2-new/` - Current Terraform configuration for deployment in AWS ECS with EC2 instances
  - `main.tf` - Main infrastructure configuration
  - `variables.tf` - Configuration variables
  - `outputs.tf` - Infrastructure outputs
  - `ecs.tf` - ECS configuration
  - `database.tf` - RDS PostgreSQL database configuration
  - `set-aws-credentials.ps1` - Script para configurar credenciales de AWS

## Current State

- **Last successful deployment**: 2025-07-01
- **PostgreSQL version**: 16
- **RDS instance type**: db.t3.micro
- **EC2 instance type**: t3.micro (Ubuntu)

## How to deploy

1. Configure AWS credentials:
   ```powershell
   .\terraform-ec2-new\set-aws-credentials.ps1
   ```

2. Initialize Terraform:
   ```powershell
   cd terraform-ec2-new
   terraform init
   ```

3. Apply the configuration:
   ```powershell
   terraform apply
   ```

## Access

- **URL del ALB**: http://auth-service-ec2-new-lb-1326682257.us-east-1.elb.amazonaws.com
- **SSH to EC2 instances**: Use the `auth-service-ec2-new-key` key

## Important Notes

- The old Terraform directories were archived and deleted to keep the project clean.
- The current configuration is optimized for development (dev). For production, adjust instance sizes and configurations as needed.
