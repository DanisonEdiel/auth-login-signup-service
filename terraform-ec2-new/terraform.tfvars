aws_region = "us-east-1"
app_name = "auth"
environment = "dev"
image_tag = "latest"
ecr_repository_url = "danisonediel/auth-login-signup-service"
db_password = "Uzumymw260916_"
jwt_secret = "super-secret-key-change-in-production"
ssh_public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCoiurVhXe0fw1W8iZ8BDQc/TTq0Ns4F/HOiCwRoRum8e0JRvjh6VLeRCNiea2QtlO3ISH35u5eNO1XFvMyyviXrehQgbIO4NXD1gwD7iRbJrfdKPnJgnAS1Zr4njXWe0alYS8jKWmW5dWLIrsC3GXqF+F8jIuzcnN3377kcUCDOMHGzZdy8gu+1DHewUfOgX37+ZAK+gmTK+AIjqe+Qfr0I7/yjnNpna+kD8t6rdq/apvpL72XsMpzyJles/RlFi4RfmTBZBGG/4o3S5GXJlDgtdeOU4dXg+5pYH89XC/qA4P+NcTa0X3+oVbKuoXZVyFKl0fU/aDWyk/tx1+Wrz7P"

# Credenciales AWS (se recomienda usar set-aws-credentials.ps1 en lugar de definirlas aquí)
aws_access_key_id     = ""  # Dejar vacío y usar set-aws-credentials.ps1
aws_secret_access_key = ""  # Dejar vacío y usar set-aws-credentials.ps1
aws_session_token     = ""  # Dejar vacío y usar set-aws-credentials.ps1

# Configuración de escalado
desired_capacity = 1

# Plan de contingencia - Controlar qué recursos crear
create_resources = {
  security_groups = false  # Cambiar a false si ya existe
  key_pair        = false  # Cambiar a false si ya existe
  db_subnet_group = false  # Cambiar a false si ya existe
  ecs_cluster     = false  # Cambiar a false si ya existe
  log_group       = false  # Cambiar a false si ya existe
  iam_role        = false  # Cambiar a false si no tienes permisos IAM
  target_group    = false  # Cambiar a false si ya existe
}
