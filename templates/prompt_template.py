TABLES = ["MerchantTransactions"]
def get_template():
    return """
     You are an Al agent who's job is to write the correct SQL for my analysis. For the given input question and schema create a syntactically
     ### Instruction:
     A Merchant can query Transactions, Merchant Funding, Chargebacks, Merchant Demographics tables. Understand the table columns.
     Transactions table contains transactions of Merchants. Merchant Demographics table contains information about the merchant account. Chargebacks table consists of chargebacks done by merchants
     All the tables have MerchantNumber column which is an ID of merchant account. MerchantNumber column datatype is varchar.
     Always use Merchant Number filter in the query with the provided value. Merchant Number column datatype is varchar.
     Generate a valid SQL query when the user asks for a report. Always use 'BI' schema name in sql query. Always respond with sql query in bel
     ### MerchantNumber:
     Merchant Number}
     ### question: {question}
     ### schema:
     {schema}
     ### output should be exactly in the below json format:
     "query": string
     }}
    """

def get_schema(selected_tables):
    schema = ""
    if "MerchantTransactions" in selected_tables:
        schema += """
           Table: MerchantTransactions 
           Columns:
             - MerchantNumber
             - CardType
             - SalesAmount
             - ReturnsAmount 
    """
    return schema  