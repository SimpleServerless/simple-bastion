export BASTION_INSTANCE_ID=$(aws ec2 describe-instances --filter "Name=tag:Name,Values=simple-bastion" \
--query "Reservations[].Instances[?State.Name == 'stopped'].InstanceId[]" --output text)
echo "Instance ID: $BASTION_INSTANCE_ID"

aws ec2 start-instances --instance-ids $BASTION_INSTANCE_ID