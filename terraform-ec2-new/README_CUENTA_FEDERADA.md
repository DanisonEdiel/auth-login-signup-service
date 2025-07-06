# Guía para Terraform con Cuenta Federada AWS

Esta guía explica cómo desplegar infraestructura usando Terraform con una cuenta federada de AWS que tiene permisos limitados.

## Limitaciones de Cuentas Federadas

Las cuentas federadas AWS típicamente no pueden:
- Crear roles IAM
- Crear políticas IAM
- Usar AWS Secrets Manager
- Crear ciertos recursos que requieren permisos elevados

## Pasos para el Despliegue

### 1. Configurar Credenciales AWS

Siempre carga las credenciales AWS temporales antes de ejecutar comandos Terraform:

```powershell
. .\set-aws-credentials.ps1
```

### 2. Ejecutar Terraform de Forma Selectiva

En lugar de ejecutar `terraform apply` para todo, aplica solo los recursos que tu cuenta puede crear:

```powershell
# Inicializar Terraform
terraform init

# Crear solo la IP elástica
terraform apply -target=aws_eip.ec2_eip

# Verificar la IP elástica creada
terraform output elastic_ip
```

### 3. Asociar la IP Elástica Manualmente

Una vez que tengas una instancia EC2 (creada manualmente o por otra parte de Terraform):

1. Edita el archivo `associate_eip.ps1`:
   - Actualiza `$instanceId` con el ID de tu instancia EC2
   - Actualiza `$allocationId` con el ID de asignación de la IP elástica

2. Ejecuta el script:
   ```powershell
   . .\associate_eip.ps1
   ```

### 4. Configurar GitHub Actions

Configura estos secretos en tu repositorio GitHub:

- `EC2_HOST`: La IP elástica asignada
- `EC2_USERNAME`: `ubuntu` (para Ubuntu) o `ec2-user` (para Amazon Linux)
- `EC2_SSH_KEY`: El contenido completo de tu archivo .pem
- `JWT_SECRET`: Tu secreto JWT
- `DATABASE_URL`: La URL de conexión a tu base de datos
- `MESSAGE_BROKER_URL`: La URL del message broker (opcional)

## Solución de Problemas

### Error de Permisos IAM

Si ves errores como:
```
Error: User is not authorized to perform: iam:CreateRole
```

Significa que estás intentando crear recursos que requieren permisos elevados. Usa el enfoque selectivo descrito arriba.

### Recursos Existentes

Si los recursos ya existen, usa `terraform import` para incorporarlos a tu estado de Terraform:

```powershell
terraform import aws_security_group.nombre_recurso sg-id
```
