# Script para configurar credenciales AWS
# Ejecutar este script antes de ejecutar terraform
# IMPORTANTE: Copia este archivo a set-aws-credentials.ps1 y reemplaza los valores con tus credenciales reales

# Reemplaza estos valores con tus credenciales reales
$AWS_ACCESS_KEY_ID = "ASIATC7JEXNEJOZYVLVA"
$AWS_SECRET_ACCESS_KEY = "kdd3wEiK3+LPOMq6BEO7CX/GOuctHo8klOod9zsm"
$AWS_SESSION_TOKEN = "IQoJb3JpZ2luX2VjEFwaCXVzLXdlc3QtMiJHMEUCIAQcMrmvW/czvdz9X2xQP+rsur+qv1QVhlyyQC8ftjRYAiEAxbnE23KbM23tuvS35nvi7PBq+s+9fmvSgQHZH8KMnZ0qswIIZRABGgwyMTI1NTI5NTY3NDQiDOR1nqgZ+2sIv5Pm+CqQAoapEKjKKAKTeouCyyIVdKLjF0IowHE2op10KgQDvsCjHxz916UoCoqyAdJXHgKHuU9Vdl/Jx8VLuhf0NYvXidNRb2dHz8IwAkKpbvfVVJ2X7mRmKMjRun+x3OuS/agt6GciQNI6H7B3+BfqicAte2EvBULNItJKDOtG5dHouNdQUqQ55lbBxnYXSaQql3dFUrs7nsNjL71PqtXedeHsLfpZqB2d1hEfC/Iparff0oIQhvYPYAGYMC/xtAa16rpfZr0qKo39MyUPXXP2zmAOUUZpiESHwTcxFTtQoezjhAdgN63G+QgIjiWskA3HKOIRnfm9Og7eEXDfb0UtfvVT2Ggw+oAUpo9aW6xtGPqLYFDnMIWpq8MGOp0BUnG64qUPWah7JgzT4mJ0JPPcizTX/R+4z8vG86GzUfE8OTEdIUsAkWBNT5gUOhUHN+sY3Ke0FX/H+GvtmZ78GCEN3Qv4JSM7zQVwKmj7WPb9AhKX9O11NWJ0+/SH7fpm+uGHBWRxVXWLn91yuzqbyeCFCQCC5AGr8mQzOpzEGs89o3FFhfVejL1lH6T7Ejy+X9Y7Du8sYi/ipn6c4Q=="  # Dejar vacío si no usas credenciales temporales

# Configurar variables de entorno
$env:AWS_ACCESS_KEY_ID = $AWS_ACCESS_KEY_ID
$env:AWS_SECRET_ACCESS_KEY = $AWS_SECRET_ACCESS_KEY

if ($AWS_SESSION_TOKEN -ne "") {
    $env:AWS_SESSION_TOKEN = $AWS_SESSION_TOKEN
}

