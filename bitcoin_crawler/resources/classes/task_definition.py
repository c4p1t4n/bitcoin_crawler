from dataclasses import dataclass
from aws_cdk import (
    aws_ecs as ecs,
    aws_logs as logs,
    aws_iam as iam,
    )
from constructs import Construct

@dataclass
class TaskDefinitionArgs:
    id_class: str
    stage: str
    vcpu: int
    task_role: iam.Role
    ecr_image: str
    execution_role: iam.Role
    project_name: str

class TaskDefinitionFargate(ecs.TaskDefinition):

    def __init__(self,scope:Construct,args: TaskDefinitionArgs,**kwargs) -> None:
        cpu = 1024*args.vcpu
        memory_mib = 1024*args.vcpu*2
        super().__init__(
            scope, args.id_class,
            cpu=str(cpu),
            memory_mib=str(memory_mib),
            compatibility=ecs.Compatibility.FARGATE,
            execution_role=args.execution_role,
            task_role=args.task_role,
            family=f'{args.project_name}_task_definition-{args.stage}'
            ,**kwargs)

        log_group = logs.LogGroup(
            scope=self,
            id=f'/ecs/{args.project_name}_{args.stage}',
            log_group_name=f'/ecs/{args.project_name}_{args.stage}',
            retention=logs.RetentionDays.ONE_WEEK,
        )
        container = self.add_container(
            id=f'{args.project_name}_ecs-{args.stage}',
            image=ecs.ContainerImage.from_registry(args.ecr_image),
            memory_limit_mib=memory_mib,
            logging=ecs.LogDriver.aws_logs(
                stream_prefix=f'{args.project_name}-{args.stage}',
                log_group=log_group,
            ),
        )

        container.add_port_mappings(ecs.PortMapping(container_port=80))