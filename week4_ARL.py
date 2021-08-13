pip install mlxtend
import pandas as pd
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
# çıktının tek bir satırda olmasını sağlar.
pd.set_option('display.expand_frame_repr', False)
from mlxtend.frequent_patterns import apriori, association_rules
df_ = pd.read_excel("online_retail_II.xlsx")
df = df_.copy()
def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

def retail_data_prep(dataframe):
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[dataframe["Quantity"] > 0]
    dataframe = dataframe[dataframe["Price"] > 0]
    replace_with_thresholds(dataframe, "Quantity")
    replace_with_thresholds(dataframe, "Price")
    return dataframe

df = retail_data_prep(df)
df.head(5)
df = df[df["Country"] == "Germany"]

def create_invoice_product_df(dataframe, id=False):
    if id:
        return dataframe.groupby(['Invoice', "StockCode"])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)
    else:
        return dataframe.groupby(['Invoice', 'Description'])['Quantity'].sum().unstack().fillna(0). \
            applymap(lambda x: 1 if x > 0 else 0)


ge_inv_pro_df = create_invoice_product_df(df)



frequent_itemsets = apriori(ge_inv_pro_df , min_support=0.01, use_colnames=True)
frequent_itemsets.sort_values("support", ascending=False).head(20)

rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.01)
rules.sort_values("support", ascending=False).head(20)

rules.sort_values("lift", ascending=False).head(20)


sorted_rules = rules.sort_values("lift", ascending=False)

product_id_21987 = 21987

recommendation_list_21987 = []

for i, product in enumerate(sorted_rules["antecedents"]):
    for j in list(product):
        if j == product_id_21987:
            recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0])


recommendation_list_21987[0:1]

product_id_23235 =23235
recommendation_list_23235 = []

for i, product in enumerate(sorted_rules["antecedents"]):
    for j in list(product):
        if j == product_id_23235:
            recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0])

recommendation_list_23235[0:1]

product_id_22747=22747

for i, product in enumerate(sorted_rules["antecedents"]):
    for j in list(product):
        if j == product_id_22747:
            recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0])

recommendation_list_22747[0:1]
