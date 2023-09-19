import os
import aws_cdk as cdk
from bitcoin_crawler.bitcoin_crawler_stack import BitcoinCrawlerStackProd

APP = cdk.App()
os.environ['STAGE'] = 'prod'
STAGE = os.getenv('STAGE')
ENV = cdk.Environment(account='288474932338', region='us-east-1')
if STAGE=='prod':
    STACK = BitcoinCrawlerStackProd(APP, 'bitcoin-crawler-prod', env=ENV)

cdk.Tags.of(STACK).add('PROJECT', 'bitcoin_crawler')
APP.synth()
