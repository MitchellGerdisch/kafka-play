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

let myvpc = new awsx.ec2.Vpc(name_base, {
    cidrBlock : vpc_cidr,
    subnets: [ 
        {type: "public"},
        {type: "private"}
    ],
    numberOfNatGateways: 0,
    tags: { "Name": name_base }
});

// Allocate a security group and then a series of rules:
let mysg = new awsx.ec2.SecurityGroup(name_base+"-sg", { myvpc }, {dependsOn: [myvpc]});

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

// Build producer/consumer VM in public subnet so it's easily accessible
let prodcon = new aws.ec2.Instance(name_base+"-prodcon", {
    ami: ubuntu_ami,
    instanceType: "t3.micro",
    associatePublicIpAddress: true,
    availabilityZone: az1,
    subnetId: myvpc.publicSubnetIds[0],
    vpcSecurityGroupIds: [mysg.id],
    keyName: ssh_key,
    tags: {
        "Name": name_base+"-prodcon",
    },
}, {dependsOn: [myvpc, mysg]});

let privtest = new aws.ec2.Instance(name_base+"-privtest", {
    ami: ubuntu_ami,
    instanceType: "t3.micro",
    availabilityZone: az1,
    subnetId: myvpc.privateSubnetIds[0],
    keyName: ssh_key,
    tags: {
        "Name": name_base+"-privtest",
    },
}, {dependsOn: [myvpc, mysg]});

// Export a few resulting fields to make them easy to use:
exports.vpcId = myvpc.id;
exports.vpcPrivateSubnetIds = myvpc.privateSubnetIds;
exports.vpcPublicSubnetIds = myvpc.publicSubnetIds;