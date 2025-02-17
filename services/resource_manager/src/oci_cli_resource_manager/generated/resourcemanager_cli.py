# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.

from __future__ import print_function
import click
import oci  # noqa: F401
import six  # noqa: F401
import sys  # noqa: F401
from oci_cli.cli_root import cli
from oci_cli import cli_constants  # noqa: F401
from oci_cli import cli_util
from oci_cli import json_skeleton_utils
from oci_cli import custom_types  # noqa: F401
from oci_cli.aliasing import CommandGroupWithAlias


@cli.command(cli_util.override('resource_manager.resource_manager_root_group.command_name', 'resource-manager'), cls=CommandGroupWithAlias, help=cli_util.override('resource_manager.resource_manager_root_group.help', """API for the Resource Manager service. Use this API to install, configure, and manage resources via the "infrastructure-as-code" model. For more information, see [Overview of Resource Manager](/iaas/Content/ResourceManager/Concepts/resourcemanager.htm)."""), short_help=cli_util.override('resource_manager.resource_manager_root_group.short_help', """Resource Manager API"""))
@cli_util.help_option_group
def resource_manager_root_group():
    pass


@click.command(cli_util.override('resource_manager.stack_group.command_name', 'stack'), cls=CommandGroupWithAlias, help="""The stack object. Stacks represent definitions of groups of Oracle Cloud Infrastructure resources that you can act upon as a group. You take action on stacks by using jobs.""")
@cli_util.help_option_group
def stack_group():
    pass


@click.command(cli_util.override('resource_manager.work_request_group.command_name', 'work-request'), cls=CommandGroupWithAlias, help="""The status of a work request.""")
@cli_util.help_option_group
def work_request_group():
    pass


@click.command(cli_util.override('resource_manager.job_group.command_name', 'job'), cls=CommandGroupWithAlias, help="""Jobs perform the actions that are defined in your configuration. There are three job types - **Plan job**. A plan job takes your Terraform configuration, parses it, and creates an execution plan. - **Apply job**. The apply job takes your execution plan, applies it to the associated stack, then executes the configuration's instructions. - **Destroy job**. To clean up the infrastructure controlled by the stack, you run a destroy job. A destroy job does not delete the stack or associated job resources, but instead releases the resources managed by the stack. - **Import_TF_State job**. An import Terraform state job takes a Terraform state file and sets it as the current state of the stack. This is used to migrate local Terraform environments to Resource Manager.""")
@cli_util.help_option_group
def job_group():
    pass


resource_manager_root_group.add_command(stack_group)
resource_manager_root_group.add_command(work_request_group)
resource_manager_root_group.add_command(job_group)


@job_group.command(name=cli_util.override('resource_manager.cancel_job.command_name', 'cancel'), help=u"""Indicates the intention to cancel the specified job. Cancellation of the job is not immediate, and may be delayed, or may not happen at all.""")
@cli_util.option('--job-id', required=True, help=u"""The [OCID] of the job.""")
@cli_util.option('--if-match', help=u"""For optimistic concurrency control. In the `PUT` or `DELETE` call for a resource, set the `if-match` parameter to the value of the etag from a previous `GET` or `POST` response for that resource.  The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.""")
@cli_util.confirm_delete_option
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["ACCEPTED", "IN_PROGRESS", "FAILED", "SUCCEEDED", "CANCELING", "CANCELED"]), multiple=True, help="""This operation creates, modifies or deletes a resource that has a defined lifecycle state. Specify this option to perform the action and then wait until the resource reaches a given lifecycle state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the resource to reach the lifecycle state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the resource to see if it has reached the lifecycle state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def cancel_job(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, job_id, if_match):

    if isinstance(job_id, six.string_types) and len(job_id.strip()) == 0:
        raise click.UsageError('Parameter --job-id cannot be whitespace or empty string')

    kwargs = {}
    if if_match is not None:
        kwargs['if_match'] = if_match
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('resource_manager', ctx)
    result = client.cancel_job(
        job_id=job_id,
        **kwargs
    )
    if wait_for_state:
        if hasattr(client, 'get_job') and callable(getattr(client, 'get_job')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the resource has entered state: {}'.format(wait_for_state), file=sys.stderr)
                oci.wait_until(client, client.get_job(job_id), 'lifecycle_state', wait_for_state, succeed_on_not_found=True, **wait_period_kwargs)
            except oci.exceptions.ServiceError as e:
                # We make an initial service call so we can pass the result to oci.wait_until(), however if we are waiting on the
                # outcome of a delete operation it is possible that the resource is already gone and so the initial service call
                # will result in an exception that reflects a HTTP 404. In this case, we can exit with success (rather than raising
                # the exception) since this would have been the behaviour in the waiter anyway (as for delete we provide the argument
                # succeed_on_not_found=True to the waiter).
                #
                # Any non-404 should still result in the exception being thrown.
                if e.status == 404:
                    pass
                else:
                    raise
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the resource entered the specified state. Please retrieve the resource to find its current state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for resource to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the resource to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)


@stack_group.command(name=cli_util.override('resource_manager.change_stack_compartment.command_name', 'change-compartment'), help=u"""Moves a Stack and it's associated Jobs into a different compartment.""")
@cli_util.option('--stack-id', required=True, help=u"""The [OCID] of the stack.""")
@cli_util.option('--compartment-id', required=True, help=u"""The [OCID] of the compartment into which the Stack should be moved.""")
@cli_util.option('--if-match', help=u"""For optimistic concurrency control. In the `PUT` or `DELETE` call for a resource, set the `if-match` parameter to the value of the etag from a previous `GET` or `POST` response for that resource.  The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.""")
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["ACCEPTED", "IN_PROGRESS", "FAILED", "SUCCEEDED"]), multiple=True, help="""This operation asynchronously creates, modifies or deletes a resource and uses a work request to track the progress of the operation. Specify this option to perform the action and then wait until the work request reaches a certain state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the work request to reach the state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the work request to see if it has reached the state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def change_stack_compartment(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, stack_id, compartment_id, if_match):

    if isinstance(stack_id, six.string_types) and len(stack_id.strip()) == 0:
        raise click.UsageError('Parameter --stack-id cannot be whitespace or empty string')

    kwargs = {}
    if if_match is not None:
        kwargs['if_match'] = if_match
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    details = {}
    details['compartmentId'] = compartment_id

    client = cli_util.build_client('resource_manager', ctx)
    result = client.change_stack_compartment(
        stack_id=stack_id,
        change_stack_compartment_details=details,
        **kwargs
    )
    if wait_for_state:
        if hasattr(client, 'get_work_request') and callable(getattr(client, 'get_work_request')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the work request has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_work_request(result.headers['opc-work-request-id']), 'status', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the work request entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for work request to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the work request to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)


@job_group.command(name=cli_util.override('resource_manager.create_job.command_name', 'create'), help=u"""Creates a job.""")
@cli_util.option('--stack-id', required=True, help=u"""The [OCID] of the stack that is associated with the current job.""")
@cli_util.option('--display-name', help=u"""Description of the job.""")
@cli_util.option('--operation', help=u"""Terraform-specific operation to execute.""")
@cli_util.option('--job-operation-details', type=custom_types.CLI_COMPLEX_TYPE, help=u"""""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--apply-job-plan-resolution', type=custom_types.CLI_COMPLEX_TYPE, help=u"""""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--freeform-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Free-form tags associated with this resource. Each tag is a key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags]. Example: `{\"Department\": \"Finance\"}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--defined-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags]. Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["ACCEPTED", "IN_PROGRESS", "FAILED", "SUCCEEDED", "CANCELING", "CANCELED"]), multiple=True, help="""This operation creates, modifies or deletes a resource that has a defined lifecycle state. Specify this option to perform the action and then wait until the resource reaches a given lifecycle state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the resource to reach the lifecycle state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the resource to see if it has reached the lifecycle state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({'job-operation-details': {'module': 'resource_manager', 'class': 'CreateJobOperationDetails'}, 'apply-job-plan-resolution': {'module': 'resource_manager', 'class': 'ApplyJobPlanResolution'}, 'freeform-tags': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'resource_manager', 'class': 'dict(str, dict(str, object))'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'job-operation-details': {'module': 'resource_manager', 'class': 'CreateJobOperationDetails'}, 'apply-job-plan-resolution': {'module': 'resource_manager', 'class': 'ApplyJobPlanResolution'}, 'freeform-tags': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'resource_manager', 'class': 'dict(str, dict(str, object))'}}, output_type={'module': 'resource_manager', 'class': 'Job'})
@cli_util.wrap_exceptions
def create_job(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, stack_id, display_name, operation, job_operation_details, apply_job_plan_resolution, freeform_tags, defined_tags):

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    details = {}
    details['stackId'] = stack_id

    if display_name is not None:
        details['displayName'] = display_name

    if operation is not None:
        details['operation'] = operation

    if job_operation_details is not None:
        details['jobOperationDetails'] = cli_util.parse_json_parameter("job_operation_details", job_operation_details)

    if apply_job_plan_resolution is not None:
        details['applyJobPlanResolution'] = cli_util.parse_json_parameter("apply_job_plan_resolution", apply_job_plan_resolution)

    if freeform_tags is not None:
        details['freeformTags'] = cli_util.parse_json_parameter("freeform_tags", freeform_tags)

    if defined_tags is not None:
        details['definedTags'] = cli_util.parse_json_parameter("defined_tags", defined_tags)

    client = cli_util.build_client('resource_manager', ctx)
    result = client.create_job(
        create_job_details=details,
        **kwargs
    )
    if wait_for_state:
        if hasattr(client, 'get_job') and callable(getattr(client, 'get_job')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the resource has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_job(result.data.id), 'lifecycle_state', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the resource entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for resource to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the resource to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)


@job_group.command(name=cli_util.override('resource_manager.create_job_create_import_tf_state_job_operation_details.command_name', 'create-job-create-import-tf-state-job-operation-details'), help=u"""Creates a job.""")
@cli_util.option('--stack-id', required=True, help=u"""The [OCID] of the stack that is associated with the current job.""")
@cli_util.option('--job-operation-details-tf-state-base64-encoded', required=True, help=u"""Base64-encoded state file""")
@cli_util.option('--display-name', help=u"""Description of the job.""")
@cli_util.option('--operation', help=u"""Terraform-specific operation to execute.""")
@cli_util.option('--apply-job-plan-resolution', type=custom_types.CLI_COMPLEX_TYPE, help=u"""""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--freeform-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Free-form tags associated with this resource. Each tag is a key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags]. Example: `{\"Department\": \"Finance\"}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--defined-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags]. Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["ACCEPTED", "IN_PROGRESS", "FAILED", "SUCCEEDED", "CANCELING", "CANCELED"]), multiple=True, help="""This operation creates, modifies or deletes a resource that has a defined lifecycle state. Specify this option to perform the action and then wait until the resource reaches a given lifecycle state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the resource to reach the lifecycle state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the resource to see if it has reached the lifecycle state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({'apply-job-plan-resolution': {'module': 'resource_manager', 'class': 'ApplyJobPlanResolution'}, 'freeform-tags': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'resource_manager', 'class': 'dict(str, dict(str, object))'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'apply-job-plan-resolution': {'module': 'resource_manager', 'class': 'ApplyJobPlanResolution'}, 'freeform-tags': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'resource_manager', 'class': 'dict(str, dict(str, object))'}}, output_type={'module': 'resource_manager', 'class': 'Job'})
@cli_util.wrap_exceptions
def create_job_create_import_tf_state_job_operation_details(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, stack_id, job_operation_details_tf_state_base64_encoded, display_name, operation, apply_job_plan_resolution, freeform_tags, defined_tags):

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    details = {}
    details['jobOperationDetails'] = {}
    details['stackId'] = stack_id
    details['jobOperationDetails']['tfStateBase64Encoded'] = job_operation_details_tf_state_base64_encoded

    if display_name is not None:
        details['displayName'] = display_name

    if operation is not None:
        details['operation'] = operation

    if apply_job_plan_resolution is not None:
        details['applyJobPlanResolution'] = cli_util.parse_json_parameter("apply_job_plan_resolution", apply_job_plan_resolution)

    if freeform_tags is not None:
        details['freeformTags'] = cli_util.parse_json_parameter("freeform_tags", freeform_tags)

    if defined_tags is not None:
        details['definedTags'] = cli_util.parse_json_parameter("defined_tags", defined_tags)

    details['jobOperationDetails']['operation'] = 'IMPORT_TF_STATE'

    client = cli_util.build_client('resource_manager', ctx)
    result = client.create_job(
        create_job_details=details,
        **kwargs
    )
    if wait_for_state:
        if hasattr(client, 'get_job') and callable(getattr(client, 'get_job')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the resource has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_job(result.data.id), 'lifecycle_state', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the resource entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for resource to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the resource to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)


@job_group.command(name=cli_util.override('resource_manager.create_job_create_apply_job_operation_details.command_name', 'create-job-create-apply-job-operation-details'), help=u"""Creates a job.""")
@cli_util.option('--stack-id', required=True, help=u"""The [OCID] of the stack that is associated with the current job.""")
@cli_util.option('--display-name', help=u"""Description of the job.""")
@cli_util.option('--operation', help=u"""Terraform-specific operation to execute.""")
@cli_util.option('--apply-job-plan-resolution', type=custom_types.CLI_COMPLEX_TYPE, help=u"""""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--freeform-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Free-form tags associated with this resource. Each tag is a key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags]. Example: `{\"Department\": \"Finance\"}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--defined-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags]. Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--job-operation-details-execution-plan-strategy', help=u"""Specifies the source of the execution plan to apply. Use `AUTO_APPROVED` to run the job without an execution plan.""")
@cli_util.option('--job-operation-details-execution-plan-job-id', help=u"""The [OCID] of a plan job, for use when specifying `FROM_PLAN_JOB_ID` as the `executionPlanStrategy`.""")
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["ACCEPTED", "IN_PROGRESS", "FAILED", "SUCCEEDED", "CANCELING", "CANCELED"]), multiple=True, help="""This operation creates, modifies or deletes a resource that has a defined lifecycle state. Specify this option to perform the action and then wait until the resource reaches a given lifecycle state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the resource to reach the lifecycle state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the resource to see if it has reached the lifecycle state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({'apply-job-plan-resolution': {'module': 'resource_manager', 'class': 'ApplyJobPlanResolution'}, 'freeform-tags': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'resource_manager', 'class': 'dict(str, dict(str, object))'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'apply-job-plan-resolution': {'module': 'resource_manager', 'class': 'ApplyJobPlanResolution'}, 'freeform-tags': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'resource_manager', 'class': 'dict(str, dict(str, object))'}}, output_type={'module': 'resource_manager', 'class': 'Job'})
@cli_util.wrap_exceptions
def create_job_create_apply_job_operation_details(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, stack_id, display_name, operation, apply_job_plan_resolution, freeform_tags, defined_tags, job_operation_details_execution_plan_strategy, job_operation_details_execution_plan_job_id):

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    details = {}
    details['jobOperationDetails'] = {}
    details['stackId'] = stack_id

    if display_name is not None:
        details['displayName'] = display_name

    if operation is not None:
        details['operation'] = operation

    if apply_job_plan_resolution is not None:
        details['applyJobPlanResolution'] = cli_util.parse_json_parameter("apply_job_plan_resolution", apply_job_plan_resolution)

    if freeform_tags is not None:
        details['freeformTags'] = cli_util.parse_json_parameter("freeform_tags", freeform_tags)

    if defined_tags is not None:
        details['definedTags'] = cli_util.parse_json_parameter("defined_tags", defined_tags)

    if job_operation_details_execution_plan_strategy is not None:
        details['jobOperationDetails']['executionPlanStrategy'] = job_operation_details_execution_plan_strategy

    if job_operation_details_execution_plan_job_id is not None:
        details['jobOperationDetails']['executionPlanJobId'] = job_operation_details_execution_plan_job_id

    details['jobOperationDetails']['operation'] = 'APPLY'

    client = cli_util.build_client('resource_manager', ctx)
    result = client.create_job(
        create_job_details=details,
        **kwargs
    )
    if wait_for_state:
        if hasattr(client, 'get_job') and callable(getattr(client, 'get_job')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the resource has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_job(result.data.id), 'lifecycle_state', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the resource entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for resource to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the resource to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)


@job_group.command(name=cli_util.override('resource_manager.create_job_create_plan_job_operation_details.command_name', 'create-job-create-plan-job-operation-details'), help=u"""Creates a job.""")
@cli_util.option('--stack-id', required=True, help=u"""The [OCID] of the stack that is associated with the current job.""")
@cli_util.option('--display-name', help=u"""Description of the job.""")
@cli_util.option('--operation', help=u"""Terraform-specific operation to execute.""")
@cli_util.option('--apply-job-plan-resolution', type=custom_types.CLI_COMPLEX_TYPE, help=u"""""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--freeform-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Free-form tags associated with this resource. Each tag is a key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags]. Example: `{\"Department\": \"Finance\"}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--defined-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags]. Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["ACCEPTED", "IN_PROGRESS", "FAILED", "SUCCEEDED", "CANCELING", "CANCELED"]), multiple=True, help="""This operation creates, modifies or deletes a resource that has a defined lifecycle state. Specify this option to perform the action and then wait until the resource reaches a given lifecycle state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the resource to reach the lifecycle state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the resource to see if it has reached the lifecycle state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({'apply-job-plan-resolution': {'module': 'resource_manager', 'class': 'ApplyJobPlanResolution'}, 'freeform-tags': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'resource_manager', 'class': 'dict(str, dict(str, object))'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'apply-job-plan-resolution': {'module': 'resource_manager', 'class': 'ApplyJobPlanResolution'}, 'freeform-tags': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'resource_manager', 'class': 'dict(str, dict(str, object))'}}, output_type={'module': 'resource_manager', 'class': 'Job'})
@cli_util.wrap_exceptions
def create_job_create_plan_job_operation_details(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, stack_id, display_name, operation, apply_job_plan_resolution, freeform_tags, defined_tags):

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    details = {}
    details['jobOperationDetails'] = {}
    details['stackId'] = stack_id

    if display_name is not None:
        details['displayName'] = display_name

    if operation is not None:
        details['operation'] = operation

    if apply_job_plan_resolution is not None:
        details['applyJobPlanResolution'] = cli_util.parse_json_parameter("apply_job_plan_resolution", apply_job_plan_resolution)

    if freeform_tags is not None:
        details['freeformTags'] = cli_util.parse_json_parameter("freeform_tags", freeform_tags)

    if defined_tags is not None:
        details['definedTags'] = cli_util.parse_json_parameter("defined_tags", defined_tags)

    details['jobOperationDetails']['operation'] = 'PLAN'

    client = cli_util.build_client('resource_manager', ctx)
    result = client.create_job(
        create_job_details=details,
        **kwargs
    )
    if wait_for_state:
        if hasattr(client, 'get_job') and callable(getattr(client, 'get_job')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the resource has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_job(result.data.id), 'lifecycle_state', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the resource entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for resource to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the resource to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)


@job_group.command(name=cli_util.override('resource_manager.create_job_create_destroy_job_operation_details.command_name', 'create-job-create-destroy-job-operation-details'), help=u"""Creates a job.""")
@cli_util.option('--stack-id', required=True, help=u"""The [OCID] of the stack that is associated with the current job.""")
@cli_util.option('--job-operation-details-execution-plan-strategy', required=True, help=u"""Specifies the source of the execution plan to apply. Currently, only `AUTO_APPROVED` is allowed, which indicates that the job will be run without an execution plan.""")
@cli_util.option('--display-name', help=u"""Description of the job.""")
@cli_util.option('--operation', help=u"""Terraform-specific operation to execute.""")
@cli_util.option('--apply-job-plan-resolution', type=custom_types.CLI_COMPLEX_TYPE, help=u"""""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--freeform-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Free-form tags associated with this resource. Each tag is a key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags]. Example: `{\"Department\": \"Finance\"}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--defined-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags]. Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["ACCEPTED", "IN_PROGRESS", "FAILED", "SUCCEEDED", "CANCELING", "CANCELED"]), multiple=True, help="""This operation creates, modifies or deletes a resource that has a defined lifecycle state. Specify this option to perform the action and then wait until the resource reaches a given lifecycle state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the resource to reach the lifecycle state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the resource to see if it has reached the lifecycle state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({'apply-job-plan-resolution': {'module': 'resource_manager', 'class': 'ApplyJobPlanResolution'}, 'freeform-tags': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'resource_manager', 'class': 'dict(str, dict(str, object))'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'apply-job-plan-resolution': {'module': 'resource_manager', 'class': 'ApplyJobPlanResolution'}, 'freeform-tags': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'resource_manager', 'class': 'dict(str, dict(str, object))'}}, output_type={'module': 'resource_manager', 'class': 'Job'})
@cli_util.wrap_exceptions
def create_job_create_destroy_job_operation_details(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, stack_id, job_operation_details_execution_plan_strategy, display_name, operation, apply_job_plan_resolution, freeform_tags, defined_tags):

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    details = {}
    details['jobOperationDetails'] = {}
    details['stackId'] = stack_id
    details['jobOperationDetails']['executionPlanStrategy'] = job_operation_details_execution_plan_strategy

    if display_name is not None:
        details['displayName'] = display_name

    if operation is not None:
        details['operation'] = operation

    if apply_job_plan_resolution is not None:
        details['applyJobPlanResolution'] = cli_util.parse_json_parameter("apply_job_plan_resolution", apply_job_plan_resolution)

    if freeform_tags is not None:
        details['freeformTags'] = cli_util.parse_json_parameter("freeform_tags", freeform_tags)

    if defined_tags is not None:
        details['definedTags'] = cli_util.parse_json_parameter("defined_tags", defined_tags)

    details['jobOperationDetails']['operation'] = 'DESTROY'

    client = cli_util.build_client('resource_manager', ctx)
    result = client.create_job(
        create_job_details=details,
        **kwargs
    )
    if wait_for_state:
        if hasattr(client, 'get_job') and callable(getattr(client, 'get_job')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the resource has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_job(result.data.id), 'lifecycle_state', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the resource entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for resource to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the resource to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)


@stack_group.command(name=cli_util.override('resource_manager.create_stack.command_name', 'create'), help=u"""Creates a stack in the specified comparment. Specify the compartment using the compartment ID. For more information, see [Create a Stack].""")
@cli_util.option('--compartment-id', required=True, help=u"""Unique identifier ([OCID]) of the compartment in which the stack resides.""")
@cli_util.option('--config-source', required=True, type=custom_types.CLI_COMPLEX_TYPE, help=u"""""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--display-name', help=u"""The stack's display name.""")
@cli_util.option('--description', help=u"""Description of the stack.""")
@cli_util.option('--variables', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Terraform variables associated with this resource. Maximum number of variables supported is 100. The maximum size of each variable, including both name and value, is 4096 bytes. Example: `{\"CompartmentId\": \"compartment-id-value\"}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--terraform-version', help=u"""The version of Terraform to use with the stack. Example: `0.12.x`""")
@cli_util.option('--freeform-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Free-form tags associated with this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags]. Example: `{\"Department\": \"Finance\"}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--defined-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Defined tags associated with this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags]. Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["CREATING", "ACTIVE", "DELETING", "DELETED"]), multiple=True, help="""This operation creates, modifies or deletes a resource that has a defined lifecycle state. Specify this option to perform the action and then wait until the resource reaches a given lifecycle state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the resource to reach the lifecycle state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the resource to see if it has reached the lifecycle state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({'config-source': {'module': 'resource_manager', 'class': 'CreateConfigSourceDetails'}, 'variables': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'freeform-tags': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'resource_manager', 'class': 'dict(str, dict(str, object))'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'config-source': {'module': 'resource_manager', 'class': 'CreateConfigSourceDetails'}, 'variables': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'freeform-tags': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'resource_manager', 'class': 'dict(str, dict(str, object))'}}, output_type={'module': 'resource_manager', 'class': 'Stack'})
@cli_util.wrap_exceptions
def create_stack(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, compartment_id, config_source, display_name, description, variables, terraform_version, freeform_tags, defined_tags):

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    details = {}
    details['compartmentId'] = compartment_id
    details['configSource'] = cli_util.parse_json_parameter("config_source", config_source)

    if display_name is not None:
        details['displayName'] = display_name

    if description is not None:
        details['description'] = description

    if variables is not None:
        details['variables'] = cli_util.parse_json_parameter("variables", variables)

    if terraform_version is not None:
        details['terraformVersion'] = terraform_version

    if freeform_tags is not None:
        details['freeformTags'] = cli_util.parse_json_parameter("freeform_tags", freeform_tags)

    if defined_tags is not None:
        details['definedTags'] = cli_util.parse_json_parameter("defined_tags", defined_tags)

    client = cli_util.build_client('resource_manager', ctx)
    result = client.create_stack(
        create_stack_details=details,
        **kwargs
    )
    if wait_for_state:
        if hasattr(client, 'get_stack') and callable(getattr(client, 'get_stack')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the resource has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_stack(result.data.id), 'lifecycle_state', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the resource entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for resource to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the resource to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)


@stack_group.command(name=cli_util.override('resource_manager.create_stack_create_zip_upload_config_source_details.command_name', 'create-stack-create-zip-upload-config-source-details'), help=u"""Creates a stack in the specified comparment. Specify the compartment using the compartment ID. For more information, see [Create a Stack].""")
@cli_util.option('--compartment-id', required=True, help=u"""Unique identifier ([OCID]) of the compartment in which the stack resides.""")
@cli_util.option('--config-source-zip-file-base64-encoded', required=True, help=u"""""")
@cli_util.option('--display-name', help=u"""The stack's display name.""")
@cli_util.option('--description', help=u"""Description of the stack.""")
@cli_util.option('--variables', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Terraform variables associated with this resource. Maximum number of variables supported is 100. The maximum size of each variable, including both name and value, is 4096 bytes. Example: `{\"CompartmentId\": \"compartment-id-value\"}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--terraform-version', help=u"""The version of Terraform to use with the stack. Example: `0.12.x`""")
@cli_util.option('--freeform-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Free-form tags associated with this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags]. Example: `{\"Department\": \"Finance\"}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--defined-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Defined tags associated with this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags]. Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--config-source-working-directory', help=u"""File path to the directory from which Terraform runs. If not specified, the root directory is used.""")
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["CREATING", "ACTIVE", "DELETING", "DELETED"]), multiple=True, help="""This operation creates, modifies or deletes a resource that has a defined lifecycle state. Specify this option to perform the action and then wait until the resource reaches a given lifecycle state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the resource to reach the lifecycle state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the resource to see if it has reached the lifecycle state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({'variables': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'freeform-tags': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'resource_manager', 'class': 'dict(str, dict(str, object))'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'variables': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'freeform-tags': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'resource_manager', 'class': 'dict(str, dict(str, object))'}}, output_type={'module': 'resource_manager', 'class': 'Stack'})
@cli_util.wrap_exceptions
def create_stack_create_zip_upload_config_source_details(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, compartment_id, config_source_zip_file_base64_encoded, display_name, description, variables, terraform_version, freeform_tags, defined_tags, config_source_working_directory):

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    details = {}
    details['configSource'] = {}
    details['compartmentId'] = compartment_id
    details['configSource']['zipFileBase64Encoded'] = config_source_zip_file_base64_encoded

    if display_name is not None:
        details['displayName'] = display_name

    if description is not None:
        details['description'] = description

    if variables is not None:
        details['variables'] = cli_util.parse_json_parameter("variables", variables)

    if terraform_version is not None:
        details['terraformVersion'] = terraform_version

    if freeform_tags is not None:
        details['freeformTags'] = cli_util.parse_json_parameter("freeform_tags", freeform_tags)

    if defined_tags is not None:
        details['definedTags'] = cli_util.parse_json_parameter("defined_tags", defined_tags)

    if config_source_working_directory is not None:
        details['configSource']['workingDirectory'] = config_source_working_directory

    details['configSource']['configSourceType'] = 'ZIP_UPLOAD'

    client = cli_util.build_client('resource_manager', ctx)
    result = client.create_stack(
        create_stack_details=details,
        **kwargs
    )
    if wait_for_state:
        if hasattr(client, 'get_stack') and callable(getattr(client, 'get_stack')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the resource has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_stack(result.data.id), 'lifecycle_state', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the resource entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for resource to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the resource to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)


@stack_group.command(name=cli_util.override('resource_manager.delete_stack.command_name', 'delete'), help=u"""Deletes the specified stack object.""")
@cli_util.option('--stack-id', required=True, help=u"""The [OCID] of the stack.""")
@cli_util.option('--if-match', help=u"""For optimistic concurrency control. In the `PUT` or `DELETE` call for a resource, set the `if-match` parameter to the value of the etag from a previous `GET` or `POST` response for that resource.  The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.""")
@cli_util.confirm_delete_option
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["CREATING", "ACTIVE", "DELETING", "DELETED"]), multiple=True, help="""This operation creates, modifies or deletes a resource that has a defined lifecycle state. Specify this option to perform the action and then wait until the resource reaches a given lifecycle state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the resource to reach the lifecycle state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the resource to see if it has reached the lifecycle state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def delete_stack(ctx, from_json, wait_for_state, max_wait_seconds, wait_interval_seconds, stack_id, if_match):

    if isinstance(stack_id, six.string_types) and len(stack_id.strip()) == 0:
        raise click.UsageError('Parameter --stack-id cannot be whitespace or empty string')

    kwargs = {}
    if if_match is not None:
        kwargs['if_match'] = if_match
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('resource_manager', ctx)
    result = client.delete_stack(
        stack_id=stack_id,
        **kwargs
    )
    if wait_for_state:
        if hasattr(client, 'get_stack') and callable(getattr(client, 'get_stack')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the resource has entered state: {}'.format(wait_for_state), file=sys.stderr)
                oci.wait_until(client, client.get_stack(stack_id), 'lifecycle_state', wait_for_state, succeed_on_not_found=True, **wait_period_kwargs)
            except oci.exceptions.ServiceError as e:
                # We make an initial service call so we can pass the result to oci.wait_until(), however if we are waiting on the
                # outcome of a delete operation it is possible that the resource is already gone and so the initial service call
                # will result in an exception that reflects a HTTP 404. In this case, we can exit with success (rather than raising
                # the exception) since this would have been the behaviour in the waiter anyway (as for delete we provide the argument
                # succeed_on_not_found=True to the waiter).
                #
                # Any non-404 should still result in the exception being thrown.
                if e.status == 404:
                    pass
                else:
                    raise
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the resource entered the specified state. Please retrieve the resource to find its current state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for resource to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the resource to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)


@job_group.command(name=cli_util.override('resource_manager.get_job.command_name', 'get'), help=u"""Returns the specified job along with the job details.""")
@cli_util.option('--job-id', required=True, help=u"""The [OCID] of the job.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'resource_manager', 'class': 'Job'})
@cli_util.wrap_exceptions
def get_job(ctx, from_json, job_id):

    if isinstance(job_id, six.string_types) and len(job_id.strip()) == 0:
        raise click.UsageError('Parameter --job-id cannot be whitespace or empty string')

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('resource_manager', ctx)
    result = client.get_job(
        job_id=job_id,
        **kwargs
    )
    cli_util.render_response(result, ctx)


@job_group.command(name=cli_util.override('resource_manager.get_job_logs.command_name', 'get-job-logs'), help=u"""Returns log entries for the specified job in JSON format.""")
@cli_util.option('--job-id', required=True, help=u"""The [OCID] of the job.""")
@cli_util.option('--type', type=custom_types.CliCaseInsensitiveChoice(["TERRAFORM_CONSOLE"]), multiple=True, help=u"""A filter that returns only logs of a specified type.""")
@cli_util.option('--level-greater-than-or-equal-to', type=custom_types.CliCaseInsensitiveChoice(["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL"]), help=u"""A filter that returns only log entries that match a given severity level or greater.""")
@cli_util.option('--sort-order', type=custom_types.CliCaseInsensitiveChoice(["ASC", "DESC"]), help=u"""The sort order, either `ASC` (ascending) or `DESC` (descending).""")
@cli_util.option('--limit', type=click.INT, help=u"""The number of items returned in a paginated `List` call. For information about pagination, see [List Pagination].""")
@cli_util.option('--page', help=u"""The value of the `opc-next-page` response header from the preceding `List` call. For information about pagination, see [List Pagination].""")
@cli_util.option('--timestamp-greater-than-or-equal-to', type=custom_types.CLI_DATETIME, help=u"""Time stamp specifying the lower time limit for which logs are returned in a query.""" + custom_types.CLI_DATETIME.VALID_DATETIME_CLI_HELP_MESSAGE)
@cli_util.option('--timestamp-less-than-or-equal-to', type=custom_types.CLI_DATETIME, help=u"""Time stamp specifying the upper time limit for which logs are returned in a query.""" + custom_types.CLI_DATETIME.VALID_DATETIME_CLI_HELP_MESSAGE)
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'resource_manager', 'class': 'list[LogEntry]'})
@cli_util.wrap_exceptions
def get_job_logs(ctx, from_json, job_id, type, level_greater_than_or_equal_to, sort_order, limit, page, timestamp_greater_than_or_equal_to, timestamp_less_than_or_equal_to):

    if isinstance(job_id, six.string_types) and len(job_id.strip()) == 0:
        raise click.UsageError('Parameter --job-id cannot be whitespace or empty string')

    kwargs = {}
    if type is not None and len(type) > 0:
        kwargs['type'] = type
    if level_greater_than_or_equal_to is not None:
        kwargs['level_greater_than_or_equal_to'] = level_greater_than_or_equal_to
    if sort_order is not None:
        kwargs['sort_order'] = sort_order
    if limit is not None:
        kwargs['limit'] = limit
    if page is not None:
        kwargs['page'] = page
    if timestamp_greater_than_or_equal_to is not None:
        kwargs['timestamp_greater_than_or_equal_to'] = timestamp_greater_than_or_equal_to
    if timestamp_less_than_or_equal_to is not None:
        kwargs['timestamp_less_than_or_equal_to'] = timestamp_less_than_or_equal_to
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('resource_manager', ctx)
    result = client.get_job_logs(
        job_id=job_id,
        **kwargs
    )
    cli_util.render_response(result, ctx)


@job_group.command(name=cli_util.override('resource_manager.get_job_logs_content.command_name', 'get-job-logs-content'), help=u"""Returns raw log file for the specified job in text format. Returns a maximum of 100,000 log entries.""")
@cli_util.option('--job-id', required=True, help=u"""The [OCID] of the job.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def get_job_logs_content(ctx, from_json, job_id):

    if isinstance(job_id, six.string_types) and len(job_id.strip()) == 0:
        raise click.UsageError('Parameter --job-id cannot be whitespace or empty string')

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('resource_manager', ctx)
    result = client.get_job_logs_content(
        job_id=job_id,
        **kwargs
    )
    cli_util.render_response(result, ctx)


@job_group.command(name=cli_util.override('resource_manager.get_job_tf_config.command_name', 'get-job-tf-config'), help=u"""Returns the Terraform configuration file for the specified job in .zip format. Returns an error if no zip file is found.""")
@cli_util.option('--job-id', required=True, help=u"""The [OCID] of the job.""")
@cli_util.option('--file', type=click.File(mode='wb'), required=True, help="The name of the file that will receive the response data, or '-' to write to STDOUT.")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def get_job_tf_config(ctx, from_json, file, job_id):

    if isinstance(job_id, six.string_types) and len(job_id.strip()) == 0:
        raise click.UsageError('Parameter --job-id cannot be whitespace or empty string')

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('resource_manager', ctx)
    result = client.get_job_tf_config(
        job_id=job_id,
        **kwargs
    )

    # If outputting to stdout we don't want to print a progress bar because it will get mixed up with the output
    # Also we need a non-zero Content-Length in order to display a meaningful progress bar
    bar = None
    if hasattr(file, 'name') and file.name != '<stdout>' and 'Content-Length' in result.headers:
        content_length = int(result.headers['Content-Length'])
        if content_length > 0:
            bar = click.progressbar(length=content_length, label='Downloading file')

    try:
        if bar:
            bar.__enter__()

        # TODO: Make the download size a configurable option
        # use decode_content=True to automatically unzip service responses (this should be overridden for object storage)
        for chunk in result.data.raw.stream(cli_constants.MEBIBYTE, decode_content=True):
            if bar:
                bar.update(len(chunk))
            file.write(chunk)
    finally:
        if bar:
            bar.render_finish()
        file.close()


@job_group.command(name=cli_util.override('resource_manager.get_job_tf_state.command_name', 'get-job-tf-state'), help=u"""Returns the Terraform state for the specified job.""")
@cli_util.option('--job-id', required=True, help=u"""The [OCID] of the job.""")
@cli_util.option('--file', type=click.File(mode='wb'), required=True, help="The name of the file that will receive the response data, or '-' to write to STDOUT.")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def get_job_tf_state(ctx, from_json, file, job_id):

    if isinstance(job_id, six.string_types) and len(job_id.strip()) == 0:
        raise click.UsageError('Parameter --job-id cannot be whitespace or empty string')

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('resource_manager', ctx)
    result = client.get_job_tf_state(
        job_id=job_id,
        **kwargs
    )

    # If outputting to stdout we don't want to print a progress bar because it will get mixed up with the output
    # Also we need a non-zero Content-Length in order to display a meaningful progress bar
    bar = None
    if hasattr(file, 'name') and file.name != '<stdout>' and 'Content-Length' in result.headers:
        content_length = int(result.headers['Content-Length'])
        if content_length > 0:
            bar = click.progressbar(length=content_length, label='Downloading file')

    try:
        if bar:
            bar.__enter__()

        # TODO: Make the download size a configurable option
        # use decode_content=True to automatically unzip service responses (this should be overridden for object storage)
        for chunk in result.data.raw.stream(cli_constants.MEBIBYTE, decode_content=True):
            if bar:
                bar.update(len(chunk))
            file.write(chunk)
    finally:
        if bar:
            bar.render_finish()
        file.close()


@stack_group.command(name=cli_util.override('resource_manager.get_stack.command_name', 'get'), help=u"""Gets a stack using the stack ID.""")
@cli_util.option('--stack-id', required=True, help=u"""The [OCID] of the stack.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'resource_manager', 'class': 'Stack'})
@cli_util.wrap_exceptions
def get_stack(ctx, from_json, stack_id):

    if isinstance(stack_id, six.string_types) and len(stack_id.strip()) == 0:
        raise click.UsageError('Parameter --stack-id cannot be whitespace or empty string')

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('resource_manager', ctx)
    result = client.get_stack(
        stack_id=stack_id,
        **kwargs
    )
    cli_util.render_response(result, ctx)


@stack_group.command(name=cli_util.override('resource_manager.get_stack_tf_config.command_name', 'get-stack-tf-config'), help=u"""Returns the Terraform configuration file in .zip format for the specified stack. Returns an error if no zip file is found.""")
@cli_util.option('--stack-id', required=True, help=u"""The [OCID] of the stack.""")
@cli_util.option('--file', type=click.File(mode='wb'), required=True, help="The name of the file that will receive the response data, or '-' to write to STDOUT.")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def get_stack_tf_config(ctx, from_json, file, stack_id):

    if isinstance(stack_id, six.string_types) and len(stack_id.strip()) == 0:
        raise click.UsageError('Parameter --stack-id cannot be whitespace or empty string')

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('resource_manager', ctx)
    result = client.get_stack_tf_config(
        stack_id=stack_id,
        **kwargs
    )

    # If outputting to stdout we don't want to print a progress bar because it will get mixed up with the output
    # Also we need a non-zero Content-Length in order to display a meaningful progress bar
    bar = None
    if hasattr(file, 'name') and file.name != '<stdout>' and 'Content-Length' in result.headers:
        content_length = int(result.headers['Content-Length'])
        if content_length > 0:
            bar = click.progressbar(length=content_length, label='Downloading file')

    try:
        if bar:
            bar.__enter__()

        # TODO: Make the download size a configurable option
        # use decode_content=True to automatically unzip service responses (this should be overridden for object storage)
        for chunk in result.data.raw.stream(cli_constants.MEBIBYTE, decode_content=True):
            if bar:
                bar.update(len(chunk))
            file.write(chunk)
    finally:
        if bar:
            bar.render_finish()
        file.close()


@stack_group.command(name=cli_util.override('resource_manager.get_stack_tf_state.command_name', 'get-stack-tf-state'), help=u"""Returns the Terraform state for the specified stack.""")
@cli_util.option('--stack-id', required=True, help=u"""The [OCID] of the stack.""")
@cli_util.option('--file', type=click.File(mode='wb'), required=True, help="The name of the file that will receive the response data, or '-' to write to STDOUT.")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def get_stack_tf_state(ctx, from_json, file, stack_id):

    if isinstance(stack_id, six.string_types) and len(stack_id.strip()) == 0:
        raise click.UsageError('Parameter --stack-id cannot be whitespace or empty string')

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('resource_manager', ctx)
    result = client.get_stack_tf_state(
        stack_id=stack_id,
        **kwargs
    )

    # If outputting to stdout we don't want to print a progress bar because it will get mixed up with the output
    # Also we need a non-zero Content-Length in order to display a meaningful progress bar
    bar = None
    if hasattr(file, 'name') and file.name != '<stdout>' and 'Content-Length' in result.headers:
        content_length = int(result.headers['Content-Length'])
        if content_length > 0:
            bar = click.progressbar(length=content_length, label='Downloading file')

    try:
        if bar:
            bar.__enter__()

        # TODO: Make the download size a configurable option
        # use decode_content=True to automatically unzip service responses (this should be overridden for object storage)
        for chunk in result.data.raw.stream(cli_constants.MEBIBYTE, decode_content=True):
            if bar:
                bar.update(len(chunk))
            file.write(chunk)
    finally:
        if bar:
            bar.render_finish()
        file.close()


@work_request_group.command(name=cli_util.override('resource_manager.get_work_request.command_name', 'get'), help=u"""Return the given work request.""")
@cli_util.option('--work-request-id', required=True, help=u"""The [OCID] of the work request.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'resource_manager', 'class': 'WorkRequest'})
@cli_util.wrap_exceptions
def get_work_request(ctx, from_json, work_request_id):

    if isinstance(work_request_id, six.string_types) and len(work_request_id.strip()) == 0:
        raise click.UsageError('Parameter --work-request-id cannot be whitespace or empty string')

    kwargs = {}
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('resource_manager', ctx)
    result = client.get_work_request(
        work_request_id=work_request_id,
        **kwargs
    )
    cli_util.render_response(result, ctx)


@job_group.command(name=cli_util.override('resource_manager.list_jobs.command_name', 'list'), help=u"""Returns a list of jobs in a stack or compartment, ordered by time created.

- To list all jobs in a stack, provide the stack [OCID]. - To list all jobs in a compartment, provide the compartment [OCID]. - To return a specific job, provide the job [OCID].""")
@cli_util.option('--compartment-id', help=u"""The compartment [OCID] on which to filter.""")
@cli_util.option('--stack-id', help=u"""The stack [OCID] on which to filter.""")
@cli_util.option('--id', help=u"""The [OCID] on which to query for jobs.""")
@cli_util.option('--lifecycle-state', type=custom_types.CliCaseInsensitiveChoice(["ACCEPTED", "IN_PROGRESS", "FAILED", "SUCCEEDED", "CANCELING", "CANCELED"]), help=u"""A filter that returns all resources that match the specified lifecycle state. The state value is case-insensitive.

Allowable values: - ACCEPTED - IN_PROGRESS - FAILED - SUCCEEDED - CANCELING - CANCELED""")
@cli_util.option('--display-name', help=u"""Display name on which to query.""")
@cli_util.option('--sort-by', type=custom_types.CliCaseInsensitiveChoice(["TIMECREATED", "DISPLAYNAME"]), help=u"""Specifies the field on which to sort. By default, `TIMECREATED` is ordered descending. By default, `DISPLAYNAME` is ordered ascending. Note that you can sort only on one field.""")
@cli_util.option('--sort-order', type=custom_types.CliCaseInsensitiveChoice(["ASC", "DESC"]), help=u"""The sort order, either `ASC` (ascending) or `DESC` (descending).""")
@cli_util.option('--limit', type=click.INT, help=u"""The number of items returned in a paginated `List` call. For information about pagination, see [List Pagination].""")
@cli_util.option('--page', help=u"""The value of the `opc-next-page` response header from the preceding `List` call. For information about pagination, see [List Pagination].""")
@cli_util.option('--all', 'all_pages', is_flag=True, help="""Fetches all pages of results. If you provide this option, then you cannot provide the --limit option.""")
@cli_util.option('--page-size', type=click.INT, help="""When fetching results, the number of results to fetch per call. Only valid when used with --all or --limit, and ignored otherwise.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'resource_manager', 'class': 'list[JobSummary]'})
@cli_util.wrap_exceptions
def list_jobs(ctx, from_json, all_pages, page_size, compartment_id, stack_id, id, lifecycle_state, display_name, sort_by, sort_order, limit, page):

    if all_pages and limit:
        raise click.UsageError('If you provide the --all option you cannot provide the --limit option')

    kwargs = {}
    if compartment_id is not None:
        kwargs['compartment_id'] = compartment_id
    if stack_id is not None:
        kwargs['stack_id'] = stack_id
    if id is not None:
        kwargs['id'] = id
    if lifecycle_state is not None:
        kwargs['lifecycle_state'] = lifecycle_state
    if display_name is not None:
        kwargs['display_name'] = display_name
    if sort_by is not None:
        kwargs['sort_by'] = sort_by
    if sort_order is not None:
        kwargs['sort_order'] = sort_order
    if limit is not None:
        kwargs['limit'] = limit
    if page is not None:
        kwargs['page'] = page
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('resource_manager', ctx)
    if all_pages:
        if page_size:
            kwargs['limit'] = page_size

        result = cli_util.list_call_get_all_results(
            client.list_jobs,
            **kwargs
        )
    elif limit is not None:
        result = cli_util.list_call_get_up_to_limit(
            client.list_jobs,
            limit,
            page_size,
            **kwargs
        )
    else:
        result = client.list_jobs(
            **kwargs
        )
    cli_util.render_response(result, ctx)


@stack_group.command(name=cli_util.override('resource_manager.list_stacks.command_name', 'list'), help=u"""Returns a list of stacks. - If called using the compartment ID, returns all stacks in the specified compartment. - If called using the stack ID, returns the specified stack.""")
@cli_util.option('--compartment-id', help=u"""The compartment [OCID] on which to filter.""")
@cli_util.option('--id', help=u"""The [OCID] on which to query for a stack.""")
@cli_util.option('--lifecycle-state', type=custom_types.CliCaseInsensitiveChoice(["CREATING", "ACTIVE", "DELETING", "DELETED"]), help=u"""A filter that returns only those resources that match the specified lifecycle state. The state value is case-insensitive.

Allowable values: - CREATING - ACTIVE - DELETING - DELETED""")
@cli_util.option('--display-name', help=u"""Display name on which to query.""")
@cli_util.option('--sort-by', type=custom_types.CliCaseInsensitiveChoice(["TIMECREATED", "DISPLAYNAME"]), help=u"""Specifies the field on which to sort. By default, `TIMECREATED` is ordered descending. By default, `DISPLAYNAME` is ordered ascending. Note that you can sort only on one field.""")
@cli_util.option('--sort-order', type=custom_types.CliCaseInsensitiveChoice(["ASC", "DESC"]), help=u"""The sort order, either `ASC` (ascending) or `DESC` (descending).""")
@cli_util.option('--limit', type=click.INT, help=u"""The number of items returned in a paginated `List` call. For information about pagination, see [List Pagination].""")
@cli_util.option('--page', help=u"""The value of the `opc-next-page` response header from the preceding `List` call. For information about pagination, see [List Pagination].""")
@cli_util.option('--all', 'all_pages', is_flag=True, help="""Fetches all pages of results. If you provide this option, then you cannot provide the --limit option.""")
@cli_util.option('--page-size', type=click.INT, help="""When fetching results, the number of results to fetch per call. Only valid when used with --all or --limit, and ignored otherwise.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'resource_manager', 'class': 'list[StackSummary]'})
@cli_util.wrap_exceptions
def list_stacks(ctx, from_json, all_pages, page_size, compartment_id, id, lifecycle_state, display_name, sort_by, sort_order, limit, page):

    if all_pages and limit:
        raise click.UsageError('If you provide the --all option you cannot provide the --limit option')

    kwargs = {}
    if compartment_id is not None:
        kwargs['compartment_id'] = compartment_id
    if id is not None:
        kwargs['id'] = id
    if lifecycle_state is not None:
        kwargs['lifecycle_state'] = lifecycle_state
    if display_name is not None:
        kwargs['display_name'] = display_name
    if sort_by is not None:
        kwargs['sort_by'] = sort_by
    if sort_order is not None:
        kwargs['sort_order'] = sort_order
    if limit is not None:
        kwargs['limit'] = limit
    if page is not None:
        kwargs['page'] = page
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('resource_manager', ctx)
    if all_pages:
        if page_size:
            kwargs['limit'] = page_size

        result = cli_util.list_call_get_all_results(
            client.list_stacks,
            **kwargs
        )
    elif limit is not None:
        result = cli_util.list_call_get_up_to_limit(
            client.list_stacks,
            limit,
            page_size,
            **kwargs
        )
    else:
        result = client.list_stacks(
            **kwargs
        )
    cli_util.render_response(result, ctx)


@stack_group.command(name=cli_util.override('resource_manager.list_terraform_versions.command_name', 'list-terraform-versions'), help=u"""Returns a list of supported Terraform versions for use with stacks.""")
@cli_util.option('--compartment-id', help=u"""The compartment [OCID] on which to filter.""")
@cli_util.option('--all', 'all_pages', is_flag=True, help="""Fetches all pages of results.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'resource_manager', 'class': 'TerraformVersionCollection'})
@cli_util.wrap_exceptions
def list_terraform_versions(ctx, from_json, all_pages, compartment_id):

    kwargs = {}
    if compartment_id is not None:
        kwargs['compartment_id'] = compartment_id
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('resource_manager', ctx)
    result = client.list_terraform_versions(
        **kwargs
    )
    cli_util.render_response(result, ctx)


@work_request_group.command(name=cli_util.override('resource_manager.list_work_request_errors.command_name', 'list-work-request-errors'), help=u"""Return a (paginated) list of errors for a given work request.""")
@cli_util.option('--work-request-id', required=True, help=u"""The [OCID] of the work request.""")
@cli_util.option('--compartment-id', help=u"""The compartment [OCID] on which to filter.""")
@cli_util.option('--limit', type=click.INT, help=u"""The number of items returned in a paginated `List` call. For information about pagination, see [List Pagination].""")
@cli_util.option('--page', help=u"""The value of the `opc-next-page` response header from the preceding `List` call. For information about pagination, see [List Pagination].""")
@cli_util.option('--sort-order', type=custom_types.CliCaseInsensitiveChoice(["ASC", "DESC"]), help=u"""The sort order, either `ASC` (ascending) or `DESC` (descending).""")
@cli_util.option('--all', 'all_pages', is_flag=True, help="""Fetches all pages of results. If you provide this option, then you cannot provide the --limit option.""")
@cli_util.option('--page-size', type=click.INT, help="""When fetching results, the number of results to fetch per call. Only valid when used with --all or --limit, and ignored otherwise.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'resource_manager', 'class': 'list[WorkRequestError]'})
@cli_util.wrap_exceptions
def list_work_request_errors(ctx, from_json, all_pages, page_size, work_request_id, compartment_id, limit, page, sort_order):

    if all_pages and limit:
        raise click.UsageError('If you provide the --all option you cannot provide the --limit option')

    if isinstance(work_request_id, six.string_types) and len(work_request_id.strip()) == 0:
        raise click.UsageError('Parameter --work-request-id cannot be whitespace or empty string')

    kwargs = {}
    if compartment_id is not None:
        kwargs['compartment_id'] = compartment_id
    if limit is not None:
        kwargs['limit'] = limit
    if page is not None:
        kwargs['page'] = page
    if sort_order is not None:
        kwargs['sort_order'] = sort_order
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('resource_manager', ctx)
    if all_pages:
        if page_size:
            kwargs['limit'] = page_size

        result = cli_util.list_call_get_all_results(
            client.list_work_request_errors,
            work_request_id=work_request_id,
            **kwargs
        )
    elif limit is not None:
        result = cli_util.list_call_get_up_to_limit(
            client.list_work_request_errors,
            limit,
            page_size,
            work_request_id=work_request_id,
            **kwargs
        )
    else:
        result = client.list_work_request_errors(
            work_request_id=work_request_id,
            **kwargs
        )
    cli_util.render_response(result, ctx)


@work_request_group.command(name=cli_util.override('resource_manager.list_work_request_logs.command_name', 'list-work-request-logs'), help=u"""Return a (paginated) list of logs for a given work request.""")
@cli_util.option('--work-request-id', required=True, help=u"""The [OCID] of the work request.""")
@cli_util.option('--compartment-id', help=u"""The compartment [OCID] on which to filter.""")
@cli_util.option('--limit', type=click.INT, help=u"""The number of items returned in a paginated `List` call. For information about pagination, see [List Pagination].""")
@cli_util.option('--page', help=u"""The value of the `opc-next-page` response header from the preceding `List` call. For information about pagination, see [List Pagination].""")
@cli_util.option('--sort-order', type=custom_types.CliCaseInsensitiveChoice(["ASC", "DESC"]), help=u"""The sort order, either `ASC` (ascending) or `DESC` (descending).""")
@cli_util.option('--all', 'all_pages', is_flag=True, help="""Fetches all pages of results. If you provide this option, then you cannot provide the --limit option.""")
@cli_util.option('--page-size', type=click.INT, help="""When fetching results, the number of results to fetch per call. Only valid when used with --all or --limit, and ignored otherwise.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'resource_manager', 'class': 'list[WorkRequestLogEntry]'})
@cli_util.wrap_exceptions
def list_work_request_logs(ctx, from_json, all_pages, page_size, work_request_id, compartment_id, limit, page, sort_order):

    if all_pages and limit:
        raise click.UsageError('If you provide the --all option you cannot provide the --limit option')

    if isinstance(work_request_id, six.string_types) and len(work_request_id.strip()) == 0:
        raise click.UsageError('Parameter --work-request-id cannot be whitespace or empty string')

    kwargs = {}
    if compartment_id is not None:
        kwargs['compartment_id'] = compartment_id
    if limit is not None:
        kwargs['limit'] = limit
    if page is not None:
        kwargs['page'] = page
    if sort_order is not None:
        kwargs['sort_order'] = sort_order
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('resource_manager', ctx)
    if all_pages:
        if page_size:
            kwargs['limit'] = page_size

        result = cli_util.list_call_get_all_results(
            client.list_work_request_logs,
            work_request_id=work_request_id,
            **kwargs
        )
    elif limit is not None:
        result = cli_util.list_call_get_up_to_limit(
            client.list_work_request_logs,
            limit,
            page_size,
            work_request_id=work_request_id,
            **kwargs
        )
    else:
        result = client.list_work_request_logs(
            work_request_id=work_request_id,
            **kwargs
        )
    cli_util.render_response(result, ctx)


@work_request_group.command(name=cli_util.override('resource_manager.list_work_requests.command_name', 'list'), help=u"""Lists the work requests in a given compartment or for a given resource.""")
@cli_util.option('--compartment-id', required=True, help=u"""The compartment [OCID] on which to filter.""")
@cli_util.option('--resource-id', help=u"""The [OCID] of the resource.""")
@cli_util.option('--limit', type=click.INT, help=u"""The number of items returned in a paginated `List` call. For information about pagination, see [List Pagination].""")
@cli_util.option('--page', help=u"""The value of the `opc-next-page` response header from the preceding `List` call. For information about pagination, see [List Pagination].""")
@cli_util.option('--all', 'all_pages', is_flag=True, help="""Fetches all pages of results. If you provide this option, then you cannot provide the --limit option.""")
@cli_util.option('--page-size', type=click.INT, help="""When fetching results, the number of results to fetch per call. Only valid when used with --all or --limit, and ignored otherwise.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={}, output_type={'module': 'resource_manager', 'class': 'list[WorkRequestSummary]'})
@cli_util.wrap_exceptions
def list_work_requests(ctx, from_json, all_pages, page_size, compartment_id, resource_id, limit, page):

    if all_pages and limit:
        raise click.UsageError('If you provide the --all option you cannot provide the --limit option')

    kwargs = {}
    if resource_id is not None:
        kwargs['resource_id'] = resource_id
    if limit is not None:
        kwargs['limit'] = limit
    if page is not None:
        kwargs['page'] = page
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])
    client = cli_util.build_client('resource_manager', ctx)
    if all_pages:
        if page_size:
            kwargs['limit'] = page_size

        result = cli_util.list_call_get_all_results(
            client.list_work_requests,
            compartment_id=compartment_id,
            **kwargs
        )
    elif limit is not None:
        result = cli_util.list_call_get_up_to_limit(
            client.list_work_requests,
            limit,
            page_size,
            compartment_id=compartment_id,
            **kwargs
        )
    else:
        result = client.list_work_requests(
            compartment_id=compartment_id,
            **kwargs
        )
    cli_util.render_response(result, ctx)


@job_group.command(name=cli_util.override('resource_manager.update_job.command_name', 'update'), help=u"""Updates the specified job.""")
@cli_util.option('--job-id', required=True, help=u"""The [OCID] of the job.""")
@cli_util.option('--display-name', help=u"""The new display name to set.""")
@cli_util.option('--freeform-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Free-form tags associated with this resource. Each tag is a key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags]. Example: `{\"Department\": \"Finance\"}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--defined-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags]. Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--if-match', help=u"""For optimistic concurrency control. In the `PUT` or `DELETE` call for a resource, set the `if-match` parameter to the value of the etag from a previous `GET` or `POST` response for that resource.  The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.""")
@cli_util.option('--force', help="""Perform update without prompting for confirmation.""", is_flag=True)
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["ACCEPTED", "IN_PROGRESS", "FAILED", "SUCCEEDED", "CANCELING", "CANCELED"]), multiple=True, help="""This operation creates, modifies or deletes a resource that has a defined lifecycle state. Specify this option to perform the action and then wait until the resource reaches a given lifecycle state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the resource to reach the lifecycle state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the resource to see if it has reached the lifecycle state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({'freeform-tags': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'resource_manager', 'class': 'dict(str, dict(str, object))'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'freeform-tags': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'resource_manager', 'class': 'dict(str, dict(str, object))'}}, output_type={'module': 'resource_manager', 'class': 'Job'})
@cli_util.wrap_exceptions
def update_job(ctx, from_json, force, wait_for_state, max_wait_seconds, wait_interval_seconds, job_id, display_name, freeform_tags, defined_tags, if_match):

    if isinstance(job_id, six.string_types) and len(job_id.strip()) == 0:
        raise click.UsageError('Parameter --job-id cannot be whitespace or empty string')
    if not force:
        if freeform_tags or defined_tags:
            if not click.confirm("WARNING: Updates to freeform-tags and defined-tags will replace any existing values. Are you sure you want to continue?"):
                ctx.abort()

    kwargs = {}
    if if_match is not None:
        kwargs['if_match'] = if_match
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    details = {}

    if display_name is not None:
        details['displayName'] = display_name

    if freeform_tags is not None:
        details['freeformTags'] = cli_util.parse_json_parameter("freeform_tags", freeform_tags)

    if defined_tags is not None:
        details['definedTags'] = cli_util.parse_json_parameter("defined_tags", defined_tags)

    client = cli_util.build_client('resource_manager', ctx)
    result = client.update_job(
        job_id=job_id,
        update_job_details=details,
        **kwargs
    )
    if wait_for_state:
        if hasattr(client, 'get_job') and callable(getattr(client, 'get_job')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the resource has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_job(result.data.id), 'lifecycle_state', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the resource entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for resource to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the resource to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)


@stack_group.command(name=cli_util.override('resource_manager.update_stack.command_name', 'update'), help=u"""Updates the specified stack object. Use `UpdateStack` when you update your Terraform configuration and want your changes to be reflected in the execution plan. For more information, see [Update a Stack] and [Edit or Delete a Stack].""")
@cli_util.option('--stack-id', required=True, help=u"""The [OCID] of the stack.""")
@cli_util.option('--display-name', help=u"""The name of the stack.""")
@cli_util.option('--description', help=u"""Description of the stack.""")
@cli_util.option('--config-source', type=custom_types.CLI_COMPLEX_TYPE, help=u"""""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--variables', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Terraform variables associated with this resource. The maximum number of variables supported is 100. The maximum size of each variable, including both name and value, is 4096 bytes. Example: `{\"CompartmentId\": \"compartment-id-value\"}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--terraform-version', help=u"""The version of Terraform to use with the stack. Example: `0.12.x`""")
@cli_util.option('--freeform-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Free-form tags associated with this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags]. Example: `{\"Department\": \"Finance\"}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--defined-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags]. Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--if-match', help=u"""For optimistic concurrency control. In the `PUT` or `DELETE` call for a resource, set the `if-match` parameter to the value of the etag from a previous `GET` or `POST` response for that resource.  The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.""")
@cli_util.option('--force', help="""Perform update without prompting for confirmation.""", is_flag=True)
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["CREATING", "ACTIVE", "DELETING", "DELETED"]), multiple=True, help="""This operation creates, modifies or deletes a resource that has a defined lifecycle state. Specify this option to perform the action and then wait until the resource reaches a given lifecycle state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the resource to reach the lifecycle state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the resource to see if it has reached the lifecycle state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({'config-source': {'module': 'resource_manager', 'class': 'UpdateConfigSourceDetails'}, 'variables': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'freeform-tags': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'resource_manager', 'class': 'dict(str, dict(str, object))'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'config-source': {'module': 'resource_manager', 'class': 'UpdateConfigSourceDetails'}, 'variables': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'freeform-tags': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'resource_manager', 'class': 'dict(str, dict(str, object))'}}, output_type={'module': 'resource_manager', 'class': 'Stack'})
@cli_util.wrap_exceptions
def update_stack(ctx, from_json, force, wait_for_state, max_wait_seconds, wait_interval_seconds, stack_id, display_name, description, config_source, variables, terraform_version, freeform_tags, defined_tags, if_match):

    if isinstance(stack_id, six.string_types) and len(stack_id.strip()) == 0:
        raise click.UsageError('Parameter --stack-id cannot be whitespace or empty string')
    if not force:
        if config_source or variables or freeform_tags or defined_tags:
            if not click.confirm("WARNING: Updates to config-source and variables and freeform-tags and defined-tags will replace any existing values. Are you sure you want to continue?"):
                ctx.abort()

    kwargs = {}
    if if_match is not None:
        kwargs['if_match'] = if_match
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    details = {}

    if display_name is not None:
        details['displayName'] = display_name

    if description is not None:
        details['description'] = description

    if config_source is not None:
        details['configSource'] = cli_util.parse_json_parameter("config_source", config_source)

    if variables is not None:
        details['variables'] = cli_util.parse_json_parameter("variables", variables)

    if terraform_version is not None:
        details['terraformVersion'] = terraform_version

    if freeform_tags is not None:
        details['freeformTags'] = cli_util.parse_json_parameter("freeform_tags", freeform_tags)

    if defined_tags is not None:
        details['definedTags'] = cli_util.parse_json_parameter("defined_tags", defined_tags)

    client = cli_util.build_client('resource_manager', ctx)
    result = client.update_stack(
        stack_id=stack_id,
        update_stack_details=details,
        **kwargs
    )
    if wait_for_state:
        if hasattr(client, 'get_stack') and callable(getattr(client, 'get_stack')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the resource has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_stack(result.data.id), 'lifecycle_state', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the resource entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for resource to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the resource to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)


@stack_group.command(name=cli_util.override('resource_manager.update_stack_update_zip_upload_config_source_details.command_name', 'update-stack-update-zip-upload-config-source-details'), help=u"""Updates the specified stack object. Use `UpdateStack` when you update your Terraform configuration and want your changes to be reflected in the execution plan. For more information, see [Update a Stack] and [Edit or Delete a Stack].""")
@cli_util.option('--stack-id', required=True, help=u"""The [OCID] of the stack.""")
@cli_util.option('--display-name', help=u"""The name of the stack.""")
@cli_util.option('--description', help=u"""Description of the stack.""")
@cli_util.option('--variables', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Terraform variables associated with this resource. The maximum number of variables supported is 100. The maximum size of each variable, including both name and value, is 4096 bytes. Example: `{\"CompartmentId\": \"compartment-id-value\"}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--terraform-version', help=u"""The version of Terraform to use with the stack. Example: `0.12.x`""")
@cli_util.option('--freeform-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Free-form tags associated with this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see [Resource Tags]. Example: `{\"Department\": \"Finance\"}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--defined-tags', type=custom_types.CLI_COMPLEX_TYPE, help=u"""Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see [Resource Tags]. Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`""" + custom_types.cli_complex_type.COMPLEX_TYPE_HELP)
@cli_util.option('--if-match', help=u"""For optimistic concurrency control. In the `PUT` or `DELETE` call for a resource, set the `if-match` parameter to the value of the etag from a previous `GET` or `POST` response for that resource.  The resource will be updated or deleted only if the etag you provide matches the resource's current etag value.""")
@cli_util.option('--config-source-working-directory', help=u"""The path of the directory from which to run terraform. If not specified, the the root will be used.""")
@cli_util.option('--config-source-zip-file-base64-encoded', help=u"""""")
@cli_util.option('--force', help="""Perform update without prompting for confirmation.""", is_flag=True)
@cli_util.option('--wait-for-state', type=custom_types.CliCaseInsensitiveChoice(["CREATING", "ACTIVE", "DELETING", "DELETED"]), multiple=True, help="""This operation creates, modifies or deletes a resource that has a defined lifecycle state. Specify this option to perform the action and then wait until the resource reaches a given lifecycle state. Multiple states can be specified, returning on the first state. For example, --wait-for-state SUCCEEDED --wait-for-state FAILED would return on whichever lifecycle state is reached first. If timeout is reached, a return code of 2 is returned. For any other error, a return code of 1 is returned.""")
@cli_util.option('--max-wait-seconds', type=click.INT, help="""The maximum time to wait for the resource to reach the lifecycle state defined by --wait-for-state. Defaults to 1200 seconds.""")
@cli_util.option('--wait-interval-seconds', type=click.INT, help="""Check every --wait-interval-seconds to see whether the resource to see if it has reached the lifecycle state defined by --wait-for-state. Defaults to 30 seconds.""")
@json_skeleton_utils.get_cli_json_input_option({'variables': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'freeform-tags': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'resource_manager', 'class': 'dict(str, dict(str, object))'}})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={'variables': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'freeform-tags': {'module': 'resource_manager', 'class': 'dict(str, string)'}, 'defined-tags': {'module': 'resource_manager', 'class': 'dict(str, dict(str, object))'}}, output_type={'module': 'resource_manager', 'class': 'Stack'})
@cli_util.wrap_exceptions
def update_stack_update_zip_upload_config_source_details(ctx, from_json, force, wait_for_state, max_wait_seconds, wait_interval_seconds, stack_id, display_name, description, variables, terraform_version, freeform_tags, defined_tags, if_match, config_source_working_directory, config_source_zip_file_base64_encoded):

    if isinstance(stack_id, six.string_types) and len(stack_id.strip()) == 0:
        raise click.UsageError('Parameter --stack-id cannot be whitespace or empty string')
    if not force:
        if variables or freeform_tags or defined_tags:
            if not click.confirm("WARNING: Updates to variables and freeform-tags and defined-tags will replace any existing values. Are you sure you want to continue?"):
                ctx.abort()

    kwargs = {}
    if if_match is not None:
        kwargs['if_match'] = if_match
    kwargs['opc_request_id'] = cli_util.use_or_generate_request_id(ctx.obj['request_id'])

    details = {}
    details['configSource'] = {}

    if display_name is not None:
        details['displayName'] = display_name

    if description is not None:
        details['description'] = description

    if variables is not None:
        details['variables'] = cli_util.parse_json_parameter("variables", variables)

    if terraform_version is not None:
        details['terraformVersion'] = terraform_version

    if freeform_tags is not None:
        details['freeformTags'] = cli_util.parse_json_parameter("freeform_tags", freeform_tags)

    if defined_tags is not None:
        details['definedTags'] = cli_util.parse_json_parameter("defined_tags", defined_tags)

    if config_source_working_directory is not None:
        details['configSource']['workingDirectory'] = config_source_working_directory

    if config_source_zip_file_base64_encoded is not None:
        details['configSource']['zipFileBase64Encoded'] = config_source_zip_file_base64_encoded

    details['configSource']['configSourceType'] = 'ZIP_UPLOAD'

    client = cli_util.build_client('resource_manager', ctx)
    result = client.update_stack(
        stack_id=stack_id,
        update_stack_details=details,
        **kwargs
    )
    if wait_for_state:
        if hasattr(client, 'get_stack') and callable(getattr(client, 'get_stack')):
            try:
                wait_period_kwargs = {}
                if max_wait_seconds is not None:
                    wait_period_kwargs['max_wait_seconds'] = max_wait_seconds
                if wait_interval_seconds is not None:
                    wait_period_kwargs['max_interval_seconds'] = wait_interval_seconds

                click.echo('Action completed. Waiting until the resource has entered state: {}'.format(wait_for_state), file=sys.stderr)
                result = oci.wait_until(client, client.get_stack(result.data.id), 'lifecycle_state', wait_for_state, **wait_period_kwargs)
            except oci.exceptions.MaximumWaitTimeExceeded as e:
                # If we fail, we should show an error, but we should still provide the information to the customer
                click.echo('Failed to wait until the resource entered the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                sys.exit(2)
            except Exception:
                click.echo('Encountered error while waiting for resource to enter the specified state. Outputting last known resource state', file=sys.stderr)
                cli_util.render_response(result, ctx)
                raise
        else:
            click.echo('Unable to wait for the resource to enter the specified state', file=sys.stderr)
    cli_util.render_response(result, ctx)
