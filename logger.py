import json
import sys


class CloudRunLogger(object):

    def __init__(self, project_id: str, local_run=False):
        self.project_id = project_id
        self.request = None
        self.trace_id = None
        self.local_run = local_run

    def update_trace_id(self, trace_id):
        self.trace_id = trace_id

    def update_request_header(self, api_request):
        self.request = api_request

    def _do_log(self, severity, message, **kwargs):
        # check if local run = true if yes just print the message
        if self.local_run:
            print(message)
        else:
            # Build structured log messages as an object.
            global_log_fields = {}
            # Add log correlation to nest all log messages
            # beneath request log in Log Viewer.
            trace_field = self._get_trace()
            if trace_field:
                global_log_fields['logging.googleapis.com/trace'] = trace_field

            mms_attributes = {}
            if kwargs:
                mms_attributes = {'media_saturn': kwargs}

            # Complete a structured log entry.
            entry = dict(
                severity=severity,
                message=message,
                trace_id=self.trace_id,
                **mms_attributes,
                **global_log_fields
            )

            print(json.dumps(entry))
            sys.stdout.flush()

    def _get_trace(self):
        if not self.request:
            return None

        trace_header = self.request.headers.get('X-Cloud-Trace-Context')
        if trace_header and self.project_id:
            trace = trace_header.split('/')
            return f"projects/{self.project_id}/traces/{trace[0]}"

    def info(self, message, **kwargs):
        self._do_log('INFO', message='MMS-INFO: {}'.format(message), **kwargs)

    def warning(self, message, **kwargs):
        self._do_log('WARNING', message='MMS-WARNING: {}'.format(message), **kwargs)

    def error(self, message, **kwargs):
        self._do_log('ERROR', message='MMS-ERROR: {}'.format(message), **kwargs)

    def debug(self, message, **kwargs):
        self._do_log('DEBUG', message='MMS-DEBUG: {}'.format(message), **kwargs)