"use strict";
const pulumi = require("@pulumi/pulumi");
const aws = require("@pulumi/aws");
const awsx = require("@pulumi/awsx");

const name_base = "kafka-play";
const vpc_cidr = "10.0.0.0/16";
const reg = "us-east-2";
const az1 = reg+"a";
const az2 = reg+"b";
const ubuntu_ami = "ami-0b51ab7c28f4bf5a6";  // being lazy and hard coding AMI from Ohio
const ssh_key = "mitch-ohio-ssh";  // predefined key laziness

let kpvpc = new awsx.ec2.Vpc(name_base, {
    cidrBlock : vpc_cidr,
    subnets: [ 
        {type: "public"},
        {type: "private"}
    ],
    numberOfNatGateways: 0,
    tags: { "Name": name_base }
});

// Allocate a security group and then a series of rules:
let mysg = new awsx.ec2.SecurityGroup(name_base+"-sg", { vpc: kpvpc });

// 1) inbound SSH traffic on port 22 from a specific IP address
mysg.createIngressRule("ssh-access", {
    location: new awsx.ec2.AnyIPv4Location(),    
    ports: new awsx.ec2.TcpPorts(22),
    description: "allow SSH access from anywhere",
});

// 2) inbound HTTPS traffic on port 443 from anywhere
mysg.createIngressRule("https-access", {
    location: new awsx.ec2.AnyIPv4Location(),
    ports: new awsx.ec2.TcpPorts(443),
    description: "allow HTTPS access from anywhere",
});

// 3) outbound TCP traffic on any port to anywhere
mysg.createEgressRule("outbound-access", {
    location: new awsx.ec2.AnyIPv4Location(),
    ports: new awsx.ec2.AllTcpPorts(),
    description: "allow outbound access to anywhere",
});

let az1_pub_subnet = pulumi.output(kpvpc.publicSubnetIds.then(ids => ids[0])) 
let az2_pub_subnet = pulumi.output(kpvpc.publicSubnetIds.then(ids => ids[1])) 
let az1_priv_subnet = pulumi.output(kpvpc.privateSubnetIds.then(ids => ids[0])) 
let az2_priv_subnet = pulumi.output(kpvpc.privateSubnetIds.then(ids => ids[1]))


// Build producer/consumer VM in public subnet so it's easily accessible
let prodcon = new aws.ec2.Instance(name_base+"-prodcon", {
    ami: ubuntu_ami,
    instanceType: "t3.micro",
    associatePublicIpAddress: true,
    availabilityZone: az1,
    subnetId: az1_pub_subnet,
    vpcSecurityGroupIds: [mysg.id],
    keyName: ssh_key,
    tags: {
        "Name": name_base+"-prodcon",
    },
});

// This is temporary for testing things.
let privtest = new aws.ec2.Instance(name_base+"-privtest", {
    ami: ubuntu_ami,
    instanceType: "t3.micro",
    associatePublicIpAddress: false,
    availabilityZone: az2,
    subnetId: az2_priv_subnet,
    keyName: ssh_key,
    tags: {
        "Name": name_base+"-privtest",
    },
});

const msk_cfg = new aws.msk.Configuration("msk_cfg", {
    serverProperties: 'auto.create.topics.enable = true',
});

const quakes_msk = new aws.msk.Cluster("quakes", {
    clusterName: "quakes",
    kafkaVersion: "2.2.1",
    configurationInfo: msk_cfg,
    numberOfBrokerNodes: 2,
    brokerNodeGroupInfo: {
        instanceType: "kafka.t3.small",
        ebsVolumeSize: 50,
        clientSubnets: [
            az1_priv_subnet,
            az2_priv_subnet
        ],
        securityGroups: [mysg.id],
    },
    tags: {
        Name: "quakes",
    },
});

// Export a few resulting fields to make them easy to use:
exports.vpcId = kpvpc.id;
exports.vpcPrivateSubnetIds = kpvpc.privateSubnetIds
exports.vpcPublicSubnetIds = kpvpc.publicSubnetIds
exports.zookeeperConnectString = quakes_msk.zookeeperConnectString;
exports.bootstrapBrokers = quakes_msk.bootstrapBrokers;
exports.bootstrapBrokersTls = quakes_msk.bootstrapBrokersTls;