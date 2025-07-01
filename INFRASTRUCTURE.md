# Auth Login Signup Service - Infraestructura

Este documento describe la infraestructura del servicio de autenticación y registro de usuarios.

## Estructura actual

- `terraform-ec2-new/` - Configuración actual de Terraform para el despliegue en AWS ECS con instancias EC2
  - `main.tf` - Configuración principal de la infraestructura
  - `variables.tf` - Variables de configuración
  - `outputs.tf` - Salidas de la infraestructura
  - `ecs.tf` - Configuración de ECS
  - `database.tf` - Configuración de la base de datos RDS PostgreSQL
  - `set-aws-credentials.ps1` - Script para configurar credenciales de AWS

## Estado actual

- **Último despliegue exitoso**: 2025-07-01
- **Versión de PostgreSQL**: 16
- **Tipo de instancia RDS**: db.t3.micro
- **Tipo de instancia EC2**: t3.micro (Ubuntu)

## Cómo desplegar

1. Configurar credenciales de AWS:
   ```powershell
   .\terraform-ec2-new\set-aws-credentials.ps1
   ```

2. Inicializar Terraform:
   ```powershell
   cd terraform-ec2-new
   terraform init
   ```

3. Aplicar la configuración:
   ```powershell
   terraform apply
   ```

## Acceso

- **URL del ALB**: http://auth-service-ec2-new-lb-1326682257.us-east-1.elb.amazonaws.com
- **SSH a instancias EC2**: Usar la clave `auth-service-ec2-new-key`

## Notas importantes

- Los directorios antiguos de Terraform fueron archivados y eliminados para mantener el proyecto limpio.
- La configuración actual está optimizada para desarrollo (dev). Para producción, ajustar los tamaños de instancias y configuraciones según sea necesario.
