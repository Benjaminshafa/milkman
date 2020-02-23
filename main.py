import json
import requests
import xlwt 
from xlwt import Workbook 
import socket
import os
from azure.storage.blob import BlockBlobService

wb = Workbook() 
restSheet = wb.add_sheet('Rest',cell_overwrite_ok=True) 
gRPCSheet = wb.add_sheet('gRPC',cell_overwrite_ok=True)

rest_api_url_base = 'http://51.137.2.228/product_service_proxy'
grpc_api_url_base= 'http://52.157.226.83/product_service_proxy'
headers = {'product_id': '5e1b83a5cbafc82b042d897a',
           'customer_id': 'c90fbf5f-1b55-44a2-b18b-0a97869b5b60'}
def makeTheRESTCall(x):
    api_url = rest_api_url_base
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        restSheet.write(0, 0, 'Total_Rest_Latency') 
        restSheet.write(x, 0, json.loads(response.content.decode('utf-8'))['Duration'])
        resultObject = json.loads(response.content)
        productInfoCallDuration = resultObject['result'][0]['product_info_call_duration']
        restSheet.write(0, 1, 'product_Info_Duration')
        restSheet.write(x, 1, productInfoCallDuration)
        productRecommendationCallDuration = resultObject['result'][1]['product_recommendation_call_duration']
        restSheet.write(0, 2, 'product_Recommendation_Duration')
        restSheet.write(x, 2, productRecommendationCallDuration)
        productReviewCallDuration = resultObject['result'][2]['product_review_call_duration']
        restSheet.write(0, 3, 'product_Recommendation_Duration')
        restSheet.write(x, 3, productReviewCallDuration)
        productShippingCallDuration = resultObject['result'][3]['product_shipping_call_duration']
        restSheet.write(0, 4, 'productShippingCallDuration')
        restSheet.write(x, 4, productShippingCallDuration)
        customerShoppingCartCallDuration = resultObject['result'][4]['product_shopping_call_duration']
        restSheet.write(0, 5, 'product_shopping_call_duration')
        restSheet.write(x, 5, customerShoppingCartCallDuration)
        return json.loads(response.content.decode('utf-8'))['Duration']
    else:
        return None

def makegRPCCall(x):
    api_url = grpc_api_url_base
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        gRPCSheet.write(0, 0, 'Total_gRPC_Latency') 
        gRPCSheet.write(x, 0, json.loads(response.content.decode('utf-8'))['Duration'])
        resultObject = json.loads(response.content)
        productInfoCallDuration = resultObject['result'][0]['product_info_call_duration']
        gRPCSheet.write(0, 1, 'product_Info_Duration')
        gRPCSheet.write(x, 1, productInfoCallDuration)
        productRecommendationCallDuration = resultObject['result'][1]['ProductRecommendationResponse']['product_recommendation_call_duration']
        gRPCSheet.write(0, 2, 'product_Recommendation_Duration')
        gRPCSheet.write(x, 2, productRecommendationCallDuration)
        productReviewCallDuration = resultObject['result'][2]['ProductReviewResponse']['product_review_call_duration']
        gRPCSheet.write(0, 3, 'product_Recommendation_Duration')
        gRPCSheet.write(x, 3, productReviewCallDuration)
        productShippingCallDuration = resultObject['result'][3]['Shippingresponse']['product_shipping_call_duration']
        gRPCSheet.write(0, 4, 'productShippingCallDuration')
        gRPCSheet.write(x, 4, productShippingCallDuration)
        customerShoppingCartCallDuration = resultObject['result'][4]['shoppingcartResponse']['customer_shopping_cart_call_duration']
        gRPCSheet.write(0, 5, 'product_shopping_call_duration')
        gRPCSheet.write(x, 5, customerShoppingCartCallDuration)        
        return json.loads(response.content.decode('utf-8'))['result']
    else:
        return None

for x in range(1,500):
    totalRestDuration = makeTheRESTCall(x)
    totalgRPCDuration = makegRPCCall(x)
wb.save('report.xls')
# now upload it to Azure
file_name = 'report.xls'
account_name = 'milkman'
account_key = ''
container_name = 'milkman-container'

block_blob_service = BlockBlobService(
    account_name=account_name,
    account_key=account_key
)
block_blob_service.create_blob_from_path(container_name,socket.gethostname()+'_report_.xls', file_name)