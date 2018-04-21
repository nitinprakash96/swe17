from cloudant.client import Cloudant

#conn = None

def create():
	global conn
	cloudant_user = "956570a2-4054-4fee-8dc6-bb699d1022d3-bluemix"
	cloudant_pass = "e1d8852c83e0cf2201b54ff7401058db52fa85f6d6fed8a9c2b2659ff66ff9cd"
	cloudant_url = "https://956570a2-4054-4fee-8dc6-bb699d1022d3-bluemix:e1d8852c83e0cf2201b54ff7401058db52fa85f6d6fed8a9c2b2659ff66ff9cd@956570a2-4054-4fee-8dc6-bb699d1022d3-bluemix.cloudant.com"

	client = Cloudant(cloudant_user, cloudant_pass, url=cloudant_url, connect=True, auto_renew=True)
	return client

def close():
	conn.close()
