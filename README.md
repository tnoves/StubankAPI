# StuBank API

StuBank API is a Python app that launches and hosts a Flask API that interacts with the remote database at 
`cs-db.ncl.ac.uk`

## Installation

Pull this git repository and then download the dependencies using pip.

```bash
pip install -r requirements.txt
```

Once all dependencies are installed, create a file in the `app` folder called `login_details.txt` to include your 
***Newcastle University login details*** so that a connection to the database can be made. The file must be written in the 
format:

```bash
username password
```

## Usage

Run the `api_main.py` file, and the API will be launched at `127.0.0.1:5000`


## REST API

#### Contents

---

- [ Users ](#users) 
    - [ Create user ](#create-user)
    - [ Get user ](#get-user)
    - [ Get all users ](#get-all-users)
    - [ Update user ](#update-user)
    - [ Delete user ](#delete-user)
- [ User Details ](#userdetails)
    - [ Get user details ](#get-user-details)
    - [ Update user details ](#update-user-details)
- [ Cards ](#cards)
    - [ Create card ](#create-card)
    - [ Get card ](#get-card)
    - [ Get all cards belonging to user ](#get-all-cards)
    - [ Update card ](#update-card)
    - [ Delete card ](#delete-card)
- [ Accounts ](#accounts)
    - [ Get account ](#get-account)
    - [ Get account from card number ](#get-account-card)
    - [ Update account ](#update-account)
    - [ Delete account ](#delete-account)
- [ Sort Codes ](#sort-codes)
    - [ Get sort code ](#get-sort-code)
    - [ Update sort code ](#update-sort-code)
- [ Transactions ](#transactions)
    - [ Create transaction ](#create-transaction)
    - [ Get transaction ](#get-transaction)
    - [ Get all transactions belonging to card ](#get-all-transactions)
    - [ Update transaction ](#update-transaction)
    - [ Delete transaction ](#delete-transaction)
- [ Payment Accounts ](#payment-accounts)
    - [ Create payment account ](#create-payment-account)
    - [ Get payment account ](#get-payment-account)
    - [ Update payment account ](#update-payment-account)
    - [ Delete payment account ](#delete-payment-account)
---

<a name="users"></a>
### Users

<a name="create-user"></a>
#### Create user

`POST 127.0.0.1:5000/user/`

###### Response

```bash
{
    "id": 1,
    "user_details_id": 1,
    "username": "Foo"
}
```

<a name="get-user"></a>
#### Get user

`GET 127.0.0.1:5000/user/<id>`

###### Response

```bash
{
    "id": 1,
    "user_details_id": 1,
    "username": "Foo"
}
```

<a name="get-all-users"></a>
#### Get all users

`GET 127.0.0.1:5000/user/all`

###### Response

```bash
[
    {
        "id": 1,
        "user_details_id": 1,
        "username": "Foo"
    }   
]
```

<a name="update-user"></a>
#### Update user

`PUT 127.0.0.1:5000/user/<id>`

###### Response

```bash
{
    "id": 1,
    "user_details_id": 1,
    "username:" "Fooo"
}
```

<a name="delete-user"></a>
#### Delete user

`DELETE 127.0.0.1:5000/user/<id>`

<a name="user-details"></a>
### User Details

<a name="get-user-details"></a>
#### Get user details

`GET 127.0.0.1:5000/user/details/<id>`

###### Response

```bash
{
    "dob": "0001-01-01",
    "email": "test@test.com",
    "firstname": "Foo",
    "lastname": "Bar",
    "phone": "1",
    "user_details_id": 1
}
```

<a name="update-user-details"></a>
#### Update user details

`PUT 127.0.0.1:5000/user/details/<id>`

###### Response

```bash
{
    "dob": "0001-01-01",
    "email": "test@test.com",
    "firstname": "Foo",
    "lastname": "Bar",
    "phone": "1",
    "user_details_id": 1
}
```

<a name="cards"></a>
### Cards

<a name="create-card"></a>
#### Create card

`POST 127.0.0.1:5000/card/`

###### Response

```bash
{
    "card_number": 9367237451037453,
    "account_id": 1,
    "active": 0,
    "balance": 150.40,
    "cvc_code": 001,
    "card_type": "GBP",
    "expiry_date": 0001-01-01,
    "payment_processor": "Visa",
    "user_id": 1
}
```

<a name="get-card"></a>
#### Get card

`GET 127.0.0.1:5000/card/<id>`

###### Response

```bash
{
    "card_number": 9367237451037453,
    "account_id": 1,
    "active": 0,
    "balance": 150.40,
    "cvc_code": 001,
    "card_type": "GBP",
    "expiry_date": 0001-01-01,
    "payment_processor": "Visa",
    "user_id": 1
}
```

<a name="get-all-cards"></a>
#### Get all cards belonging to user

`GET 127.0.0.1:5000/card/user/<id>`

###### Response

```bash
[
    {
        "card_number": 9367237451037453,
        "account_id": 1,
        "active": 0,
        "balance": 150.40,
        "cvc_code": 001,
        "card_type": "GBP",
        "expiry_date": 0001-01-01,
        "payment_processor": "Visa",
        "user_id": 1
    }
]
```

<a name="update-card"></a>
#### Update card

`PUT 127.0.0.1:5000/card/<id>`

###### Response

```bash
{
    "card_number": 9367237451037453,
    "account_id": 1,
    "active": 0,
    "balance": 150.40,
    "cvc_code": 001,
    "card_type": "GBP",
    "expiry_date": 0001-01-01,
    "payment_processor": "Visa",
    "user_id": 1
}
```

<a name="delete-card"></a>
#### Delete card

`DELETE 127.0.0.1:5000/card/<id>`

<a name="accounts"></a>
### Accounts

<a name="get-account"></a>
#### Get account

`GET 127.0.0.1:5000/account/<id>`

###### Response

```bash
{
    "account_id": 1,
    "account_number": 93742845,
    "sort_code_id": 1
}
```

<a name="get-account-card"></a>
#### Get account from card account number

`GET 127.0.0.1:5000/account/card/<id>`

###### Response

```bash
{
    "account_id": 1,
    "account_number": 93742845,
    "sort_code_id": 1
}
```

<a name="update-account"></a>
#### Update account

`PUT 127.0.0.1:5000/account/<id>`

###### Response

```bash
{
    "account_id": 1,
    "account_number": 93742845,
    "sort_code_id": 1
}
```

<a name="delete-account"></a>
#### Delete account

`DELETE 127.0.0.1:5000/account/<id>`

<a name="sort-codes"></a>
### Sort Codes

<a name="get-sort-code"></a>
#### Get sort code

`GET 127.0.0.1:5000/sort_code/<id>`

###### Response

```bash
{
    "sort_code_id": 1,
    "sort_code": "740591"
}
```

<a name="update-sort-code"></a>
#### Update sort code

`PUT 127.0.0.1:5000/sort_code/<id>`

###### Response

```bash
{
    "sort_code_id": 1,
    "sort_code": "740591"
}
```

<a name="transactions"></a>
### Transactions 

<a name="create-transaction"></a>
#### Create transaction

`POST 127.0.0.1:5000/transaction/`

###### Response

```bash
{
    "id": 1,
    "card_number": 9367237451037453,
    "balance": 25.43,
    "date": 0001-01-01,
    "payment_account_id": 1,
    "payment_amount": 25.43,
    "payment_type": "debit"
}
```

<a name="get-transaction"></a>
#### Get transaction

`GET 127.0.0.1:5000/transaction/<id>`

###### Response

```bash
{
    "id": 1,
    "card_number": 9367237451037453,
    "balance": 25.43,
    "date": 0001-01-01,
    "payment_account_id": 1,
    "payment_amount": 25.43,
    "payment_type": "debit"
}
```

<a name="get-all-transactions"></a>
#### Get all transactions belonging to card

`GET 127.0.0.1:5000/transaction/card/<id>`

###### Response

```bash
[
    {
        "id": 1,
        "card_number": 9367237451037453,
        "balance": 25.43,
        "date": 0001-01-01,
        "payment_account_id": 1,
        "payment_amount": 25.43,
        "payment_type": "debit"
    }
]
```

<a name="update-transaction"></a>
#### Update transaction

`PUT 127.0.0.1:5000/transaction/<id>`

###### Response

```bash
{
    "id": 1,
    "card_number": 9367237451037453,
    "balance": 25.43,
    "date": 0001-01-01,
    "payment_account_id": 1,
    "payment_amount": 25.43,
    "payment_type": "debit"
}
```

<a name="delete-transaction"></a>
#### Delete transaction

`DELETE 127.0.0.1:5000/transaction/<id>`

<a name="payment-accounts"></a>
### Payment Accounts

<a name="create-payment-account"></a>
#### Create payment account

`POST 127.0.0.1:5000/payment_account/`

###### Response

```bash
{
    "payment_account_id": 1,
    "account_id": 1,
    "user_details_id": 1
}
```

<a name="get-payment-account"></a>
#### Get payment account

`GET 127.0.0.1:5000/payment_account/<id>`

###### Response

```bash
{
    "payment_account_id": 1,
    "account_id": 1,
    "user_details_id": 1
}
```

<a name="update-payment-account"></a>
#### Update payment account

`PUT 127.0.0.1:5000/payment_account/<id>`

###### Response

```bash
{
    "payment_account_id": 1,
    "account_id": 1,
    "user_details_id": 1
}
```

<a name="delete-payment-account"></a>
#### Delete payment account

`DELETE 127.0.0.1:5000/payment_account/<id>`
