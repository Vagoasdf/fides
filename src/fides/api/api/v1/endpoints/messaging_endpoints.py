from typing import Dict, List, Optional

from fastapi import Depends, Security
from fastapi_pagination import Page, Params
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.sqlalchemy import paginate
from fideslang.validation import FidesKey
from loguru import logger
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from fides.api.api import deps
from fides.api.common_exceptions import (
    MessageDispatchException,
    MessagingConfigNotFoundException,
    EmailTemplateNotFoundException,
    MessagingTemplateValidationException,
)
from fides.api.models.messaging import (
    MessagingConfig,
    default_messaging_config_key,
    default_messaging_config_name,
    get_schema_for_secrets,
)
from fides.api.models.messaging_template import (
    DEFAULT_MESSAGING_TEMPLATES,
    MessagingTemplate,
)
from fides.api.oauth.utils import verify_oauth_client
from fides.api.schemas.api import BulkUpdateFailed
from fides.api.schemas.messaging.messaging import (
    BulkPutBasicMessagingTemplateResponse,
    MessagingActionType,
    MessagingConfigRequest,
    MessagingConfigRequestBase,
    MessagingConfigResponse,
    MessagingConfigStatus,
    MessagingConfigStatusMessage,
    MessagingServiceType,
    BasicMessagingTemplateRequest,
    BasicMessagingTemplateResponse,
    TestMessagingStatusMessage,
    MessagingTemplateWithPropertiesSummary,
    MessagingTemplateWithPropertiesDetail,
    MessagingTemplateWithPropertiesBodyParams,
    MessagingTemplateDefault,
    MessagingTemplateWithPropertiesPatchBodyParams,
)
from fides.api.schemas.messaging.messaging_secrets_docs_only import (
    possible_messaging_secrets,
)
from fides.api.schemas.redis_cache import Identity
from fides.api.service.messaging.message_dispatch_service import dispatch_message
from fides.api.service.messaging.messaging_crud_service import (
    create_or_update_messaging_config,
    delete_messaging_config,
    get_all_basic_messaging_templates,
    get_messaging_config_by_key,
    update_messaging_config,
    create_or_update_basic_templates,
    get_default_template_by_type,
    create_property_specific_template_by_type,
    get_template_by_id,
    update_property_specific_template,
    delete_template_by_id,
    save_defaults_for_all_messaging_template_types,
    patch_property_specific_template,
)
from fides.api.util.api_router import APIRouter
from fides.api.util.logger import Pii
from fides.common.api.scope_registry import (
    MESSAGING_CREATE_OR_UPDATE,
    MESSAGING_DELETE,
    MESSAGING_READ,
    MESSAGING_TEMPLATE_UPDATE,
)
from fides.common.api.v1.urn_registry import (
    MESSAGING_ACTIVE_DEFAULT,
    MESSAGING_BY_KEY,
    MESSAGING_CONFIG,
    MESSAGING_DEFAULT,
    MESSAGING_DEFAULT_BY_TYPE,
    MESSAGING_DEFAULT_SECRETS,
    MESSAGING_SECRETS,
    MESSAGING_STATUS,
    BASIC_MESSAGING_TEMPLATES,
    MESSAGING_TEST,
    V1_URL_PREFIX,
    MESSAGING_TEMPLATES_SUMMARY,
    MESSAGING_TEMPLATES_BY_TEMPLATE_TYPE,
    MESSAGING_TEMPLATE_DEFAULT_BY_TEMPLATE_TYPE,
    MESSAGING_TEMPLATE_BY_ID,
)
from fides.config.config_proxy import ConfigProxy

router = APIRouter(tags=["Messaging"], prefix=V1_URL_PREFIX)


@router.post(
    MESSAGING_CONFIG,
    status_code=HTTP_200_OK,
    dependencies=[Security(verify_oauth_client, scopes=[MESSAGING_CREATE_OR_UPDATE])],
    response_model=MessagingConfigResponse,
)
def post_config(
    *,
    db: Session = Depends(deps.get_db),
    messaging_config: MessagingConfigRequest,
) -> MessagingConfigResponse:
    """
    Given a messaging config, create corresponding MessagingConfig object, provided no config already exists
    """

    try:
        return create_or_update_messaging_config(db=db, config=messaging_config)
    except ValueError as e:
        logger.warning(
            "Create failed for messaging config {}: {}",
            messaging_config.key,
            Pii(str(e)),
        )
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Config with key {messaging_config.key} failed to be added: {e}",
        )
    except Exception as exc:
        logger.warning(
            "Create failed for messaging config {}: {}",
            messaging_config.key,
            Pii(str(exc)),
        )
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Config with key {messaging_config.key} failed to be added: {exc}",
        )


@router.patch(
    MESSAGING_BY_KEY,
    dependencies=[Security(verify_oauth_client, scopes=[MESSAGING_CREATE_OR_UPDATE])],
    response_model=MessagingConfigResponse,
)
def patch_config_by_key(
    config_key: FidesKey,
    *,
    db: Session = Depends(deps.get_db),
    messaging_config: MessagingConfigRequest,
) -> Optional[MessagingConfigResponse]:
    """
    Updates config for messaging by key, provided config with key can be found.
    """
    try:
        return update_messaging_config(db=db, key=config_key, config=messaging_config)
    except MessagingConfigNotFoundException:
        logger.warning("No messaging config found with key {}", config_key)
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No messaging config found with key {config_key}",
        )
    except Exception as exc:
        logger.warning(
            "Patch failed for messaging config {}: {}",
            messaging_config.key,
            Pii(str(exc)),
        )
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Config with key {messaging_config.key} failed to be added",
        )


# this needs to come before other `/default/{messaging_type}` routes so that `/status`
# isn't picked up as a path param
@router.get(
    MESSAGING_ACTIVE_DEFAULT,
    dependencies=[Security(verify_oauth_client, scopes=[MESSAGING_READ])],
    response_model=MessagingConfigResponse,
)
def get_active_default_config(*, db: Session = Depends(deps.get_db)) -> MessagingConfig:
    """
    Retrieves the active default messaging config.
    """
    logger.info("Finding active default messaging config")
    try:
        messaging_config = MessagingConfig.get_active_default(db)
    except ValueError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Invalid notification_service_type configured.",
        )
    if not messaging_config:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No active default messaging config found.",
        )
    return messaging_config


# this needs to come before other `/default/{messaging_type}` routes so that `/status`
# isn't picked up as a path param
@router.get(
    MESSAGING_STATUS,
    dependencies=[Security(verify_oauth_client, scopes=[MESSAGING_READ])],
    response_model=MessagingConfigStatusMessage,
    responses={
        HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": {
                        "config_status": "configured",
                        "detail": "Active default messaging service of type mailgun is fully configured",
                    }
                }
            }
        }
    },
)
def get_messaging_status(
    *, db: Session = Depends(deps.get_db)
) -> MessagingConfigStatusMessage:
    """
    Determines the status of the active default messaging config
    """
    logger.info("Determining active default messaging config status")

    # confirm an active default messaging config is present
    messaging_config = MessagingConfig.get_active_default(db)
    if not messaging_config:
        return MessagingConfigStatusMessage(
            config_status=MessagingConfigStatus.not_configured,
            detail="No active default messaging configuration found",
        )

    try:
        details = messaging_config.details
        MessagingConfigRequestBase.validate_details_schema(
            messaging_config.service_type, details
        )
    except Exception as e:
        logger.error(f"Invalid or unpopulated details on {messaging_config.service_type.value} messaging configuration: {Pii(str(e))}")  # type: ignore
        return MessagingConfigStatusMessage(
            config_status=MessagingConfigStatus.not_configured,
            detail=f"Invalid or unpopulated details on {messaging_config.service_type.value} messaging configuration",  # type: ignore
        )

    # confirm secrets are present and pass validation
    secrets = messaging_config.secrets
    if not secrets:
        return MessagingConfigStatusMessage(
            config_status=MessagingConfigStatus.not_configured,
            detail=f"No secrets found for {messaging_config.service_type.value} messaging configuration",  # type: ignore
        )
    try:
        get_schema_for_secrets(
            service_type=messaging_config.service_type,  # type: ignore
            secrets=secrets,
        )
    except (ValueError, KeyError) as e:
        logger.error(f"Invalid secrets found on {messaging_config.service_type.value} messaging configuration: {Pii(str(e))}")  # type: ignore
        return MessagingConfigStatusMessage(
            config_status=MessagingConfigStatus.not_configured,
            detail=f"Invalid secrets found on {messaging_config.service_type.value} messaging configuration",  # type: ignore
        )

    return MessagingConfigStatusMessage(
        config_status=MessagingConfigStatus.configured,
        detail=f"Active default messaging service of type {messaging_config.service_type.value} is fully configured",  # type: ignore
    )


@router.put(
    MESSAGING_DEFAULT,
    dependencies=[Security(verify_oauth_client, scopes=[MESSAGING_CREATE_OR_UPDATE])],
    response_model=MessagingConfigResponse,
)
def put_default_config(
    *,
    db: Session = Depends(deps.get_db),
    messaging_config: MessagingConfigRequestBase,
) -> Optional[MessagingConfigResponse]:
    """
    Updates default messaging config for given service type.
    """
    logger.info(
        "Starting upsert for default messaging config of type '{}'",
        messaging_config.service_type,
    )
    incoming_data = messaging_config.dict()
    existing_default = MessagingConfig.get_by_type(db, messaging_config.service_type)
    if existing_default:
        # take the key of the existing default and add that to the incoming data, to ensure we overwrite the same record
        incoming_data["key"] = existing_default.key
        incoming_data["name"] = existing_default.name
    else:
        # set a key and name for our config if we're creating a new default
        incoming_data["name"] = default_messaging_config_name(
            messaging_config.service_type.value
        )
        incoming_data["key"] = default_messaging_config_key(
            messaging_config.service_type.value
        )
    return create_or_update_messaging_config(
        db, MessagingConfigRequest(**incoming_data)
    )


@router.put(
    MESSAGING_DEFAULT_SECRETS,
    status_code=HTTP_200_OK,
    dependencies=[Security(verify_oauth_client, scopes=[MESSAGING_CREATE_OR_UPDATE])],
    response_model=TestMessagingStatusMessage,
)
def put_default_config_secrets(
    service_type: MessagingServiceType,
    *,
    db: Session = Depends(deps.get_db),
    unvalidated_messaging_secrets: possible_messaging_secrets,
) -> TestMessagingStatusMessage:
    messaging_config = MessagingConfig.get_by_type(db, service_type=service_type)
    if not messaging_config:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No default messaging config found of type '{service_type}'",
        )
    return update_config_secrets(db, messaging_config, unvalidated_messaging_secrets)


@router.put(
    MESSAGING_SECRETS,
    status_code=HTTP_200_OK,
    dependencies=[Security(verify_oauth_client, scopes=[MESSAGING_CREATE_OR_UPDATE])],
    response_model=TestMessagingStatusMessage,
)
def put_config_secrets(
    config_key: FidesKey,
    *,
    db: Session = Depends(deps.get_db),
    unvalidated_messaging_secrets: possible_messaging_secrets,
) -> TestMessagingStatusMessage:
    """
    Add or update secrets for messaging config.
    """
    logger.info("Finding messaging config with key '{}'", config_key)
    messaging_config = MessagingConfig.get_by(db=db, field="key", value=config_key)
    if not messaging_config:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No messaging configuration with key {config_key}.",
        )
    return update_config_secrets(db, messaging_config, unvalidated_messaging_secrets)


def update_config_secrets(
    db: Session,
    messaging_config: MessagingConfig,
    unvalidated_messaging_secrets: possible_messaging_secrets,
) -> TestMessagingStatusMessage:
    try:
        secrets_schema = get_schema_for_secrets(
            service_type=messaging_config.service_type,  # type: ignore
            secrets=unvalidated_messaging_secrets,
        )
    except KeyError as exc:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.args[0],
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=exc.args[0],
        )

    logger.info(
        "Updating messaging config secrets for config with key '{}'",
        messaging_config.key,
    )
    try:
        messaging_config.set_secrets(db=db, messaging_secrets=secrets_schema.dict())  # type: ignore
    except ValueError as exc:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=exc.args[0],
        )
    msg = f"Secrets updated for MessagingConfig with key: {messaging_config.key}."
    # todo- implement test status for messaging service
    return TestMessagingStatusMessage(msg=msg, test_status=None)


@router.get(
    MESSAGING_CONFIG,
    dependencies=[Security(verify_oauth_client, scopes=[MESSAGING_READ])],
    response_model=Page[MessagingConfigResponse],
)
def get_configs(
    *, db: Session = Depends(deps.get_db), params: Params = Depends()
) -> AbstractPage[MessagingConfig]:
    """
    Retrieves configs for messaging.
    """
    logger.info(
        "Finding all messaging configurations with pagination params {}", params
    )
    return paginate(
        MessagingConfig.query(db=db).order_by(MessagingConfig.created_at.desc()),
        params=params,
    )


@router.get(
    MESSAGING_BY_KEY,
    dependencies=[Security(verify_oauth_client, scopes=[MESSAGING_READ])],
    response_model=MessagingConfigResponse,
)
def get_config_by_key(
    config_key: FidesKey, *, db: Session = Depends(deps.get_db)
) -> MessagingConfigResponse:
    """
    Retrieves configs for messaging service by key.
    """
    logger.info("Finding messaging config with key '{}'", config_key)

    try:
        return get_messaging_config_by_key(db=db, key=config_key)
    except MessagingConfigNotFoundException as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.get(
    MESSAGING_DEFAULT_BY_TYPE,
    dependencies=[Security(verify_oauth_client, scopes=[MESSAGING_READ])],
    response_model=MessagingConfigResponse,
)
def get_default_config_by_type(
    service_type: MessagingServiceType, *, db: Session = Depends(deps.get_db)
) -> MessagingConfig:
    """
    Retrieves default config for messaging service by type.
    """
    logger.info("Finding default messaging config of type '{}'", service_type)

    messaging_config = MessagingConfig.get_by_type(db, service_type)
    if not messaging_config:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No default messaging config found of type '{service_type}'",
        )
    return messaging_config


@router.delete(
    MESSAGING_BY_KEY,
    status_code=HTTP_204_NO_CONTENT,
    dependencies=[Security(verify_oauth_client, scopes=[MESSAGING_DELETE])],
)
def delete_config_by_key(
    config_key: FidesKey, *, db: Session = Depends(deps.get_db)
) -> None:
    """
    Deletes messaging configs by key.
    """
    try:
        delete_messaging_config(db=db, key=config_key)
    except MessagingConfigNotFoundException as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.post(
    MESSAGING_TEST,
    status_code=HTTP_200_OK,
    dependencies=[Security(verify_oauth_client, scopes=[MESSAGING_CREATE_OR_UPDATE])],
    response_model=Dict[str, str],
    responses={
        HTTP_200_OK: {
            "content": {
                "application/json": {
                    "example": {
                        "details": "Test message successfully sent",
                    }
                }
            }
        }
    },
)
def send_test_message(
    message_info: Identity,
    db: Session = Depends(deps.get_db),
    config_proxy: ConfigProxy = Depends(deps.get_config_proxy),
) -> Dict[str, str]:
    """Sends a test message."""
    try:
        dispatch_message(
            db,
            action_type=MessagingActionType.TEST_MESSAGE,
            to_identity=message_info,
            service_type=config_proxy.notifications.notification_service_type,
        )
    except MessageDispatchException as e:
        raise HTTPException(
            status_code=400, detail=f"There was an error sending the test message: {e}"
        )
    return {"details": "Test message successfully sent"}


@router.get(
    BASIC_MESSAGING_TEMPLATES,
    dependencies=[Security(verify_oauth_client, scopes=[MESSAGING_TEMPLATE_UPDATE])],
    response_model=List[BasicMessagingTemplateResponse],
)
def get_basic_messaging_templates(
    *, db: Session = Depends(deps.get_db)
) -> List[BasicMessagingTemplateResponse]:
    """Returns the available messaging templates, augments the models with labels to be used in the UI."""
    return [
        BasicMessagingTemplateResponse(
            type=template.type,
            content=template.content,
            label=DEFAULT_MESSAGING_TEMPLATES.get(template.type, {}).get("label", None),
        )
        for template in get_all_basic_messaging_templates(db=db)
    ]


@router.put(
    BASIC_MESSAGING_TEMPLATES,
    dependencies=[Security(verify_oauth_client, scopes=[MESSAGING_TEMPLATE_UPDATE])],
)
def update_basic_messaging_templates(
    templates: List[BasicMessagingTemplateRequest],
    *,
    db: Session = Depends(deps.get_db),
) -> BulkPutBasicMessagingTemplateResponse:
    """Updates the messaging templates and reverts empty subject or body values to the default values."""

    succeeded = []
    failed = []

    for template in templates:
        template_type = template.type
        content = template.content

        try:
            default_template = DEFAULT_MESSAGING_TEMPLATES.get(template_type)
            if not default_template:
                raise ValueError("Invalid template type.")

            content["subject"] = content["subject"] or default_template["content"]["subject"]
            content["body"] = content["body"] or default_template["content"]["body"]

            # For Basic Messaging Templates, we ignore the is_enabled flag at runtime. This is because
            # enabling/disabling by template is only supported for property-specific messaging templates,
            # not basic templates.
            create_or_update_basic_templates(
                db,
                data={"type": template_type, "content": content, "is_enabled": False},
            )

            succeeded.append(
                BasicMessagingTemplateResponse(
                    type=template_type,
                    content=content,
                    label=default_template.get("label"),
                )
            )

        except ValueError as e:
            failed.append(BulkUpdateFailed(message=str(e), data=template))
        except Exception:
            failed.append(
                BulkUpdateFailed(
                    message="Unexpected error updating template.", data=template
                )
            )

    return BulkPutBasicMessagingTemplateResponse(succeeded=succeeded, failed=failed)


@router.get(
    MESSAGING_TEMPLATES_SUMMARY,
    dependencies=[Security(verify_oauth_client, scopes=[MESSAGING_TEMPLATE_UPDATE])],
    response_model=Page[MessagingTemplateWithPropertiesSummary],
)
def get_property_specific_messaging_templates_summary(
    *, db: Session = Depends(deps.get_db), params: Params = Depends()
) -> AbstractPage[MessagingTemplate]:
    """
    Returns all messaging templates, automatically saving any missing message template types to the db.
    """
    # First save any missing template types to db
    save_defaults_for_all_messaging_template_types(db)
    ordered_templates = MessagingTemplate.query(db=db).order_by(
        MessagingTemplate.created_at.desc()
    )
    # Now return all templates
    return paginate(
        ordered_templates,
        params=params,
    )


@router.get(
    MESSAGING_TEMPLATE_DEFAULT_BY_TEMPLATE_TYPE,
    dependencies=[Security(verify_oauth_client, scopes=[MESSAGING_TEMPLATE_UPDATE])],
    response_model=MessagingTemplateDefault,
)
def get_default_messaging_template(
    template_type: MessagingActionType,
) -> MessagingTemplateDefault:
    """
    Retrieves default messaging template by template type.
    """
    logger.info(
        "Finding default messaging template of template type '{}'", template_type
    )
    try:
        return get_default_template_by_type(template_type)
    except MessagingTemplateValidationException as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=e.message,
        )


@router.post(
    MESSAGING_TEMPLATES_BY_TEMPLATE_TYPE,
    dependencies=[Security(verify_oauth_client, scopes=[MESSAGING_TEMPLATE_UPDATE])],
    response_model=Optional[MessagingTemplateWithPropertiesDetail],
)
def create_property_specific_messaging_template(
    template_type: MessagingActionType,
    *,
    db: Session = Depends(deps.get_db),
    messaging_template_create_body: MessagingTemplateWithPropertiesBodyParams,
) -> Optional[MessagingTemplate]:
    """
    Creates property-specific messaging template by template type.
    """
    logger.info(
        "Creating new property-specific messaging template of type '{}'", template_type
    )
    try:
        return create_property_specific_template_by_type(
            db, template_type, messaging_template_create_body
        )
    except MessagingTemplateValidationException as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=e.message,
        )


@router.put(
    MESSAGING_TEMPLATE_BY_ID,
    dependencies=[Security(verify_oauth_client, scopes=[MESSAGING_TEMPLATE_UPDATE])],
    response_model=Optional[MessagingTemplateWithPropertiesDetail],
)
def update_property_specific_messaging_template(
    template_id: str,
    *,
    db: Session = Depends(deps.get_db),
    messaging_template_update_body: MessagingTemplateWithPropertiesBodyParams,
) -> Optional[MessagingTemplate]:
    """
    Updates property-specific messaging template by template id.
    """
    logger.info("Updating property-specific messaging template of id '{}'", template_id)
    try:
        return update_property_specific_template(
            db, template_id, messaging_template_update_body
        )
    except EmailTemplateNotFoundException as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except MessagingTemplateValidationException as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=e.message,
        )


@router.patch(
    MESSAGING_TEMPLATE_BY_ID,
    dependencies=[Security(verify_oauth_client, scopes=[MESSAGING_TEMPLATE_UPDATE])],
    response_model=Optional[MessagingTemplateWithPropertiesDetail],
)
def patch_property_specific_messaging_template(
    template_id: str,
    *,
    db: Session = Depends(deps.get_db),
    messaging_template_update_body: MessagingTemplateWithPropertiesPatchBodyParams,
) -> Optional[MessagingTemplate]:
    """
    Updates property-specific messaging template by template id.
    """
    logger.info("Patching property-specific messaging template of id '{}'", template_id)
    try:
        data = messaging_template_update_body.dict(exclude_none=True)
        return patch_property_specific_template(db, template_id, data)
    except EmailTemplateNotFoundException as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except MessagingTemplateValidationException as e:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=e.message,
        )


@router.get(
    MESSAGING_TEMPLATE_BY_ID,
    dependencies=[Security(verify_oauth_client, scopes=[MESSAGING_TEMPLATE_UPDATE])],
    response_model=MessagingTemplateWithPropertiesDetail,
)
def get_messaging_template_by_id(
    template_id: str,
    *,
    db: Session = Depends(deps.get_db),
) -> MessagingTemplateWithPropertiesDetail:
    """
    Retrieves messaging template by template tid.
    """
    logger.info("Finding messaging template with id '{}'", template_id)

    try:
        messaging_template = get_template_by_id(db, template_id)
        return MessagingTemplateWithPropertiesDetail(
            id=template_id,
            type=messaging_template.type,
            content=messaging_template.content,
            is_enabled=messaging_template.is_enabled,
            properties=messaging_template.properties,
        )
    except EmailTemplateNotFoundException as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=e.message,
        )


@router.delete(
    MESSAGING_TEMPLATE_BY_ID,
    dependencies=[Security(verify_oauth_client, scopes=[MESSAGING_TEMPLATE_UPDATE])],
    status_code=HTTP_204_NO_CONTENT,
    response_model=None,
)
def delete_messaging_template_by_id(
    template_id: str,
    *,
    db: Session = Depends(deps.get_db),
) -> None:
    """
    Deletes messaging template by template id.
    """
    logger.info("Deleting messaging template with id '{}'", template_id)
    try:
        delete_template_by_id(db, template_id)
    except EmailTemplateNotFoundException as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except MessagingTemplateValidationException as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=e.message)
