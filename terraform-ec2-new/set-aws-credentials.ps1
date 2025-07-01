# Script para configurar credenciales AWS
# Ejecutar este script antes de ejecutar terraform

# IMPORTANTE: Este es un archivo de ejemplo. Reemplaza estos valores con tus credenciales reales.
# NO subas este archivo con credenciales reales al repositorio.
$AWS_ACCESS_KEY_ID = "" # Ingresa tu AWS Access Key ID aquí
$AWS_SECRET_ACCESS_KEY = "" # Ingresa tu AWS Secret Access Key aquí
$AWS_SESSION_TOKEN = ""  # Ingresa tu AWS Session Token aquí si usas credenciales temporales

# Configurar variables de entorno
$env:AWS_ACCESS_KEY_ID = $AWS_ACCESS_KEY_ID
$env:AWS_SECRET_ACCESS_KEY = $AWS_SECRET_ACCESS_KEY

if ($AWS_SESSION_TOKEN -ne "") {
    $env:AWS_SESSION_TOKEN = $AWS_SESSION_TOKEN
}

Write-Host "Variables de entorno AWS configuradas correctamente."
Write-Host "Ahora puedes ejecutar: terraform plan o terraform apply"
