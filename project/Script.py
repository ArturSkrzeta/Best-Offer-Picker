import pandas as pd
import numpy as np

def count_percentage(list1, list2):
    percentages_outcome = []
    for price1, price2 in zip(list1, list2):
        percentage = str(round(((price2/price1) - 1)*100,2)) + '%'
        percentages_outcome.append(percentage)
    else:
        return percentages_outcome

def get_prices(offers):
    mins, second_mins, maxs = [], [],[]
    for product_prices in offers:
        max = np.nanmax(product_prices)
        min = np.nanmin(product_prices)
        second_min = max
        for price in product_prices:
            if price > min and price < max and price < second_min:
                second_min = price
        else:
            second_mins.append(second_min)
            mins.append(min)
            maxs.append(max)
    return second_mins, mins, maxs

def main():
    df = pd.read_csv('Raw Data.csv', encoding='latin-1')
    df = df.replace({'0':np.nan, 0:np.nan, 0.00:np.nan})

    df['Supplier Best Offer'] = df.apply(lambda x: x.isin(df.min(axis=1)), axis=1).apply(lambda x: list(df.columns[x]), axis=1)     # finding min price from each row and looking up the column name = supplier name
    products = df['Product'].to_numpy()                                                                                             # taking all products from Product column
    best_offers = df['Supplier Best Offer'].to_numpy()                                                                              # taking all suppliers with best offer per each row = product
    
    df.drop(['Supplier Best Offer'],axis=1,inplace=True)
    df.drop(['Product'],axis=1,inplace=True)

    offers  = df.to_numpy()                                                                                                         # taking all prices from all suppliers


    second_mins, mins, maxs = get_prices(offers)
    percentages_sec_mins = count_percentage(mins, second_mins)
    percentages_maxs = count_percentage(mins, maxs)
    savings = [(max - min) for max, min in zip(maxs, mins)]

    outcome_dict = {'Porduct': products,
                    'Supplier Best Offer': best_offers,
                    'Best Price': mins,
                    'Second Best Price': second_mins,
                    'Percentage Second': percentages_sec_mins,
                    'Max Price': maxs,
                    'Percentage Max': percentages_maxs,
                    'Saving': savings
    }

    outcome_df = pd.DataFrame(outcome_dict)
    outcome_df.to_csv(r'Outcome.csv', index = False)

if __name__ == "__main__":
    main()
