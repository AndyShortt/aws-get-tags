## Summary
This is a reference implementation of the AWS Resource Groups and Tagging API [GetResources](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resourcegroupstaggingapi.html#ResourceGroupsTaggingAPI.Client.get_resources). The purpose is to demonstrate how the GetResources API can be used as a replacement for service-specific API calls to retrieve tag values, such as the AWS Service Catalog API [DescribeProductAsAdmin](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog.html#ServiceCatalog.Client.describe_product_as_admin). In this scenario, the advantage of GetResources is reduced API calls to AWS for the same result.

## Prerequisites
- Python3 runtime
- AWS boto3 installed and [configured](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration)

## What it does
The __Get_Resources.py__ script takes several fixed inputs, and returns a JSON list of Service Catalog Product IDs with the requested tag value. The KEY variable and the product_ids list should be adjusted by you to reference the appropriate tag key and product list to filter on (leaving product list blank will return no results).

During execution, the script follows this path:
- Calls the GetResources API to get tags for Service Catalog products that contain the specified tag key. This API supports pagination, and the script handles paginated responses properly.
- Takes the full list of responses and filters out product IDs that are not in the product_ids list and tags that have different keys than the specified KEY.
- Prints the result as a JSON list of Product IDs and Key:Values.

## Why Does it Matter
Comparing this script to __Describe_Product_As_Admin.py__ you will find identical inputs and outputs, however this script uses the Service Catalog API (compared to Resource Groups and Tagging API). When the goal is to just get the tag values for Service Catalog products, using the GetResources API allows you to make a single API call. This is compared to using the DescribeProductAsAdmin API which you have to call for each product in your list. This results in significantly reduced AWS API calls which helps with AWS API throttling and any network latency. The tradeoff is that the GetResources API requires more client-side logic, as you have to iterate through the list locally and pull out only the products you are looking for. It would be appropriate to call the DescribeProductAsAdmin API if you needed more information about the product than just the tag values.


## Disclaimer
This is not production code and will not be activly maintained. You can reuse this code, at your own risk, under the MIT-0 license as outlined in LICENSE file. Use of the AWS Services demonstrated here require the AWS [Customer Agreement](https://aws.amazon.com/agreement/).