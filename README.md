# amazon-pricedrop
Receive notifications of price drops on previous Amazon purchases.

## Installation
1. Clone this project: `git clone https://github.com/tomhoover/amazon-pricedrop.git`
1. Create python venv (if desired)
1. Install requirements: `pip install -r requirements.txt`

## Usage
1. Download your 'Order History Report' from Amazon, and save as `purchases.csv`
    - while logged into your Amazon account, select 'Accounts & Lists'
    - under 'Ordering and shopping preferences', select 'Download order reports'
1. Execute `python3 ./amazon-pricedrop.py`
1. Any items that have had a price drop since your previous purchase will be
  displayed (the results will also be saved in 'price_drops.txt')
