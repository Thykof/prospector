# -*- coding: utf-8 -*-
import json
from datetime import datetime

from jinja2 import Template
from prospector.formatters.base import Formatter

__all__ = (
    'HTMLFormatter',
)


class HTMLFormatter(Formatter):
    """Usage: prospector -o html > prospector_report.html"""
    def render(self, summary=True, messages=True, profile=False):
        output = {}

        if summary:
            # we need to slightly change the types and format
            # of a few of the items in the summary to make
            # them play nice with JSON formatting
            munged = {}
            for key, value in self.summary.items():
                if isinstance(value, datetime):
                    munged[key] = str(value)
                else:
                    munged[key] = value
            output['summary'] = munged

        if profile:
            output['profile'] = json.dumps(self.profile.as_dict(), indent=2).replace('\n', '<br>')

        if messages:
            output['messages'] = [m.as_dict() for m in self.messages]

        with open('prospector/formatters/templates/html.html') as f:
            template = Template(f.read())
        return template.render(output=output)
