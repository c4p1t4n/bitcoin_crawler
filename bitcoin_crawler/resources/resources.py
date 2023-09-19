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
    aws_glue as glue,

)


def template_lambda(
    scope: Construct,
    iam_role: iam,
    lambda_handler: str,
    lambda_name: str,
    code_path: str,
    id_name: str,
    name: str,
    minutes: int
) -> _lambda.Function:
    """
    Return a lambda Function with 1GB of memory 
    """
    return _lambda.Function(
        scope=scope,
        memory_size=1024,
        role=iam_role,
        timeout=Duration.minutes(minutes),
        handler=lambda_handler,
        runtime=_lambda.Runtime.PYTHON_3_8,
        id=id_name,
        function_name=lambda_name,
        code=_lambda.Code.from_asset(code_path),
        layers=[
            # _lambda.LayerVersion.from_layer_version_arn(
            #     scope=scope,
            #     id=f'awswrangler3_{name}-{STAGE}',
            #     layer_version_arn=f'arn:aws:lambda:{REGION}:{ACCOUNT}:layer:awswrangler3:3'
            # ),
            # _lambda.LayerVersion.from_layer_version_arn(
            #     scope=scope,
            #     id=f'polars{name}-{STAGE}',
            #     layer_version_arn=f'arn:aws:lambda:us-east-1:288474932338:layer:polars:2'
            # )
        ],
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
        statements: [ ]
    """
    return iam.Policy(
        scope=scope,
        id=id_name,
        statements=statements
    )


def template_iam_principal(actions: list, resources: list, principals: list) -> iam.PolicyStatement:
    """

    """
    return iam.PolicyStatement(
        effect=iam.Effect.ALLOW,
        actions=actions,
        resources=resources,
        principals=principals
    )


def template_role_lambda(scope: Construct, id_name: str, role_name: str) -> iam.Policy:
    """
        Return a Service Principal for use lambda
        Args: 
            id_name: id of role
            role_name: name of the role in AWS
    """
    return iam.Role(
            scope=scope,
            id=id_name,
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            role_name=role_name
        )



def template_topic_sns(scope: Construct, id_name: str, topic_name: str) -> sns.Topic:
    sns_topic = sns.Topic(
        scope=scope,
        id=id_name,
        topic_name=topic_name
    )
    return sns_topic


def add_subscription_sqs(scope: Construct, sns_topic: sns.Topic, sqs_queue: sqs.Queue):
    topic_policy = sns.TopicPolicy(scope, "TopicPolicy",
                                   topics=[sns_topic]
                                   )
    topic_policy.document.add_statements(iam.PolicyStatement(
        actions=["sns:Publish"],
        principals=[iam.ServicePrincipal("sqs.amazonaws.com")],
        resources=[sns_topic.topic_arn]
    )
    )

    sns_topic.add_subscription(sns_subscriptions.SqsSubscription(sqs_queue))


def template_event_bridge(scope: Construct, id_name: str, duration: Duration, _lambda: _lambda.Function):
    event = events.Rule(
        scope=scope,
        id=id_name,
        schedule=events.Schedule.rate(duration),
        targets=[targets.LambdaFunction(_lambda)]
    )
    return event
