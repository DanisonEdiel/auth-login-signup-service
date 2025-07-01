// Función Lambda para asociar Elastic IPs a instancias EC2
const AWS = require('aws-sdk');
const ec2 = new AWS.EC2();
const autoscaling = new AWS.AutoScaling();

exports.handler = async (event) => {
    console.log('Evento recibido:', JSON.stringify(event, null, 2));
    
    try {
        // Extraer información del evento
        const instanceId = event.detail.EC2InstanceId;
        const lifecycleHookName = event.detail.LifecycleHookName;
        const autoScalingGroupName = event.detail.AutoScalingGroupName;
        
        console.log(`Procesando instancia: ${instanceId}`);
        
        // Obtener todas las Elastic IPs disponibles del entorno
        const eipIds = JSON.parse(process.env.EIP_IDS || '[]');
        console.log(`EIPs disponibles: ${eipIds.join(', ')}`);
        
        if (eipIds.length === 0) {
            console.log('No hay Elastic IPs configuradas');
            await completeLifecycleAction(lifecycleHookName, autoScalingGroupName, instanceId, 'CONTINUE');
            return { statusCode: 200, body: 'No hay Elastic IPs configuradas' };
        }
        
        // Obtener todas las direcciones elásticas
        const addresses = await ec2.describeAddresses().promise();
        console.log('Direcciones elásticas:', JSON.stringify(addresses, null, 2));
        
        // Buscar una EIP no asociada
        let availableEip = null;
        for (const eipId of eipIds) {
            const eip = addresses.Addresses.find(addr => addr.AllocationId === eipId);
            if (eip && !eip.AssociationId) {
                availableEip = eip;
                break;
            }
        }
        
        if (!availableEip) {
            console.log('No hay Elastic IPs disponibles sin asociar');
            await completeLifecycleAction(lifecycleHookName, autoScalingGroupName, instanceId, 'CONTINUE');
            return { statusCode: 200, body: 'No hay Elastic IPs disponibles' };
        }
        
        // Asociar la EIP a la instancia
        console.log(`Asociando EIP ${availableEip.AllocationId} a la instancia ${instanceId}`);
        await ec2.associateAddress({
            AllocationId: availableEip.AllocationId,
            InstanceId: instanceId
        }).promise();
        
        console.log('EIP asociada correctamente');
        
        // Completar la acción del ciclo de vida
        await completeLifecycleAction(lifecycleHookName, autoScalingGroupName, instanceId, 'CONTINUE');
        
        return {
            statusCode: 200,
            body: `EIP ${availableEip.AllocationId} asociada a la instancia ${instanceId}`
        };
    } catch (error) {
        console.error('Error:', error);
        
        // Intentar completar la acción del ciclo de vida incluso si hay un error
        if (event.detail) {
            try {
                await completeLifecycleAction(
                    event.detail.LifecycleHookName,
                    event.detail.AutoScalingGroupName,
                    event.detail.EC2InstanceId,
                    'CONTINUE'
                );
            } catch (lifecycleError) {
                console.error('Error al completar la acción del ciclo de vida:', lifecycleError);
            }
        }
        
        return {
            statusCode: 500,
            body: `Error: ${error.message}`
        };
    }
};

// Función para completar la acción del ciclo de vida
async function completeLifecycleAction(hookName, groupName, instanceId, result) {
    console.log(`Completando acción del ciclo de vida: ${hookName}, ${groupName}, ${instanceId}, ${result}`);
    
    return autoscaling.completeLifecycleAction({
        LifecycleHookName: hookName,
        AutoScalingGroupName: groupName,
        InstanceId: instanceId,
        LifecycleActionResult: result
    }).promise();
}
