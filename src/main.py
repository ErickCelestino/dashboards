from data_access.get_finances_data import GetFinancesData

def main():
    data = GetFinancesData()
    print(data.today_data_finance('BRL'))

if __name__ == "__main__":
    main()