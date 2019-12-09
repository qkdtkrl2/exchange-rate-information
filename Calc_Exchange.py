def Usd_Exchage(name, exchange, money):

    if name =="JPY 일본":
        jpy_money = ((exchange/100.0) * money)
        str = f'{jpy_money}'
        return str
    elif name == "IDR 인도네시아":
        jpy_money = ((exchange / 100.0) * money)
        str = f'{jpy_money}'
        return str
    else:
        usd_money = exchange * money
        str = f'{usd_money}'
        return str

