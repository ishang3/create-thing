"""
This application uses AWS iot pragmatically create
a new thing. It also downloads the necessary
certificates and keys.

"""



import boto3
import json
thingArn = ''
thingId = ''

thingName = 'pragmatictest'
defaultPolicyName = 'edXPolicy'

class CreateThing():

	def __init__(self):
		self.thingClient = boto3.client('iot')
		self.policyname = 'edXPolicy'

	def createThing(self,thingName='pragmatictest',policyname='edXPolicy'):
		thingResponse = self.thingClient.create_thing(
			thingName=thingName
		)
		print(thingResponse)
		data = json.loads(json.dumps(thingResponse, sort_keys=False, indent=4))
		for element in data:
			print(element)
			if element == 'thingArn':
				thingArn = data['thingArn']
			elif element == 'thingId':
				thingId = data['thingId']

		self.createCertificate()

	def createCertificate(self):
		certResponse = self.thingClient.create_keys_and_certificate(
			setAsActive=True
		)
		data = json.loads(json.dumps(certResponse, sort_keys=False, indent=4))
		for element in data:
			if element == 'certificateArn':
				certificateArn = data['certificateArn']
			elif element == 'keyPair':
				PublicKey = data['keyPair']['PublicKey']
				PrivateKey = data['keyPair']['PrivateKey']
			elif element == 'certificatePem':
				certificatePem = data['certificatePem']
			elif element == 'certificateId':
				certificateId = data['certificateId']

		with open('public.key', 'w') as outfile:
			outfile.write(PublicKey)
		with open('private.key', 'w') as outfile:
			outfile.write(PrivateKey)
		with open('cert.pem', 'w') as outfile:
			outfile.write(certificatePem)

		response = self.thingClient.attach_policy(
			policyName=self.policyname,
			target=certificateArn
		)
		response = self.thingClient.attach_thing_principal(
			thingName=thingName,
			principal=certificateArn
		)




thing = CreateThing()
thing.createThing()