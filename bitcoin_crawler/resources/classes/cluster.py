from dataclasses import dataclass
from aws_cdk import (
    aws_ecs as ecs,
    aws_logs as logs,
    aws_iam as iam,
    aws_ec2 as ec2
    )
from constructs import Construct




class ClusterECS(Construct):

    def __init__(self,scope:Construct,id_class:str,cluster_name:str,vpc:ec2.Vpc ,**kwargs) -> None:
        super().__init__(scope, id_class,**kwargs)
        
        ecs.Cluster(self, cluster_name, vpc=vpc)
