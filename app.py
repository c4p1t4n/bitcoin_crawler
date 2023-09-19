"""Module to create a env for dev in aws using local enviroments"""
import os
import aws_cdk as cdk
from bitcoin_crawler.bitcoin_crawler_stack import BitcoinCrawlerStackProd
# ,BitcoinCrawlerStackDev


app = cdk.App()
os.environ['STAGE'] = 'prod'
stage = os.getenv('STAGE')
env = cdk.Environment(account='288474932338', region='us-east-1')
if stage=='prod':
    stack = BitcoinCrawlerStackProd(app, 'bitcoin-crawler-prod', env=env)
# else:
#     stack = BitcoinCrawlerStackProd(app,'bitcoin-crawler-dev', env=env)




cdk.Tags.of(stack).add('PROJECT', 'bitcoin_crawler')




app.synth()
