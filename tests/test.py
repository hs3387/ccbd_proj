import json


resp = {'Item': {'suggestion_0': '{\n  "title": "Ae Airflex 360 Slim Jean Men\'s Blue Breeze 32 x 36",\n  "product_link": "https://www.google.com/shopping/product/9438483085234779754?q=blue+jeans&hl=en&gl=us&prds=eto:11948724819674195360_0,pid:17108193665691941949,rsk:PC_4357192662493800297&sa=X&ved=0ahUKEwic5tmpiOL-AhWVsjEKHTLSBogQ8wII7xE",\n  "product_rating": "4.9",\n  "product_reviews": null,\n  "price": "$53.95",\n  "store": "American Eagle Outfitters",\n  "thumbnail": "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcSu-kvMpBO2JBacVjAUz2vpJK-gLtvP1A-Gv1jax-H2TRFx0rpZBHRBDqDT7IiaRum4fPjs8e14ckOnMZgpWLqXm5IFTvopIcK06co_ATu57Fs0IMKId8bISg&usqp=CAE",\n  "store_link": "https://www.google.com/url?url=https://www.ae.com/us/en/p/men/slim-fit-jeans/slim-jeans/ae-airflex-360-slim-jean/0117_6216_441%3Fmenu%3Dcat4840004&rct=j&q=&esrc=s&sa=U&ved=0ahUKEwic5tmpiOL-AhWVsjEKHTLSBogQguUECPER&usg=AOvVaw1Mpf8NJ6s9tn-3FfbJnN5-",\n  "delivery": "$7.95 delivery",\n  "store_rating": "4.8",\n  "store_reviews": "53",\n  "store_reviews_link": "https://www.google.com/url?url=https://www.google.com/shopping/ratings/account/metrics%3Fq%3Dae.com%26c%3DUS%26v%3D19%26hl%3Den&rct=j&q=&esrc=s&sa=U&ved=0ahUKEwic5tmpiOL-AhWVsjEKHTLSBogQ9-wCCPgR&usg=AOvVaw1wTsbPk1rH_RZH-zKaLFMx",\n  "compare_prices_link": null\n}'}, 'ResponseMetadata': {'RequestId': 'OID8EIKQ4AO3QK506SLA971MRRVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Sun, 07 May 2023 04:33:45 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '1356', 'connection': 'keep-alive', 'x-amzn-requestid': 'OID8EIKQ4AO3QK506SLA971MRRVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '2098740488'}, 'RetryAttempts': 0}}

x = json.loads(resp)

type(x)