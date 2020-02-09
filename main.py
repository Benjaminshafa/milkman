import json
import requests
import xlwt 
from xlwt import Workbook 
wb = Workbook() 
sheet1 = wb.add_sheet('Rest',cell_overwrite_ok=True) 

rest_api_url_base = 'http://40.74.161.60/product_service_proxy'
grpc_api_url_base= 'http://20.45.1.226/product_service_proxy'
headers = {'product_id': '5e1b83a5cbafc82b042d897a',
           'customer_id': 'c90fbf5f-1b55-44a2-b18b-0a97869b5b60'}
def makeTheRESTCall(x):
    api_url = rest_api_url_base
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        sheet1.write(0, 0, 'Total_Rest_Latency') 
        sheet1.write(x, 0, json.loads(response.content.decode('utf-8'))['Total_Services_Call_In_REST_took'])
        print('done') 
        return json.loads(response.content.decode('utf-8'))['Total_Services_Call_In_REST_took']
    else:
        return None
def makegRPCCall(x):
    api_url = grpc_api_url_base
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        sheet1.write(0, 2, 'Total_gRPC_Latency') 
        sheet1.write(x, 2, json.loads(response.content.decode('utf-8'))['Total_Services_Call_In_gRPC_Per_Millisecond'])
        print('done') 
        return json.loads(response.content.decode('utf-8'))['Total_Services_Call_In_gRPC_Per_Millisecond']
    else:
        return None
for x in range(1,20):
    totalRestDuration = makeTheRESTCall(x)
    totalgRPCDuration = makegRPCCall(x)
wb.save('report.xls')


# https://www.geeksforgeeks.org/writing-excel-sheet-using-python/