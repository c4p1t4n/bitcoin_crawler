from dataclasses import dataclass
from constructs import Construct
from aws_cdk import (
    Tags,
    Stack,
    Duration,
    aws_ecr as ecr,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_events_targets as targets,
    aws_events as events,
    aws_lambda as _lambda,
    aws_sns_subscriptions as sns_subscriptions,
)





def template_iam(actions: list, resources: list) -> iam.PolicyStatement:
    """
    Return a Policy Statement.

    Parameters:
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


def template_event_bridge(
        scope: Construct
        , id_name: str
        , duration: Duration, 
        _lambda: _lambda.Function):
    """
    
    """

    event = events.Rule(
        scope=scope,
        id=id_name,
        schedule=events.Schedule.rate(duration),
        targets=[targets.LambdaFunction(_lambda)]
    )
    return event
