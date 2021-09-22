import boto3

sc = boto3.client('servicecatalog')
KEY = 'sc:deployment:launch-role:object-key' #UPDATE
product_ids=['prod-XXXX', 'prod-YYYY'] #UPDATE
product_portfolio={'products':[]}

def main():
    all_products_list = get_products_and_tags(product_ids)
    portfolio = filter_products(all_products_list)
    print (portfolio)

def get_products_and_tags(product_ids):
    
    all_products_list = []
    for ID in product_ids:
        product_info = describe_product(ID)
        all_products_list.append(product_info)

    return all_products_list

def describe_product(product_id):

    response = sc.describe_product_as_admin(
        Id=product_id
        )

    return response

def filter_products(all_products_list):

    for product in all_products_list:
        for tag in product['Tags']:
            if tag['Key'] == KEY:
                product_portfolio['products'].append(
                    {'Id': product['ProductViewDetail']['ProductViewSummary']['ProductId'], 'launch-role-object': tag['Value']}
                )

    return product_portfolio

def product_id_from_resourceARN(resourceARN):
    elements = resourceARN.split(':')
    product = elements[5].split('/')
    return product[1]

main()