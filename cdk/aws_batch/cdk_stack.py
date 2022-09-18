from aws_cdk import (
    Stack,
    CfnOutput,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    aws_s3_assets as s3_assets,
    aws_ecs as ecs
)

import aws_cdk.aws_batch_alpha as batch
from constructs import Construct

class BatchStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "VPC")
        
        my_security_group = ec2.SecurityGroup(self, "SecurityGroup", vpc=vpc, allow_all_outbound=True)
        my_security_group.add_ingress_rule(ec2.Peer.ipv4("82.29.120.181/32"), ec2.Port.all_traffic(), "my house")
        my_security_group.add_ingress_rule(ec2.Peer.ipv4("10.0.0.0/16"), ec2.Port.all_traffic(), "my vpc")

        # default is managed
        compute_environment = batch.ComputeEnvironment(self, "AWSManagedComputeEnv",
            compute_resources=batch.ComputeResources(
                vpc=vpc,
                security_groups=[my_security_group],
                allocation_strategy=batch.AllocationStrategy.BEST_FIT_PROGRESSIVE
            )
        )

        job_queue = batch.JobQueue(self, "JobQueue",
            compute_environments=[batch.JobQueueComputeEnvironment(
                # Defines a collection of compute resources to handle assigned batch jobs
                compute_environment=compute_environment,
                # Order determines the allocation order for jobs (i.e. Lower means higher preference for job assignment)
                order=1
            )
            ]
        )

        batch.JobDefinition(self, "JobDefLocal",
            container=batch.JobDefinitionContainer(
                # todo-list is a directory containing a Dockerfile to build the application
                image=ecs.ContainerImage.from_asset("../docker-image")
            )
        )
        
        l = ("ami-03a7c686223124056", ec2.InstanceClass.MEMORY6_GRAVITON), \ # AL3 ARM64
        ("ami-05eccde7d55ac81f8", ec2.InstanceClass.MEMORY5_AMD), \ # AL2 AMD
        ("ami-0dd5421b8e4031719", ec2.InstanceClass.G4DN) # Windows x86
        
        for ami, instance_class in l:
            
            print(ami)
            print(instance_class)

            al2_nice_dcv = ec2.MachineImage.generic_linux({
                "eu-west-1": ami
            })
            
            
            root_volume = ec2.BlockDevice(
                device_name="/dev/xvda",
                volume=ec2.BlockDeviceVolume.ebs(300),
            )
    
            my_ec2_instance = ec2.Instance(self, "Nice_DCV_" + ami ,
                vpc=vpc,
                instance_type=ec2.InstanceType.of(instance_class, ec2.InstanceSize.XLARGE2),
                machine_image=al2_nice_dcv,
                security_group=my_security_group,
                block_devices=[root_volume],
                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType('PUBLIC')),
                key_name="aws_ssh",
            )
    
            my_ec2_instance.role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name('AmazonSSMManagedInstanceCore'))
    
            asset = s3_assets.Asset(self, "Asset_" + ami,
                path="./aws_batch/configure.sh"
            )
    
            local_path = my_ec2_instance.user_data.add_s3_download_command(
                bucket=asset.bucket,
                bucket_key=asset.s3_object_key,
                region="eu-west-2"
            )
            my_ec2_instance.user_data.add_execute_file_command(
                file_path=local_path
            )
            asset.grant_read(my_ec2_instance.role)
    
            # print the IAM role arn for this service account
            CfnOutput(self, "IP_" + ami + "_" + str(instance_class), value=my_ec2_instance.instance_public_ip)
        