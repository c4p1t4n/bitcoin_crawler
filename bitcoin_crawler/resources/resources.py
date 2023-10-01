from dataclasses import dataclass
from constructs import Construct
from aws_cdk.aws_events import Rule, Schedule
from aws_cdk.aws_events_targets import EcsTask
from aws_cdk import (
    Tags,
    Stack,
    Duration,
    aws_ecr as ecr,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_ecs as ecs,
    aws_events_targets as targets,
    aws_events as events,
    aws_lambda as _lambda,
    aws_sns_subscriptions as sns_subscriptions,
    aws_ec2 as ec2
)





def template_iam(actions: list, resources: list) -> iam.PolicyStatement:
    """
    Return a Policy Statement.

    Args:
        actions (list): A list of permissions to be applied.
        resources (list): A list of resources to which the actions will apply.
    Returns:
        iam.PolicyStatement: A policy statement defining permissions and resources.
    """

    return iam.PolicyStatement(
        effect=iam.Effect.ALLOW,
        actions=actions,
        resources=resources
    )


def template_policy(scope: Construct, id_name: str, statements: list) -> iam.Policy:
    """

    Args:
        scope: self
        id_name: policy_test
        statements: [iam.PolicyStatement(args)] or template_iam_principal(args)]
    """
    return iam.Policy(
        scope=scope,
        id=id_name,
        statements=statements
    )


def template_iam_principal(actions: list, resources: list, principals: list) -> iam.PolicyStatement:
    """
        Return a Policy statement
    Args:
        actions: permissions list example = ['s3:PutObject']
        resources: "arn:s3//example"
        
    """
    return iam.PolicyStatement(
        effect=iam.Effect.ALLOW,
        actions=actions,
        resources=resources,
        principals=principals
    )


def template_role(scope: Construct, id_name: str, role_name: str,service_name:str) -> iam.Role:
    """
        Return a Service Principal for use lambda
        Args: 
            id_name: id of role
            role_name: name of the role in AWS
            service_name: service aws that will assume the Role
    """
    return iam.Role(
            scope=scope,
            id=id_name,
            assumed_by=iam.ServicePrincipal(f'{service_name}.amazonaws.com'),
            role_name=role_name
        )
def template_cluster(scope:Construct,ecs_name,vpc:ec2.Vpc=None)->ecs.Cluster:
    """
    Return a ClusterECS
        Args:
            scope: self
            ecs_name: the name of the cluster ecs
            vpc: ec2.Vpc, note if vpc is none will use the default vpc
    Returns:
        ecs.Cluster
    """
    if not vpc:
        vpc =ec2.Vpc.from_lookup(scope, "VPC",
            is_default=True
        )

    return ecs.Cluster(scope,f'{ecs_name}_cluster', vpc=vpc)
