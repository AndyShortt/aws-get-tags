import boto3

rgt = boto3.client('resourcegroupstaggingapi')
KEY = 'sc:deployment:launch-role:object-key' #UPDATE
product_ids=['prod-XXXX', 'prod-YYYY'] #UPDATE
product_portfolio={'products':[]}

def main():
    all_products_list = get_products_and_tags()
    portfolio = filter_products(product_ids,all_products_list)
    print (portfolio)

def get_products_and_tags():
    
    NO_TOKEN = ''
    product_list = get_resources(NO_TOKEN)
    all_products_list = product_list['ResourceTagMappingList']
    while product_list['PaginationToken']:
        product_list = get_resources(product_list['PaginationToken'])
        all_products_list.extend(product_list['ResourceTagMappingList'])

    return all_products_list

def get_resources(pagination_token):

    response = rgt.get_resources(
        PaginationToken=pagination_token,
        TagFilters=[
            {
                'Key': KEY
            },
        ],
        ResourcesPerPage=100,
        ResourceTypeFilters=[
            'catalog:product',
        ],
        IncludeComplianceDetails=False,
        ExcludeCompliantResources=False,
        )

    return response

def filter_products(product_ids,all_products_list):

    for product_id in product_ids:

        for product in all_products_list:
            if product_id == product_id_from_resourceARN(product['ResourceARN']):

                for tag in product['Tags']:
                    if tag['Key'] == KEY:
                        product_portfolio['products'].append(
                            {'Id': product_id, 'launch-role-object': tag['Value']}
                        )

    return product_portfolio

def product_id_from_resourceARN(resourceARN):
    elements = resourceARN.split(':')
    product = elements[5].split('/')
    return product[1]

main()