# Script para configurar credenciales AWS
# Ejecutar este script antes de ejecutar terraform

# Reemplaza estos valores con tus credenciales reales
$AWS_ACCESS_KEY_ID = "ASIATC7JEXNEEBN7VX42"
$AWS_SECRET_ACCESS_KEY = "geUi3Ig2RJmUihH+vXN1geFoFSt6ceuBOfaDDxXz"
$AWS_SESSION_TOKEN = "IQoJb3JpZ2luX2VjENn//////////wEaCXVzLXdlc3QtMiJGMEQCIBHb208vzNsjuEcOEI5N4kxPGJ8djPG1qWjxm2S+AbjMAiAYujCKJgFQNXjZi3cM1RaKnzcNTPffRPA92m41atkk/Sq8AgjR//////////8BEAEaDDIxMjU1Mjk1Njc0NCIMGqgw8o16zxYGo8lkKpACsJxLQ8OUKtYu12VBN77U81Y6kk/57ZUW0H+1esZfZnCkBBc0NaPXkk1e1dMDePkKkqhaRNAOAZJoUsF3AjNkXuIu+SyrdqDrUW6xYCUzFFdEo4COdYhpV7B2y+hcZhI5duGKCW81RfGdVaeRa+l0lI2IzJ/6LFKcVpesnjsyh9QgFcnF18kBr5xB1p+dkGpEog5irCkoLDo/mkEMb4tPkKyP1qgu2NR4Y1WK1MjtJeA9idz9tI+czIkWzOfXXnnAGrF2Pl3XuBN6fGaLteCcJjNtdPjX9y76AKYCUsmCwp7SmS3eZCk80wmEIhsB123u0fL/8v7NVc1Hihc6xTRcxoEf+09P1LZ2rpFQ4d4XBoYw6rSOwwY6ngGrLyQJF6MbzOR35iKTbnFjxxS96Gya2Iij1bWPbAnIAwFoBCt4/LlGozflUrCyp9JQpXRz4NAmSHR3WgoWh/I1sp6tzelrrIcJB1NtI2TqtOYhsdvdWEDehBdDTFPYvJd8aGAhYABg36Ck3d3Qc5KUfe2mfmn6Z/PQEDGhYPKMsZDMnM82Y4+LIO2Zq7ndd0UJPrTwurDvTNRqRF8ncg=="  # Dejar vacío si no usas credenciales temporales

# Configurar variables de entorno
$env:AWS_ACCESS_KEY_ID = $AWS_ACCESS_KEY_ID
$env:AWS_SECRET_ACCESS_KEY = $AWS_SECRET_ACCESS_KEY

if ($AWS_SESSION_TOKEN -ne "") {
    $env:AWS_SESSION_TOKEN = $AWS_SESSION_TOKEN
}

Write-Host "Variables de entorno AWS configuradas correctamente."
Write-Host "Ahora puedes ejecutar: terraform plan o terraform apply"
