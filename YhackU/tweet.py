import twitter

api = twitter.Api(consumer_key='20GUN4VeGC6femOun8VdzA',consumer_secret='gmouyeFmCXQQANzEgU9zWfC2QRvDQYYxBlpCv5cA1KI', access_token_key='1273494510-jSQemAFyFlDg5yDFtqHWpkNwt2zUPnptxNo17Ib', access_token_secret='cCk6owpDysCqRLbQyenmuMevGrbEV7oX3wNVRy34')
print api.VerifyCredentials()
print [x.AsDict() for x in api.GetSearch(term='#skyfall', per_page=30)]
