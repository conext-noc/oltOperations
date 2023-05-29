####################             IN MAINTANCE             ####################

# import os
# from dotenv import load_dotenv
# import boto3
# from botocore.exceptions import NoCredentialsError

# load_dotenv()


# def get_health_status(environment_name):
#     data = {"Ops-env": {}, "Ins-env": {}, "Sch-env": {}, "Mod-env": {}, "Mod-env": {}}
#     envs = ["Ops-env", "Ins-env", "Sch-env", "Mod-env", "Mon-env"]
#     try:
#         # Create a session using your AWS access key and secret access key
#         session = boto3.Session(
#             aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
#             aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
#         )

#         # Create an AWS Elastic Beanstalk client
#         eb_client = session.client("elasticbeanstalk")

#         # Get information about the environment
#         for idx, environment in enumerate(envs):
#             eb_envs = eb_client.describe_environments(EnvironmentNames=[environment])
#             if len(eb_envs["Environments"]) == 0:
#                 data[environment] = None
#             else:
#                 response = eb_envs["Environments"][0]
#                 data[environment]["health"] = (
#                     response["HealthStatus"]
#                     if "HealthStatus" in response
#                     else response["Health"]
#                 )
#                 data[environment]["application"] = response["ApplicationName"]
#                 data[environment]["version"] = response["VersionLabel"]
#                 data[environment]["status"] = response["Status"]
#         return data

#     except NoCredentialsError:
#         print(
#             """Unable to locate AWS credentials.
#             Make sure you have valid AWS access key and secret access key."""
#         )
#         return None


# # Replace 'your-environment-name' with the actual name of your Elastic Beanstalk environment
# environment_name = "Ops-env"

# # Get the health status of the Elastic Beanstalk instance
# status = get_health_status(environment_name)

# if status:
#     print(f"The health status of the environment '{environment_name}' is: {status}")

####################             IN MAINTANCE             ####################


####################             DATA PARSER ODOO             ####################

# from tkinter import filedialog
# from helpers.fileFormatters.fileHandler import dictToFile, fileToDict

# def compare():
#   fileOLT = "./DATA_DE_CLIENTES_OLT.xlsx"
#   fileODOO = "./DATA_DE_CLIENTES_ODOO.xlsx"
#   olt = fileToDict(fileOLT, "E")
#   odoo = fileToDict(fileODOO, "E")
#   print(olt[0])
#   print(odoo[0])
#   client = []
#   for odooClient in odoo:
#     for oltClient in olt:
#       if oltClient["sn"] == odooClient["Serial del ONT"]:
#         client.append({
#           "fsp":f'{oltClient["frame"]}/{oltClient["slot"]}/{oltClient["port"]}',
#           "frame":oltClient["frame"],
#           "slot":oltClient["slot"],
#           "port":oltClient["port"],
#           "onu_id":oltClient["onu_id"],
#           "name":odooClient["Cliente"],
#           "contract": str(odooClient["Referencia"]).zfill(10),
#           "sn":oltClient["sn"],
#           "device":oltClient["device"],
#           "ID externo": odooClient["ID.1"],
#           "state":oltClient["state"],
#           "olt": "1",
#           "plan_name":oltClient["plan_name"]
#         })
#   print("Selecciona la carpeta de resultados...")
#   path = filedialog.askdirectory()
#   dictToFile("RESULTADO", "E", path, client, False)
# compare()

####################             DATA PARSER ODOO             ####################

####################             SMART OLT REQUESTS             ####################

# import requests

# sub_domain = "conext"
# api_key="6125bdf043c44912847385f9e62ee42d"


# def activate_batch():
#   url = f"https://{sub_domain}.smartolt.com/api/onu/bulk_enable"
#   payload={
#     "onus_external_ids":"9876543210"
#   }
#   headers = {
#     'X-Token': f'{api_key}'
#   }
#   response = requests.request("POST", url, headers=headers, data=payload, files=[])
#   print(response.text)

# # activate_batch()

# def deactivate_batch():
#   url = f"https://{sub_domain}.smartolt.com/api/onu/bulk_disable"
#   payload={
#     "onus_external_ids":"9876543210"
#   }
#   headers = {
#     'X-Token': f'{api_key}'
#   }
#   response = requests.request("POST", url, headers=headers, data=payload, files=[])
#   print(response.text)

# deactivate_batch()

####################             SMART OLT REQUESTS             ####################
