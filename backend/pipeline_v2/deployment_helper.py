import logging
from typing import Any

from api_v2.api_key_validator import BaseAPIKeyValidator
from api_v2.exceptions import InvalidAPIRequest
from api_v2.key_helper import KeyHelper
from rest_framework.request import Request
from utils.user_context import UserContext

from pipeline_v2.exceptions import PipelineNotFound
from pipeline_v2.pipeline_processor import PipelineProcessor

logger = logging.getLogger(__name__)


class DeploymentHelper(BaseAPIKeyValidator):
    @staticmethod
    def validate_parameters(request: Request, **kwargs: Any) -> None:
        """Validate pipeline_id for pipeline deployments."""
        pipeline_id = kwargs.get("pipeline_id") or request.data.get("pipeline_id")
        org_name = kwargs.get("org_name") or request.data.get("org_name")
        if not pipeline_id:
            raise InvalidAPIRequest("Missing params pipeline_id")
        if not org_name:
            raise InvalidAPIRequest("Missing params org_name")
        UserContext.set_organization_identifier(org_name)

    @staticmethod
    def validate_and_process(
        self: Any, request: Request, func: Any, api_key: str, *args: Any, **kwargs: Any
    ) -> Any:
        """Fetch pipeline and validate API key."""
        pipeline_id = kwargs.get("pipeline_id") or request.data.get("pipeline_id")
        pipeline = PipelineProcessor.get_active_pipeline(pipeline_id=pipeline_id)
        if not pipeline:
            raise PipelineNotFound()
        KeyHelper.validate_api_key(api_key=api_key, instance=pipeline)
        kwargs["pipeline"] = pipeline
        return func(self, request, *args, **kwargs)
