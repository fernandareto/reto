from turtle import update
from unicodedata import name
from urllib import response
from mysqlx import Session
import boto3
from botocore.exceptions import ClientError
import json

#create service s3 with boto3:

#s3client=boto3.client('s3', region_name ='eu-west-1')
#s3client.create_bucket(Bucket="pruebafernanda",CreateBucketConfiguration={'LocationConstraint':'eu-west-1'})
#response= s3client.list_buckets()
#print(response)

#create service EC2 with boto3

#def create_ec2_instance():
 #   try:
  #      print("creating EC2 instance")
   #     ec2instance =boto3.client('ec2')
    #    ec2instance.run_instances(
     #       ImageId="ami-033b95fb8079dc481", #acá coloco que imagen quiero en mi maquina, en este caso linux 64 bits se toma de aws
      #      MinCount=1,
       #     MaxCount=1,
        #    InstanceType="t2.micro", #Acá coloco las especificaciones de software que quiero quetenga mi maquina (ram,memoria)
         #   KeyName ="keyprueba"
        #)
    #except Exception as e:
     #   print(e)

#create_ec2_instance()

#def describe_ec2_instance():
 #   try:
  #      print("describe EC2 instance")
   #     ec2instance =boto3.client('ec2')
    #    print(ec2instance.describe_instances(InstanceIds=['i-0cebe7074a148dbd3']))
     #   print('vpc')
      #  print (ec2instance.describe_vpcs())
   # except Exception as e:
    #    print(e)

#descripcion=describe_ec2_instance()


class CreateInstanceEC2(object):
    def __init__(self, ec2_client):
        self.ec2_client = ec2_client

    def grep_vpc_subnet_id(self):
        response = self.ec2_client.describe_vpcs()
        if len(response['Vpcs']) == 1:
            vpc_id = response['Vpcs'][0]['VpcId']
        print(vpc_id)

        response = self.ec2_client.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
        subnet_id = response["Subnets"][0]["SubnetId"]
        print("The Default Subnet : ", subnet_id)
        return vpc_id, subnet_id
        print(vpc_id,subnet_id)
        
    def create_security_group(self):
        sg_name = "awspy_security_group"
        try:
            vpc_id, subnet_id = self.grep_vpc_subnet_id()
            response = self.ec2_client.create_security_group(
                GroupName=sg_name,
                Description="This is created using python",
                VpcId=vpc_id
            )
            sg_id = response["GroupId"]
            print(sg_id)
            sg_config = self.ec2_client.authorize_security_group_ingress(
                GroupId=sg_id,
                IpPermissions=[
                    {
                        'IpProtocol':'tcp',
                        'FromPort':22,
                        'ToPort': 22,
                        'IpRanges':[{'CidrIp':'0.0.0.0/0'}]
                    }
                ]
            )
            print(sg_config)
            return sg_id, sg_name
        except Exception as e:
            if str(e).__contains__("already exists"):
                response = self.ec2_client.describe_security_groups(GroupNames=[sg_name])
                sg_id = response["SecurityGroups"][0]["GroupId"]
                print(sg_id, sg_name)
                return sg_id, sg_name
    

    def create_ec2_instance(self):
        """
        MaxCount=1, # Keep the max count to 1, unless you have a requirement to increase it
        InstanceType="t2.micro", # Change it as per your need, But use the Free tier one
        KeyName="ec2-key" # Change it to the name of the key you have.
        :return: Creates the EC2 instance.
        """
        print("Creating EC2 instance")
        sg_id, sg_name = self.create_security_group()
        vpc_id, subnet_id = self.grep_vpc_subnet_id()
        self.ec2_client.run_instances(
            ImageId="ami-033b95fb8079dc481",
            MinCount=1,
            MaxCount=1,
            InstanceType="t2.micro",
            KeyName="keyprueba",
            SecurityGroupIds=[sg_id],
            SubnetId=subnet_id,
        )    


#try:
#    ec2_client = boto3.client('ec2')
#    call_obj = CreateInstanceEC2(ec2_client)
#    call_obj.grep_vpc_subnet_id()
#    call_obj.create_security_group()
#    call_obj.create_ec2_instance()
#except ClientError as e:
#    print("There is a error in the client configuration: ", e)

clientcommit = boto3.client('codecommit') #create repository code commit

def createrepository(name,description):
    repositorio = clientcommit.create_repository(
        repositoryName=name,
        repositoryDescription=description
    )
    return repositorio


#createrepository('fernandarepo','ismyfirstrepo')

#def create_branch (namerepo, ranmerame):
 #   repositorio = clientcommit.create_branch ( 
  #  repositoryName = namerepo , 
   # branchName = ranmerame , 
    #commitId= '123'
   
    #)
    #return repositorio
    #print (repositorio)
#create_branch('nuevoname','rama')

#response = clientcommit.update_repository_description(
 #   repositoryName='nuevoname',
  #  repositoryDescription='hola'
#)

#resp = clientcommit.create_commit(
 #           repositoryName='nuevoname',
  #          branchName='master',
   #         authorName='fer',
    #)

def update_name_repo(name,newname):
    repositorio =''
    try:
        repositorio = clientcommit.update_repository_name(
        oldName=name,
        newName=newname
        )   
    except Exception as e:
        print ('yaseactualizo')
    
    return repositorio

ipdate=update_name_repo('repositorio','test')
print (update)