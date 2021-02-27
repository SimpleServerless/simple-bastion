aws cloudformation deploy --template-file bastion_killer.yaml \
--stack-name "bastion-killer" \
--parameter-override StopScheduled="cron(0 6 * * ? *)" \
--capabilities CAPABILITY_IAM