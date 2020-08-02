'''
Builds a system in AWS with which the kafka producers and consumers can be used.
Some key assets:
- MSK - This is AWS' kafka-based streaming service
- kafka client instance - This is an EC2 instance where the producer and consumer will be run.
- RDS (Postgres) - RDS DB running Postgres. (Because the original kafka code was written to push data into Postgres.)
'''

import pulumi
import pulumi_aws as aws

name_base = "kafka-play"
vpc_cidr = "10.0.0.0/16"
az1_subnet_cidr = "10.0.1.0/24"
az2_subnet_cidr = "10.0.2.0/24"

reg = "us-east-2"
az1 = reg+"a"
az1 = reg+"b"
ubuntu_ami = "ami-0b51ab7c28f4bf5a6" # being lazy for now and hardcoding Ohio Ubuntu 18.04 ami from Canonical

# Custom provider based on settings above
region = aws.Provider(reg, region=reg)

# VPC for the stack
vpc = aws.ec2.Vpc(name_base+"-vpc", 
    cidr_block=vpc_cidr,
    tags={"Name":name_base+"-vpc"})

gw = aws.ec2.InternetGateway(name_base+"-gw",
    tags={
        "Name": name_base+"-gw"
    },
    vpc_id=vpc.id)

    routes=[
        {
            "cidr_block": vpc_cidr,
            "gateway_id": gw.id
        },
    ],
    tags={
        "Name": name_base+"-rt"
    },
    vpc_id=vpc.id)
    
# Subnets for the stack. MSK has to be deployed across at least two AZs and so two subnets are created.
az1_subnet = aws.ec2.Subnet(name_base+"-subnet-1",
    cidr_block=az1_subnet_cidr,
    tags={
        "Name": name_base+"-subnet-1",
    },
    vpc_id=vpc.id)

az2_subnet = aws.ec2.Subnet(name_base+"-subnet-2",
    cidr_block=az2_subnet_cidr,
    tags={
        "Name": name_base+"-subnet-2",
    },
    vpc_id=vpc.id)

sec_grp = aws.ec2.SecurityGroup(name_base+"-sg",
    vpc_id=vpc.id)

sec_grp_ssh_rule = aws.ec2.SecurityGroupRule(name_base+"-ssh",
    type="ingress",
    from_port=22,
    to_port=22,
    protocol="tcp",
    cidr_blocks=["0.0.0.0/0"],
    security_group_id=sec_grp.id)


# Build the MSK cluster
# TBD

# Build the RDS Postgres
# TBD

# Build the producer/consumer machine
# small VM, git clone this repo for the consumer/producer code
# may have to install python3 and stuff ...
# Start up the producer and consumer ....
prod_con = aws.ec2.Instance(name_base+"-prodcon",
    ami=ubuntu_ami,
    instance_type="t3.micro",
    tags={
        "Name": name_base+"-prodcon",
    },
    subnet_id=az1_subnet.id,
    vpc_security_group_ids=[sec_grp.id])