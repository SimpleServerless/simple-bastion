# Shamelessly lifted from https://medium.com/faun/create-a-bastion-with-aws-cdk-d5ebfb91aef9

from aws_cdk import (
    core
)
from aws_cdk.aws_ec2 import BastionHostLinux, InstanceType, AmazonLinuxImage, \
    SubnetSelection, SecurityGroup, SubnetType, Vpc
import os
import boto3
import logging

log = logging.getLogger()

ssm = boto3.client('ssm')
vpc_id: str = ssm.get_parameter(Name="VpcId")['Parameter']['Value']

class CdkStack(core.Stack):
    security_group: SecurityGroup

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = Vpc.from_lookup(self, 'VPC', vpc_id=vpc_id)
        self.security_group = self.__create_security_group(vpc)

        bastion = BastionHostLinux(
            self, id,
            vpc=vpc,
            instance_name='simple-bastion',
            instance_type=InstanceType('t3a.nano'),
            machine_image=AmazonLinuxImage(),
            subnet_selection=SubnetSelection(subnet_type=SubnetType.PUBLIC),
            security_group=self.security_group,
        )
        core.CfnOutput(self, 'bastion-id', value=bastion.instance_id)

    def __create_security_group(self, vpc: Vpc) -> SecurityGroup:
        return SecurityGroup(
            scope=self,
            id='bastion-sg',
            security_group_name='bastion-sg',
            description='Security group for the bastion, no inbound open because we should access'
                        ' to the bastion via AWS SSM',
            vpc=vpc,
            allow_all_outbound=True
        )

app = core.App()

account = os.environ['AWS_ACCOUNT']
region = os.environ['AWS_DEFAULT_REGION']
CdkStack(app, "simple-bastion-us-east2-dev", env={"account": account, "region": region})

app.synth()