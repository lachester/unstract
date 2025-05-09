from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from pipeline_v2.piepline_api_execution_views import PipelineApiExecution

execute = PipelineApiExecution.as_view()

urlpatterns = format_suffix_patterns(
    [
        re_path(
            r"^api/(?P<org_name>[\w-]+)/(?P<pipeline_id>[\w-]+)/?$",
            execute,
            name="pipeline_api_deployment_execution",
        ),
    ]
)
