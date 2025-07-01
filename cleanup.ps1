# Script para limpiar directorios de Terraform no utilizados
# Este script mueve los directorios antiguos a una carpeta de archivo

# Crear directorio de archivo si no existe
$archiveDir = "c:\PythonProjects\auth-login-signup-service\terraform-archive"
if (-not (Test-Path $archiveDir)) {
    New-Item -ItemType Directory -Path $archiveDir
    Write-Host "Directorio de archivo creado: $archiveDir"
}

# Mover directorios antiguos al archivo
$dirsToArchive = @(
    "c:\PythonProjects\auth-login-signup-service\terraform",
    "c:\PythonProjects\auth-login-signup-service\terraform-ec2"
)

foreach ($dir in $dirsToArchive) {
    if (Test-Path $dir) {
        $dirName = Split-Path $dir -Leaf
        $destPath = Join-Path $archiveDir $dirName
        
        # Si ya existe un directorio con el mismo nombre en el archivo, añadir timestamp
        if (Test-Path $destPath) {
            $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
            $destPath = "$destPath-$timestamp"
        }
        
        # Mover el directorio
        Move-Item -Path $dir -Destination $destPath
        Write-Host "Movido: $dir -> $destPath"
    } else {
        Write-Host "El directorio no existe, no se puede mover: $dir"
    }
}

Write-Host "`nLimpieza completada. Los directorios antiguos se han movido a: $archiveDir"
Write-Host "El directorio activo es: c:\PythonProjects\auth-login-signup-service\terraform-ec2-new"
