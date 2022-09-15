from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs
)
import aws_cdk.aws_batch_alpha as batch
from constructs import Construct

class BatchStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "VPC")

        # default is managed
        compute_environment = batch.ComputeEnvironment(self, "AWSManagedComputeEnv",
            compute_resources=batch.ComputeResources(
                vpc=vpc
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
