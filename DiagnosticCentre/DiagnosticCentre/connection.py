from cloudant.client import Cloudant

def create():
	cloudant_user = "f95c6130-1964-448c-a8d7-257d80b30e65-bluemix"
	cloudant_pass = "9aabf072adfc481b889e322f7824c79b4c517eb187a447bf7fba90120b278c1d"
	cloudant_url = "https://f95c6130-1964-448c-a8d7-257d80b30e65-bluemix:9aabf072adfc481b889e322f7824c79b4c517eb187a447bf7fba90120b278c1d@f95c6130-1964-448c-a8d7-257d80b30e65-bluemix.cloudant.com"
	client = Cloudant(cloudant_user, cloudant_pass, url=cloudant_url, connect=True, auto_renew=True)
	return client
