export BASTION_INSTANCE_ID=$(aws ec2 describe-instances --filter "Name=tag:Name,Values=simple-bastion" \
--query "Reservations[].Instances[?State.Name == 'running'].InstanceId[]" --output text)
echo "Instance ID: $BASTION_INSTANCE_ID"

# Shell into bastion
aws ssm start-session --target $BASTION_INSTANCE_ID
