from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from bitcoin_crawler.resources.resources import (
    template_role_lambda,
    template_iam,
    template_lambda,
    template_policy
)
from constructs import Construct


class BitcoinCrawlerStackProd(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        role_lambda_bitcoin_crawler = template_role_lambda(
            self,
            "role_lambda_bitcoin_crawler",
            "role_bitcoin_crawler"
        )
        s3_statement = template_iam(actions=['s3:PutObject'], resources=['*'])


        
        policy_lambda = template_policy(
            scope=self,
            id_name='policy_lambda_bitcoin_crawler',
            statements=[
                # s3_read_write_stmt,
                # cloudwatch_logs_stmt,
                # sqs_statement,
                s3_statement,
                # role_lambda_bitcoin_crawler
                # glue_statement
            ]
        )

        role_lambda_bitcoin_crawler.attach_inline_policy(policy_lambda)
        policy_lambda = template_lambda(
            self
            ,role_lambda_bitcoin_crawler
            ,'bitcoin_crawler_stack.lambda_handler'
            ,'lambda_bitcoin_crawler'
            ,'src/'
            ,'id_lambda_bitcoin_crawler',
            'lambda_bitcoin_crawler',
            5
        )



# class BitcoinCrawlerStackDev(Stack):

#     def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
#         super().__init__(scope, construct_id, **kwargs)

    
