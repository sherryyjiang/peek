def get_currency_list():
    return ["SGD", "USD", "EUR", "GBP", "INR", "AUD", "CAD", "JPY", "CNY", "HKD", "KRW", "THB", "IDR", "MYR", "PHP",
            "VND", "TWD"]


def get_currency_symbol(currency):
    currency_mapper = {
        "SGD": "S$",
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "INR": "₹",
        "AUD": "A$",
        "CAD": "C$",
        "JPY": "¥",
        "CNY": "¥",
        "HKD": "HK$",
        "KRW": "₩",
        "THB": "฿",
        "IDR": "Rp",
        "MYR": "RM",
        "PHP": "₱",
        "VND": "₫",
        "TWD": "NT$"
    }
    return currency_mapper.get(currency, "$")
