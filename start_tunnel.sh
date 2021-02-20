export BASTION_INSTANCE_ID=$(aws ec2 describe-instances --filter "Name=tag:Name,Values=simple-bastion" \
--query "Reservations[].Instances[?State.Name == 'running'].InstanceId[]" --output text)
echo "Instance ID: $BASTION_INSTANCE_ID"

if test -z "$DB_HOST"; then echo "****** DB_HOST not set. Set DB_HOST with: export DB_HOST=my-db.host.url.com"; exit 1; fi
if test -z "$BASTION_INSTANCE_ID"; then echo "****** DB_HOST not set. Make sure the AWS region and credentials are set"; exit 1; fi

ssh ssm-user@$BASTION_INSTANCE_ID -L 5432:$DB_HOST:5432