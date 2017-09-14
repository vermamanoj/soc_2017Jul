#!/usr/bin/env python3


import logging
import os
import sys
from configparser import ConfigParser

import boto3
from django.http import JsonResponse
from django.shortcuts import render, redirect

from gentelella.core import global_config

logger = logging.getLogger('root')
FORMAT = "[%(filename)s:%(lineno)s-%(funcName)s] %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)


def index(request):
    return render(request, 'aws2.html')


def get_insecure_instances(request):
    return render(request, 'aws2.html')


def insecure_instance_acl_old(request):
    conf = get_aws_config()
    if 'error' in conf.keys():
        return {
            "outcome": "error",
            "error": "configuration does not exist",
        }
    ec2 = boto3.resource('ec2',
                         aws_access_key_id=conf['success']['akey'],
                         aws_secret_access_key=conf['success']['skey'],
                         # region =  conf['success']['region'],
                         )
    ec2_list = []

    for i in ec2.instances.all():
        # i = ec2.Instance('i-0ab3170d8d452bb8c')
        # if True:
        unsecure_instance = False
        instance_dict = {}

        if i.state['Name'] == 'running':

            instance_name = i.tags[0]['Value']
            instance_dict['instance_name'] = instance_name
            for security_group in i.security_groups:

                group_id = security_group['GroupId']
                sg = ec2.SecurityGroup(group_id)
                instance_dict['security_group_name'] = sg.group_name
                instance_dict['security_group_description'] = sg.description

                port_list = []
                for acl in sg.ip_permissions:

                    for iprange in acl['IpRanges']:
                        if iprange['CidrIp'] == '0.0.0.0/0':
                            port_list.append(acl['ToPort'])
                            unsecure_instance = True
                instance_dict['port_list'] = port_list
        if unsecure_instance:
            ec2_list.append(instance_dict)

    for x in ec2_list:
        print(x)
    result = {
        "outcome": "success",
        "success": ec2_list
    }
    return JsonResponse(result, safe=False)


def insecure_instance_acl_json(request):
    conf = get_aws_config()
    if 'error' in conf.keys():
        return {
            "outcome": "error",
            "error": "configuration does not exist",
        }
    try:
        ec2 = boto3.resource('ec2',
                             aws_access_key_id=conf['success']['akey'],
                             aws_secret_access_key=conf['success']['skey'],
                             # region=conf['success']['region'],
                             )

        ec2_list = []

        for i in ec2.instances.all():
            # i = ec2.Instance('i-0ab3170d8d452bb8c')
            # if True:
            unsecure_instance = "False"
            instance_dict = {}

            if i.state['Name'] == 'running':

                instance_name = i.tags[0]['Value']
                instance_dict['instance_name'] = instance_name
                instance_dict['instance_id'] = i.instance_id
                for security_group in i.security_groups:

                    group_id = security_group['GroupId']
                    sg = ec2.SecurityGroup(group_id)
                    instance_dict['security_group_name'] = sg.group_name
                    instance_dict['security_group_description'] = sg.description

                    acl_list = []

                    for acl in sg.ip_permissions:
                        acl_dict = {}
                        acl_dict['insecure'] = "False"

                        if acl['IpProtocol'] == '-1':
                            acl_dict['toport'] = "All traffic"
                        else:
                            acl_dict['toport'] = acl['ToPort']
                        print(acl)
                        for iprange in acl['IpRanges']:
                            acl_dict['iprange'] = iprange['CidrIp']
                            if iprange['CidrIp'] == '0.0.0.0/0':
                                acl_dict['insecure'] = "True"
                                instance_dict['insecure'] = "True"


                        acl_list.append(acl_dict)

                    instance_dict['acl_list'] = acl_list
                ec2_list.append(instance_dict)

        for x in ec2_list:
            print(x)
        result = {
            "outcome": "success",
            "success": ec2_list
        }
        return JsonResponse(result, safe=False)
    except Exception as e:
        logger.error(e)
        raise
        error = {
            "outcome": "error",
            "error": "server internal error",
        }
        return JsonResponse(error)


def config(request):
    conf = get_aws_config()
    if "success" in conf['outcome']:
        result = {
            "outcome": "success",
            "success": "Configuration exists"
        }
        return JsonResponse(result)


def get_instance_acl(request, instance_id=None):
    url = '/aws/get_instance_acl_json/' + instance_id
    return render(request, 'aws_instance_details.html', {"url": url})


def get_instance_acl_json(request, instance_id=None):
    conf = get_aws_config()
    if 'error' in conf.keys():
        return {
            "outcome": "error",
            "error": "configuration does not exist",
        }
    ec2 = boto3.resource('ec2',
                         aws_access_key_id=conf['success']['akey'],
                         aws_secret_access_key=conf['success']['skey'],
                         # region=conf['success']['region'],
                         )
    ec2_list = []
    if instance_id == None:
        result = {
            "outcome": "error",
            "error": "instance_id missing"
        }
        return JsonResponse(result, safe=False)

    i = ec2.Instance(instance_id)
    if True:
        unsecure_instance = "False"
        instance_dict = {}

        if i.state['Name'] == 'running':

            instance_name = i.tags[0]['Value']
            instance_dict['instance_name'] = instance_name
            for security_group in i.security_groups:

                group_id = security_group['GroupId']
                sg = ec2.SecurityGroup(group_id)
                instance_dict['security_group_name'] = sg.group_name
                instance_dict['security_group_description'] = sg.description

                acl_list = []

                for acl in sg.ip_permissions:
                    acl_dict = {}
                    acl_dict['insecure'] = "False"

                    if acl['IpProtocol'] == '-1':
                        acl_dict['toport'] = "All traffic"
                    else:
                        acl_dict['toport'] = acl['ToPort']
                    if len(acl['IpRanges']) > 0:
                        acl_dict['iprange'] = acl['IpRanges'][0]['CidrIp']

                        if acl['IpRanges'][0]['CidrIp'] == '0.0.0.0/0':
                            acl_dict['insecure'] = "True"
                            instance_dict['insecure'] = "True"

                    acl_list.append(acl_dict)

                instance_dict['acl_list'] = acl_list
            ec2_list.append(instance_dict)

    for x in ec2_list:
        print(x)
    result = {
        "outcome": "success",
        "success": ec2_list
    }
    return JsonResponse(result, safe=False)


def send_email(request):
    aws_send_email(request)
    result = {
        "outcome": "success",
        "success": "Email successfully sent"
    }
    return JsonResponse(result)


def aws_send_email(request):
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    sender = "manojver@hcl.com"

    # Replace recipient@example.com with a "To" address. If your account
    # is still in the sandbox, this address must be verified.
    recipient = "manojver@hcl.com"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    awsregion = "us-east-1"

    # The subject line for the email.
    subject = "SOC notification - insecure AWS instance"

    # The HTML body of the email.
    htmlbody = """<h1>SOC notification - insecure AWS instance</h1><p>Your instance is insecure</p>"""

    # The email body for recipients with non-HTML email clients.
    textbody = "SOC notification - insecure AWS instance"

    # The character encoding for the email.
    charset = "UTF-8"

    # Create a new SES resource and specify a region.
    conf = get_aws_config()
    if 'error' in conf.keys():
        return {
            "outcome": "error",
            "error": "configuration does not exist",
        }
    client = boto3.client('ses',
                          aws_access_key_id=conf['success']['akey'],
                          aws_secret_access_key=conf['success']['skey'],
                          # region=conf['success']['region'],
                          )
    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': charset,
                        'Data': htmlbody,
                    },
                    'Text': {
                        'Charset': charset,
                        'Data': textbody,
                    },
                },
                'Subject': {
                    'Charset': charset,
                    'Data': subject,
                },
            },
            Source=sender,
        )
    # Display an error if something goes wrong.
    except Exception as e:
        logger.error("Error: ", e)
    else:
        print(response)
    result = {
        "outcome": "success",
        "success": response
    }
    return JsonResponse(result)


def secure_acl(request, instance_id=None):
    conf = get_aws_config()
    if 'error' in conf.keys():
        return {
            "outcome": "error",
            "error": "configuration does not exist",
        }
    ec2 = boto3.resource('ec2',
                         aws_access_key_id=conf['success']['akey'],
                         aws_secret_access_key=conf['success']['skey'],
                         # region=conf['success']['region'],
                         )

    ec2c = boto3.client('ec2',
                        aws_access_key_id=conf['success']['akey'],
                        aws_secret_access_key=conf['success']['skey'],
                        # region=conf['success']['region'],
                        )

    i = ec2.Instance(instance_id)
    for security_group in i.security_groups:
        group_id = security_group['GroupId']
        sg = ec2.SecurityGroup(group_id)
        for acl in sg.ip_permissions:
            if acl['IpRanges'][0]['CidrIp'] == '0.0.0.0/0':
                revoke = ec2c.revoke_security_group_ingress(
                    GroupId='sg-9a7917eb',
                    IpPermissions=[acl]
                )

                logger.info("Machine name")
                logger.info(i.tags[0]['Value'])
                logger.info("Security group")
                logger.info(group_id)
                acl['IpRanges'][0]['CidrIp'] = '172.16.0.0/24'
                data = ec2c.authorize_security_group_ingress(
                    GroupId=group_id,
                    IpPermissions=[acl]
                )
    print(data)
    url = '/aws/get_instance_acl/' + instance_id
    return redirect(url)

    return JsonResponse(request)


def config(request):
    conf = get_aws_config()
    if "success" in conf['outcome']:
        result = {
            "outcome": "success",
            "success": {
                "akey": conf['success']['akey'],
                # "region" : conf['success']['region'],
            }
        }
        return JsonResponse(result)


def get_aws_config():
    # The function does not take any input

    # The variable snow_config_exists is used to verify if config was read properly or not
    # and its used to return error message if it remains False
    aws_config_exists = 0

    # Call get_global_config function to read name and path of  credentials file
    global_configuration = global_config.get_global_config()

    if global_configuration['outcome'] == 'success':
        configFile = global_configuration['data']['credentials_file']

        try:
            if os.path.exists(configFile):
                config = ConfigParser()
                config.read(r'./config/config.ini')
                print(config)

                if 'aws' in config.sections():
                    akey = config['aws']['access_key']
                    skey = config['aws']['secret_key']
                    region = config['aws']['region']
                    result = {
                        "outcome": "success",
                        "success": {"akey": akey, "skey": skey, "region": region}
                    }
                    aws_config_exists = 1
                    return result

        except:
            logger.error(sys.exc_info())

    if aws_config_exists == 0:
        result = {
            "outcome": "error",
            "error": "Configuration does not exist"
        }
        return result
