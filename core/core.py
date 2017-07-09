import os

import boto3
import botocore


# The CloudFormation client to create, update and delete stack
cf = boto3.client('cloudformation')


def _stack_exists(stack_name):
    """ Checks if the stack exists.
    Returns True if it exists and False if not.
    """
    exists = False
    try:
        cf.describe_stacks(StackName=stack_name)
        exists = True
    except botocore.exceptions.ClientError as ex:
        if ex.response['Error']['Code'] == 'ValidationError':
            exists = False
        else:
            raise
    return exists


def create_stack(stack_name, template):
    """ Creates the stack given the template. """
    if _stack_exists(stack_name):
        raise Exception("Stack exists, stack_name=%s" % stack_name)
    resp = cf.create_stack(StackName=stack_name, TemplateBody=template)
    return resp['StackId']


def update_stack(stack_name, template):
    """ Updates the stack with the updated template. """
    if not _stack_exists(stack_name):
        raise Exception("Stack does not exists, stack_name=%s" % stack_name)
    resp = cf.update_stack(StackName=stack_name, TemplateBody=template)
    return resp['StackId']


def delete_stack(stack_name):
    """ Deletes the stack. """
    cf.delete_stack(StackName=stack_name)
