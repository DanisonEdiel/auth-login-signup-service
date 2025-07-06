# Terraform AWS ECS EC2 Deployment

Este directorio contiene la configuración de Terraform para desplegar el servicio de autenticación y registro de usuarios en AWS ECS con instancias EC2.

## Configuración de credenciales AWS

Para configurar las credenciales de AWS de forma segura, sigue estos pasos:

1. Copia el archivo de ejemplo a un archivo local:
   ```
   cp set-aws-credentials.example.ps1 set-aws-credentials.ps1
   ```

2. Edita el archivo `set-aws-credentials.ps1` y añade tus credenciales AWS:
   ```powershell
   $AWS_ACCESS_KEY_ID = "TU_ACCESS_KEY_ID"
   $AWS_SECRET_ACCESS_KEY = "TU_SECRET_ACCESS_KEY"
   $AWS_SESSION_TOKEN = "TU_SESSION_TOKEN"  # Solo si usas credenciales temporales
   ```

3. Ejecuta el script para configurar las variables de entorno:
   ```powershell
   .\set-aws-credentials.ps1
   ```

> **IMPORTANTE**: El archivo `set-aws-credentials.ps1` está incluido en `.gitignore` para evitar subir credenciales al repositorio. NUNCA subas este archivo con credenciales reales al repositorio.

## Despliegue de la infraestructura

Una vez configuradas las credenciales, puedes desplegar la infraestructura:

```powershell
terraform init
terraform plan
terraform apply
```

## Componentes de la infraestructura

- **ECS Cluster**: Cluster de ECS para ejecutar el servicio
- **EC2 Instances**: Instancias EC2 con Ubuntu 20.04 y el agente ECS
- **RDS PostgreSQL**: Base de datos PostgreSQL para almacenar los datos de usuarios
- **Application Load Balancer**: Balanceador de carga para distribuir el tráfico
- **Elastic IPs**: IPs elásticas para las instancias EC2 (configuración opcional)

## Elastic IPs para instancias EC2

La configuración incluye la asignación automática de IPs elásticas a las instancias EC2 mediante una función Lambda. Esto permite que las instancias mantengan una dirección IP pública estática, incluso después de reiniciarse.

Para modificar el número de instancias y IPs elásticas, ajusta la variable `desired_capacity` en el archivo `terraform.tfvars` o al ejecutar `terraform apply`:

```powershell
terraform apply -var="desired_capacity=2"
```

## Acceso SSH

Para acceder a las instancias EC2 mediante SSH, utiliza la clave SSH configurada en `terraform.tfvars`.
