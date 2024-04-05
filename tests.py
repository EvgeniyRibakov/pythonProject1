from src.masks import mask_accounts, convert_date_string

account_card = input()
masked_card = mask_accounts(account_card)

account_bill = input()
masked_bill = mask_accounts(account_bill)

date_string = input()
converted_date = convert_date_string(date_string)
print(converted_date)

