# coding: utf-8
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.

from __future__ import print_function

import click
import os
import six
import sys

from oci import exceptions
from oci import config as oci_config

from oci_cli import cli_util
from oci_cli import json_skeleton_utils
from oci_cli.aliasing import CommandGroupWithAlias
from services.dts.src.oci_cli_dts.appliance_init_auth_spec import InitAuthSpec

from services.dts.src.oci_cli_dts.generated import dts_service_cli
from services.dts.src.oci_cli_dts.appliance_init_auth import InitAuth
from services.dts.src.oci_cli_dts.appliance_client_proxy import ApplianceClientProxy

from services.dts.src.oci_cli_dts.appliance_config_manager import ApplianceConfigManager
from services.dts.src.oci_cli_dts.appliance_constants import APPLIANCE_CONFIGS_BASE_DIR, ENDPOINT, APPLIANCE_PROFILE, \
    LIFECYCLE_STATE_PREPARING, KEY_FILE_KEY, APPLIANCE_UPLOAD_USER_CONFIG_PATH, TEST_OBJECT


"""
physical-appliance command
This is a local command set and not generated from spec, but created here.
These commands accesses the locally attached physical appliances.
"""


@click.command('physical-appliance', cls=CommandGroupWithAlias, help="""Physical Appliance Operations""")
@cli_util.help_option_group
def physical_appliance_group():
    pass


dts_service_cli.dts_service_group.add_command(physical_appliance_group)


@physical_appliance_group.command('initialize-authentication',
                                  help=u"""Initializes authentication between the Data Transfer Utility
                                  and the transfer appliance.""")
@cli_util.option('--job-id', required=True, help=u"""Transfer job ocid.""")
@cli_util.option('--appliance-label', required=True, help=u"""Appliance label.""")
@cli_util.option('--appliance-cert-fingerprint', required=True,
                 help=u"""The transfer appliance X.509/SSL certificate fingerprint.""")
@cli_util.option('--appliance-ip', required=True, help=u"""AThe IP address of the transfer appliance.""")
@cli_util.option('--appliance-port', required=False, type=click.INT, default=443, help=u"""Appliance label.""")
@cli_util.option('--profile', required=False, default="DEFAULT", help=u"""profile""")
@cli_util.option('--appliance-profile', required=False, default="DEFAULT", help=u"""Appliance profile""")
@cli_util.option('--access-token', required=False,
                 help=u"""the access token to authenticate with the transfer appliance.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={},
                                                      output_type={'module': 'dts', 'class': 'PhysicalAppliance'})
@cli_util.wrap_exceptions
def pa_initialize_authentication(ctx, from_json, job_id, appliance_label, appliance_cert_fingerprint, appliance_ip,
                                 appliance_port, access_token, profile, appliance_profile):
    if isinstance(job_id, six.string_types) and len(job_id.strip()) == 0:
        raise click.UsageError('Parameter --job-id cannot be whitespace or empty string')

    if isinstance(appliance_label, six.string_types) and len(appliance_label.strip()) == 0:
        raise click.UsageError('Parameter --appliance-label cannot be whitespace or empty string')

    # Do this for all the input arguments

    kwargs = {}

    click.echo("Retrieving the Appliance serial id from Oracle Cloud Infrastructure")
    # Get the Transfer Appliance serial number from the information received from CCP
    client = cli_util.build_client('transfer_appliance', ctx)
    result = client.get_transfer_appliance(
        id=job_id,
        transfer_appliance_label=appliance_label,
        **kwargs
    )
    serial_number = result.data.serial_number
    auth_spec = InitAuthSpec(cert_fingerprint=appliance_cert_fingerprint, appliance_ip=appliance_ip,
                             appliance_port=appliance_port, appliance_profile=appliance_profile,
                             serial_id=serial_number, access_token=access_token)

    init_auth = create_init_auth(auth_spec)
    init_auth.run()

    # The initialize-authentication shows the transfer appliance details the same as oci dts physical-appliance show
    appliance_client = create_appliance_client(ctx, appliance_profile)
    cli_util.render_response(appliance_client.get_physical_transfer_appliance(), ctx)


def create_init_auth(auth_spec):
    return InitAuth(auth_spec)


@physical_appliance_group.command('list', help=u"""Lists all appliances registered via initialize authentication.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={},
                                                      output_type={'module': 'dts', 'class': 'PhysicalAppliance'})
@cli_util.wrap_exceptions
def pa_list(ctx, from_json):
    result = []
    config_manager = ApplianceConfigManager(APPLIANCE_CONFIGS_BASE_DIR)
    for profile_name, config in config_manager.list_configs().items():
        result.append({
            ENDPOINT: config.get_appliance_url(),
            APPLIANCE_PROFILE: profile_name
        })
    cli_util.render(result, None, ctx)


@physical_appliance_group.command('unregister',
                                  help=u"""Unregister appliance registered via initialize authentication.""")
@cli_util.option('--appliance-profile', default="DEFAULT", required=False, help=u"""Appliance Profile""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def pa_unregister(ctx, from_json, appliance_profile):
    config_manager = ApplianceConfigManager(APPLIANCE_CONFIGS_BASE_DIR)
    config = config_manager.get_config(appliance_profile)
    if not click.confirm("Is it OK to unregister appliance with endpoint {}".format(config.get_appliance_url())):
        click.echo("Exiting...")
        sys.exit(-1)
    else:
        config_manager.delete_config(appliance_profile)
    click.echo("Unregistered the appliance")


@physical_appliance_group.command('configure-encryption',
                                  help=u"""Configures encryption on the transfer appliance.""")
@cli_util.option('--appliance-profile', required=False, default="DEFAULT", help=u"""Appliance Profile""")
@cli_util.option('--job-id', required=True, help=u"""Transfer job OCID.""")
@cli_util.option('--appliance-label', required=True, help=u"""Appliance label.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def pa_configure_encryption(ctx, from_json, appliance_profile, job_id, appliance_label):
    client = cli_util.build_client('transfer_appliance', ctx)
    result = client.get_transfer_appliance(
        id=job_id,
        transfer_appliance_label=appliance_label
    )
    # If the appliance is not already in a preparing state, move it to a preparing state
    if result.data.lifecycle_state != LIFECYCLE_STATE_PREPARING:
        click.echo("Moving the state of the appliance to preparing...")
        details = {
            "lifecycleState": LIFECYCLE_STATE_PREPARING
        }
        client.update_transfer_appliance(
            id=job_id,
            transfer_appliance_label=appliance_label,
            update_transfer_appliance_details=details,
        )

    click.echo("Passphrase being retrieved...")
    passphrase = client.get_transfer_appliance_encryption_passphrase(
        id=job_id,
        transfer_appliance_label=appliance_label
    ).data.encryption_passphrase
    appliance_client = create_appliance_client(ctx, appliance_profile)
    click.echo("Configuring encryption...")

    appliance_client.configure_encryption(passphrase_details={'passphrase': passphrase})
    click.echo("Encryption configured. Getting physical transfer appliance info...")
    appliance_info = appliance_client.get_physical_transfer_appliance()
    cli_util.render_response(appliance_info, ctx)


def create_appliance_client(ctx, appliance_profile):
    return ApplianceClientProxy(ctx, appliance_profile)


@physical_appliance_group.command('unlock',
                                  help=u"""Unlocks the transfer appliance.""")
@cli_util.option('--appliance-profile', required=False, default="DEFAULT", help=u"""Appliance Profile""")
@cli_util.option('--job-id', required=False, help=u"""Transfer job OCID.""")
@cli_util.option('--appliance-label', required=False, help=u"""Appliance label.""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def pa_unlock(ctx, from_json, appliance_profile, job_id, appliance_label):
    if job_id is None or appliance_label is None:
        click.echo("Specify the --job-id and the --appliance-label to retrieve the passphrase from Oracle Cloud"
                   "Infrastructure or enter the passphrase")
        passphrase = click.prompt('Passphrase', hide_input=True)
        if passphrase is None:
            click.echo('No input provided. Exiting...')
            sys.exit(-1)
    else:
        click.echo("Retrieving the passphrase from Oracle Cloud Infrastructure")
        client = cli_util.build_client('transfer_appliance', ctx)
        passphrase = client.get_transfer_appliance_encryption_passphrase(
            id=job_id,
            transfer_appliance_label=appliance_label
        ).data.encryption_passphrase
    appliance_client = create_appliance_client(ctx, appliance_profile)
    appliance_client.unlock_appliance(details={'passphrase': passphrase})
    cli_util.render_response(appliance_client.get_physical_transfer_appliance(), ctx)


@physical_appliance_group.command('show', help=u"""Shows transfer appliance details.""")
@cli_util.option('--appliance-profile', required=False, default="DEFAULT", help=u"""Appliance Profile""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def pa_show(ctx, from_json, appliance_profile):
    appliance_client = create_appliance_client(ctx, appliance_profile)
    appliance_info = appliance_client.get_physical_transfer_appliance()
    cli_util.render_response(appliance_info, ctx)


@physical_appliance_group.command('finalize', help=u"""Finalizes the appliance.""")
@cli_util.option('--appliance-profile', required=False, default="DEFAULT", help=u"""Appliance Profile""")
@cli_util.option('--job-id', required=True, help=u"""Transfer job OCID.""")
@cli_util.option('--appliance-label', required=True, help=u"""Appliance label.""")
@cli_util.option('--skip-upload-user-check', required=False, is_flag=True,
                 help=u"""Skip checking whether the upload user has the right credentials""")
@json_skeleton_utils.get_cli_json_input_option({})
@cli_util.help_option
@click.pass_context
@json_skeleton_utils.json_skeleton_generation_handler(input_params_to_complex_types={})
@cli_util.wrap_exceptions
def pa_finalize(ctx, from_json, appliance_profile, job_id, appliance_label, skip_upload_user_check):
    click.echo("Retrieving the upload summary object name from Oracle Cloud Infrastructure")
    client = cli_util.build_client('transfer_appliance', ctx)
    appliance_client = create_appliance_client(ctx, appliance_profile)

    upload_summary_obj_name = client.get_transfer_appliance(
        id=job_id,
        transfer_appliance_label=appliance_label
    ).data.upload_status_log_uri

    click.echo("Retrieving the upload bucket name from Oracle Cloud Infrastructure")
    client = cli_util.build_client('transfer_job', ctx)
    upload_bucket = client.get_transfer_job(id=job_id).data.upload_bucket_name

    if not skip_upload_user_check:
        click.echo("Validating the upload user credentials")
        validate_upload_user_credentials(ctx, upload_bucket)

    click.echo("Storing the upload user configuration and credentials on the transfer appliance")
    upload_user_config = oci_config.from_file(APPLIANCE_UPLOAD_USER_CONFIG_PATH)
    upload_user_key_file = open(os.path.expanduser(upload_user_config[KEY_FILE_KEY])).read()
    upload_config = {
        'uploadBucket': upload_bucket,
        'overwrite': False,
        'objectNamePrefix': "",
        'uploadSummaryObjectName': upload_summary_obj_name,
        'uploadUserOciConfig': open(APPLIANCE_UPLOAD_USER_CONFIG_PATH).read(),
        'uploadUserPrivateKeyPem': upload_user_key_file
    }
    appliance_client.set_object_storage_upload_config(upload_config=upload_config)

    click.echo("Finalizing the transfer appliance...")
    appliance_client.finalize_appliance()
    appliance_info = appliance_client.get_physical_transfer_appliance()

    click.echo("The transfer appliance is locked after finalize. Hence the finalize status will be shown as NA. "
               "Please unlock the transfer appliance again to see the correct finalize status")
    cli_util.render_response(appliance_info, ctx)


def validate_upload_user_credentials(ctx, upload_bucket):
    """
    There are two users, the admin user and the upload user
    The admin user is the one who has access to the user's tenancy and can perform operations like creating a job,
    requesting an appliance, etc.
    The upload user has enough permissions to just upload data to a particular user bucket. The upload user cannot
    delete objects from the bucket nor can it make modifications to the bucket or account. In essence it is a
    restricted user.
    The upload user is defined in ~/.oci/config_upload_user under the [DEFAULT] section. There is no way to change
    the file and the section. These are standards that are expected
    The idea of validation is to check whether the upload user has the ability to create objects, inspect the object
    and read the object's meta data from Oracle Cloud Infrastructure
    The procedure is this:
    1. Admin user tries to get the test object and delete it if it is present.
      - This is more of an error check when there is a stale object present from a previous failed run
      - Only the admin user, NOT the upload user, can delete an object
    2. Upload user creates the test object
    3. Upload user overwrites the test object
    4. Upload user gets the checksum of the test object
    5. Upload user gets the metadata of the test bucket
    6. Admin user deletes the test object
    :param upload_bucket: The bucket to upload to
    :return: None
    """
    admin_user = oci_config.from_file(ctx.obj['config_file'])['user']
    # Overriding any endpoint that was set. Need to get to the endpoint based on the config file, not based on the
    # override parameter
    ctx.endpoint = None
    ctx.obj['endpoint'] = None
    object_storage_admin_client = cli_util.build_client('object_storage', ctx)
    # A bit hacky but gets the job done. Only two parameters need to be changed to get the upload user context,
    # the profile and the config file. All other parameters remain the same
    upload_user_ctx = ctx
    upload_user_ctx.obj['profile'] = 'DEFAULT'
    upload_user_ctx.obj['config_file'] = APPLIANCE_UPLOAD_USER_CONFIG_PATH
    # Overriding any endpoint that was set. Need to get to the endpoint based on the config_upload_user file
    upload_user_ctx.endpoint = None
    object_storage_upload_client = cli_util.build_client('object_storage', upload_user_ctx)

    namespace = object_storage_admin_client.get_namespace().data
    try:
        try:
            object_storage_admin_client.head_object(namespace, upload_bucket, TEST_OBJECT)
            click.echo("Found test object in bucket. Deleting  it...")
            object_storage_admin_client.delete_object(namespace, upload_bucket, TEST_OBJECT)
        except exceptions.ServiceError as se:
            if se.status != 404:
                raise se
    except Exception as e:
        raise exceptions.RequestException(
            "Admin user {} failed to delete the test object {}: {}".format(admin_user, TEST_OBJECT, str(e)))

    test_object_content = "Bulk Data Transfer Test"

    operation = None
    test_object_exists = False
    try:
        operation = "Create object {} in bucket {} using upload user".format(TEST_OBJECT, upload_bucket)
        object_storage_upload_client.put_object(namespace, upload_bucket, TEST_OBJECT, test_object_content)
        click.echo(operation)
        test_object_exists = True

        operation = "Overwrite object {} in bucket {} using upload user".format(TEST_OBJECT, upload_bucket)
        object_storage_upload_client.put_object(namespace, upload_bucket, TEST_OBJECT, test_object_content)
        click.echo(operation)

        operation = "Inspect object {} in bucket {} using upload user".format(TEST_OBJECT, upload_bucket)
        object_storage_upload_client.head_object(namespace, upload_bucket, TEST_OBJECT)
        click.echo(operation)

        operation = "Read bucket metadata {} using upload user".format(upload_bucket)
        metadata = object_storage_upload_client.get_bucket(namespace, upload_bucket).data.metadata
        click.echo(operation)
    except exceptions.ServiceError as se:
        raise exceptions.RequestException(
            "Failed to {} in tenancy {} as upload user: {}".format(operation, namespace, se.message))
    finally:
        if test_object_exists:
            try:
                object_storage_admin_client.delete_object(namespace, upload_bucket, TEST_OBJECT)
            except exceptions.ServiceError as se:
                raise exceptions.ServiceError(
                    "Failed to delete test object {} as admin user {}: {}".format(TEST_OBJECT, admin_user, se.message))
