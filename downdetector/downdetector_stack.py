from aws_cdk import (
    aws_events as events,
    aws_lambda as lambda_,
    aws_events_targets as targets,
    core,
)

class DowndetectorStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lambdaFn = lambda_.Function(
            self, "Singleton",
            code=lambda_.AssetCode(path="./lambda"),
            handler="handler.main",
            timeout=core.Duration.seconds(300),
            runtime=lambda_.Runtime.PYTHON_3_7,
            environment={"PYTHONPATH": "/var/task/packages:/var/runtime"},
        )

        # Run every 1 hour
        # See https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
        rule = events.Rule(
            self, "Rule",
            schedule=events.Schedule.cron(
                minute='0',
                hour='0/1',
                month='*',
                week_day='*',
                year='*'),
        )
        rule.add_target(targets.LambdaFunction(lambdaFn))
