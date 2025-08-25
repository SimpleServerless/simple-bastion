# Shamelessly lifted from https://medium.com/faun/create-a-bastion-with-aws-cdk-d5ebfb91aef9


from aws_cdk import (
    Stack,
    CfnOutput,
    App,
    aws_ec2 as ec2,
)
from constructs import Construct
import os
import boto3
import logging

log = logging.getLogger()

ssm = boto3.client('ssm')
vpc_id: str = ssm.get_parameter(Name="VpcId")['Parameter']['Value']

class CdkStack(Stack):
    security_group: ec2.SecurityGroup

    def __init__(self, scope, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, 'VPC', vpc_id=vpc_id)
        self.security_group = self.__create_security_group(vpc)

        bastion = ec2.BastionHostLinux(
            self, id,
            vpc=vpc,
            instance_name='simple-bastion',
            instance_type=ec2.InstanceType('t3a.nano'),
            machine_image=ec2.AmazonLinuxImage(),
            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_group=self.security_group,
        )
        CfnOutput(self, 'bastion-id-output', value=bastion.instance_id, export_name="BastionInstanceId")
        CfnOutput(self, "bastion-sg-output", value=self.security_group.security_group_id, export_name="BastionSG")

    def __create_security_group(self, vpc: ec2.Vpc) -> ec2.SecurityGroup:
        return ec2.SecurityGroup(
            self,
            id='bastion-sg',
            security_group_name='bastion-sg',
            description='Security group for the bastion, no inbound open because we should access'
                        ' to the bastion via AWS SSM',
            vpc=vpc,
            allow_all_outbound=True
        )

app = App()

account = os.environ['AWS_ACCOUNT']
region = os.environ['AWS_DEFAULT_REGION']
CdkStack(app, "simple-bastion-us-east2-dev", env={"account": account, "region": region})

app.synth()