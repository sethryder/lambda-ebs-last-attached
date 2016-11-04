import boto3
import logging

attached_key_name = 'Last Attached Name'
attached_key_instance_id = 'Last Attached ID'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ec2_client = boto3.client('ec2')

def lambda_handler(event, context):
    logger.info('Starting EBS volume check')

    response = ec2_client.describe_volumes(
        Filters=[{
            'Name': 'attachment.status',
            'Values': [
                'attached',
            ]
        }]
    )

    for volume in response['Volumes']:
        name_key_needs_update = True
        instance_id_needs_update = True

        if volume['Attachments'][0]['InstanceId']:
            instance_id = volume['Attachments'][0]['InstanceId']
            instance_tags = ec2_client.describe_tags(
                Filters=[{
                    'Name': 'resource-id',
                    'Values': [
                        instance_id,
                ]},
                {
                    'Name': 'key',
                    'Values': [
                        'Name',
                    ],
                }]
            )

            instance_name = instance_tags['Tags'][0]['Value']

            if 'Tags' in volume:
                for volume_tag in volume['Tags']:
                    if volume_tag['Key'] == attached_key_name:
                        if volume_tag['Value'] == instance_name:
                            name_key_needs_update = False

                    if volume_tag['Key'] == attached_key_instance_id:
                        if volume_tag['Value'] == instance_id:
                            instance_id_needs_update = False

            if name_key_needs_update or instance_id_needs_update:
                logger.info('Updating key(s) for %s', volume['VolumeId'])
                response = ec2_client.create_tags(
                    Resources=[
                        volume['VolumeId'],
                    ],
                    Tags=[{
                            'Key': attached_key_name,
                            'Value': instance_name,
                        },
                        {
                            'Key': attached_key_instance_id,
                            'Value': instance_id,
                        }]
                )

    logger.info('Finished EBS volume check')
