from aws_cdk import (
    # Duration,
    Stack,
    aws_ecs as ecs,
    aws_logs as logs
    # aws_sqs as sqs,
)
from constructs import Construct
from bitcoin_crawler.resources.classes.task_definition import (TaskDefinition,TaskDefinitionArgs)
from bitcoin_crawler.resources.resources import (
    template_role,
    template_iam,
    template_policy
)


class BitcoinCrawlerStackProd(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        role_ecs_bitcoin_crawler = template_role(
            scope=self,
            id_name="role_ecs_bitcoin_crawler",
            role_name="role_ecs_bitcoin_crawler",
            service_name='ecs-tasks'
        )
        ecr_statement = template_iam(
            actions=[
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
            ],
            resources=['*']    
        )

        s3_statement = template_iam(
            actions=[
                "ecs:RunTask",
                "ecs:StartTask",
                "ecs:StopTask",
                "ecs:DescribeTasks",
                "ecs:ListTasks",
                "ecs:DescribeTaskDefinition",
                "ecs:RegisterTaskDefinition",
                "ecs:DeregisterTaskDefinition",
                "ecs:ListTaskDefinitions",
                "ecs:UpdateService",
                "ecs:CreateService",
                "ecs:DeleteService",
                "ecs:ListServices",
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:DescribeLogGroups",
                "s3:PutObject"
            ],
            resources=['*']
        )

        policy_ecs = template_policy(
            scope=self,
            id_name='policy_ecs_bitcoin_crawler',
            statements=[
                ecr_statement,
                s3_statement
            ]
        )
        role_ecs_bitcoin_crawler.attach_inline_policy(policy_ecs)



        args = TaskDefinitionArgs(
            id_class='bitcoin_crawler_dev',
            stage='dev',
            vcpu=1,
            task_role=role_ecs_bitcoin_crawler,
            ecr_image='288474932338.dkr.ecr.us-east-1.amazonaws.com/bitcoin_crawler',
            execution_role=role_ecs_bitcoin_crawler,
            project_name='bitcoin_crawler',
        )


        TaskDefinition(self,args)
