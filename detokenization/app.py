#de-tokenization

import boto3
from flask import Flask, request, render_template

app = Flask(__name__)

# Create a Boto3 client for DynamoDB
dynamodb_client = boto3.client('dynamodb', region_name='ap-southeast-2')

# Create a Boto3 client for KMS
kms_client = boto3.client('kms', region_name='ap-southeast-2')

# DynamoDB table name
dynamodb_table_name = 'token-db'

@app.route('/', methods=['GET', 'POST'])
def detokenize():
    if request.method == 'POST':
        # Get the name from the request
        name = request.form.get('name')

        # Check if the name is provided
        if not name:
            return 'Name not provided', 400

        # Check if the name exists in DynamoDB
        response = dynamodb_client.scan(
            TableName=dynamodb_table_name,
            FilterExpression='#nm = :name',
            ExpressionAttributeNames={'#nm': 'name'},
            ExpressionAttributeValues={':name': {'S': name}}
        )

        # If a record is found, decrypt and detokenize the credit card number
        if 'Items' in response and len(response['Items']) > 0:
            item = response['Items'][0]
            ciphertext = item['ciphertext']['B']
            credit_card_number = decrypt_credit_card_number(ciphertext)

            return f'Credit Card Number: {credit_card_number}'
        else:
            return f'No record found for name: {name}'

    # If it's a GET request, render the HTML form
    return render_template('detokenize.html')

def decrypt_credit_card_number(ciphertext):
    # Use the KMS client to decrypt the credit card number
    response = kms_client.decrypt(CiphertextBlob=ciphertext)
    KeyId='055e121c-723e-49d1-90b7-049f827793d2'
    credit_card_number = response['Plaintext'].decode('utf-8')
    return credit_card_number

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
