import json
import pytest

from aws_cdk import core
from downdetector.downdetector_stack import DowndetectorStack


def get_template():
    app = core.App()
    DowndetectorStack(app, "downdetector")
    return json.dumps(app.synth().get_stack("downdetector").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
