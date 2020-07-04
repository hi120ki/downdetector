#!/usr/bin/env python3

from aws_cdk import core

from downdetector.downdetector_stack import DowndetectorStack


app = core.App()
DowndetectorStack(app, "downdetector", env={'region': 'ap-northeast-1'})

app.synth()
