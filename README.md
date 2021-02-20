# Simple Bastion

### This project uses CDK to deploy a t3a.nano ($3.50/month) bastion host for the purpose of tunneling to an RDS instance on a public subnet.

### How to deploy bastion host

1. Install cdk cli https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html
2. Configure your AWS credentials on your local shell
3. Set a parameter in System Manager named "VpcId". This is used during deployment determine what VPC the bastion host is deployed to.

```vpc_id: str = ssm.get_parameter(Name="VpcId")['Parameter']['Value']``` 
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