# Simple Bastion

If you're at home building a simple serverless API on AWS that uses an RDS database hopefully your database
is on a private subnet and protected from Internet access. This means you may be looking for a simple but cheap way to deploy
and run a bastion host that you can tunnel through to your database. I was there once and had a hard time finding a nice
turnkey solution so I made this project, hope it helps. If you need help deploying a low cost RDS database to your
VPC I have something else you might want to check out [here](https://github.com/SimpleServerless/simple-database).

This project uses CDK to deploy a t3a.nano ($3.50/month) bastion host for the purpose of tunneling to an RDS instance on a private subnet.
Because I'm too cheap to pay even $3.50/month there is also a CloudFormation template `bastion_killer.yaml` that deploys 
a lambda that will kill your bastion host every night at 11:00 MST. Finally the script `start_bastion.sh` contains
the command needed to restart your bastion host from your shell. So if you start the bastion at 7:00 three nights a week and work
a couple hours or until bastion_killer shuts down the bastion host your EC2 bill will be about $0.23/month. (Disclaimer: Fees vary, this is just an example, don't take my word for it,
you should always set billing alerts on your AWS account, and don't send me your AWS bill if you screw this up).

Also I'm certainly too cheap to pay $30/month for a NAT instance to pipe access from my bastion host my database on a private subnet
so I set up VPC endpoints which are a fraction of the cost of a NAT instance. [VPC Endpoints](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/vpc-interface-endpoints.html)

Hope this is helped you out.

### How to deploy bastion host

1. Install cdk cli https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html
2. Configure your AWS credentials on your local shell
3. Set a parameter in System Manager named "VpcId". 
   This is used during deployment determine what VPC the bastion host is deployed to.`vpc_id: str = ssm.get_parameter(Name="VpcId")['Parameter']['Value']`
4. Run the command "cdk deploy"

### Upload a public key to bastion host
1. Create your private/public ssh key pair.
2. Log into the bastion server and put your public key in the authorized keys file.
   ```
   $ ./start_session.sh
   Starting session with SessionId: 
   sh-4.2$ cd ~/
   sh-4.2$ mkdir .ssh
   sh-4.2$ chmod 700 .ssh
   sh-4.2$ touch .ssh/authorized_keys
   sh-4.2$ chmod 600 .ssh/authorized_keys
   sh-4.2$ vi .ssh/authorized_keys
   ```
   Paste your public key (perhaps from .ssh/id_rsa.pub) and save authorized_keys file.

### How to create a tunnel to a database
1. Make sure the database allows access from the bastion security group created by the CDK deployment.
2. Edit .ssh/config. This will start an ssm session anytime you run a command like `ssh i-XXXXXXX`
```
Host i-* mi-*
  ProxyCommand sh -c "aws ssm start-session --target %h --document-name AWS-StartSSHSession --parameters 'portNumber=%p'"
```
3. Set an environment variable called DB_HOST
```
export DB_HOST=my-database-name.cluster-cw3bjgnjhzxa.us-east-2.rds.amazonaws.com
```
4. Run `./start_tunnel.sh` Note this will both start a tunnel and login to the bastion server.

5. Connect to your database on `localhost`
```
psql -h localhost -d my_database_name -U admin_user -W
```

### How to deploy bastion_killer
1. Install the AWS CLI
2. Configure your AWS credentials AWS_DEFAULT_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY...
3. run bastion_killer_deploy.sh `./bastion_killer_deploy.sh`