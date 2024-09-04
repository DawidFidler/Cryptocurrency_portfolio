import requests
from pprint import pprint
from api_key import KEY

PATH = "crypto.txt"
CLEAR = "\033[2J"
BASE_URL_CRYPTO = "https://pro-api.coinmarketcap.com/"
BASE_URL_EXCHANGE = "https://open.er-api.com/v6/latest/USD"
ENDPOINT_1 = "v1/cryptocurrency/listings/latest?"
CMC = "CMC_PRO_API_KEY="


def view_actual_prices():
    with open(PATH, "r") as f:
        lines = f.readlines()
        portfolio = {}
        for line in lines:  #Creating dictionary with symbols and amount of each coin
            tokens = line.strip().split(":")
            symbol = tokens[0].strip()
            amount = float(tokens[1].strip())
            portfolio[symbol] = amount
    
    response = requests.get(BASE_URL_CRYPTO + ENDPOINT_1 + CMC + KEY + "&limit=20")    #limiting data request to 20 first tokens
    if response.status_code == 200:
        data = (response.json())
        for coin in data["data"]:
            symbol = coin["symbol"]
            if symbol in portfolio:
                current_price = coin["quote"]["USD"]["price"]
                value = round(current_price * amount, 2)
                portfolio[symbol] = value

    print(CLEAR)
    print("Your cryptocurrencies are worth (USD):\n")
    for symbol, value in portfolio.items():
        print(f"{symbol}: {value}")
    
    convert = input("Would you like to convert that value for other currency? (NO, YES): ").upper()
    if convert == "YES":
        convert_value()
    else:
        pass
    

def view_amount():
    with open(PATH, "r") as f:
        print(CLEAR, "\nPortfolio contains:")
        for line in f.readlines():
            data = (line.rstrip())
            print(data)   
    

def add():
    response = requests.get(BASE_URL_CRYPTO + ENDPOINT_1 + CMC + KEY + "&limit=20")    #limiting data request to 20 first tokens
    if response.status_code == 200:
        data = (response.json())

        view_amount()
        print("\nBelow you can see all cryptocurrency you can add to portfolio:")
        
        symbols = []
        for crypto in (data["data"]):
            symbol = crypto["symbol"]
            symbols.append(symbol)
        print(*symbols) #This way symbols list will be printed without square brackets
        
        while True:
            token_choice = input("Type a proper symbol: ").upper()
            if token_choice not in symbols:
                print("You typed invalid symbol!")
            else:
                break

        token_amount = float(input(f"How many {token_choice} would you like to add? "))
        if token_amount > 0:
            with open(PATH, "r") as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if line.startswith(token_choice):
                        parts = line.split(":")
                        existing_amount = float(parts[1].strip())
                        lines[i] = f"{token_choice}: {existing_amount + token_amount}\n"
                        break
                else:   #it happens when for loop ends naturally (doesn't find any existing token)
                    lines.append(f"\n{token_choice}: {token_amount}")

            with open(PATH, "w") as f:
                f.writelines(lines)
            
            delete_empty_lines()

        else:
            print("You have to enter positive number!")

    else:
        print(f"Something get wrong with request. Status code -> {response.status_code}")
        quit()


def convert_value():
    response = requests.get(BASE_URL_EXCHANGE)
    data = response.json()
    rates = data["rates"]
    currencies_symbol = list(rates.keys())
    print(CLEAR)
    print(*currencies_symbol)
    
    choice = input("\nSelect currency to which you wanna convert the value of your portfolio: ").upper()
    if choice in currencies_symbol:
        choice_rate = rates[choice]

        with open(PATH, "r") as f:
            lines = f.readlines()
            portfolio = {}
            for line in lines:  #Creating dictionary with symbols and amount of each coin
                tokens = line.strip().split(":")
                symbol = tokens[0].strip()
                amount = float(tokens[1].strip())
                portfolio[symbol] = amount
        
        response = requests.get(BASE_URL_CRYPTO + ENDPOINT_1 + CMC + KEY + "&limit=20")    #limiting data request to 20 first tokens
        data = (response.json())
        for coin in data["data"]:
            symbol = coin["symbol"]
            if symbol in portfolio:
                current_price = coin["quote"]["USD"]["price"]
                value = current_price * amount
                converted_value = round(value * choice_rate, 2)
                portfolio[symbol] = converted_value
        
        print(f"{CLEAR}\nYour cryptocurrencies in {choice} are worth:")
        for symbol, converted_value in portfolio.items():
            print(f"{symbol}: {converted_value}")


def remove():
    response = requests.get(BASE_URL_CRYPTO + ENDPOINT_1 + CMC + KEY + "&limit=20")    #limiting data request to 20 first tokens
    if response.status_code == 200:
        data = response.json()

        view_amount()
        print("\nBelow you can see all cryptocurrency you can remove from portfolio:")
        
        symbols = []
        for crypto in (data["data"]):
            symbol = crypto["symbol"]
            symbols.append(symbol)
        print(*symbols)     #This way symbols list will be printed without square brackets
        
        while True:
            token_choice = input("Type a proper symbol: ").upper()
            if token_choice not in symbols:
                print("You typed invalid symbol!")
            else:
                break

        token_amount = float(input(f"How many {token_choice} would you like to remove? "))
        if token_amount > 0:
            with open(PATH, "r") as f:
                lines = f.readlines()
                for i, line in enumerate(lines):    #going through file and returning characters and indexes. By i- it numerates each line
                    if line.startswith(token_choice):
                        parts = line.split(":")
                        existing_amount = float(parts[1].strip())
                        if existing_amount > token_amount:
                            lines[i] = f"{token_choice}: {existing_amount - token_amount}\n"
                            break   #Breaking loop not to go through next lines
                        elif existing_amount < token_amount:
                            print(f"You have {existing_amount} {token_choice}. You can't remove {token_amount}")
                            break
                        else:
                            del lines[i]                      
                else:
                    print(f"You don't have any {token_choice} in portfolio!")

            with open(PATH, "w") as f:
                f.writelines(lines)
            
            delete_empty_lines()

        else:
            print("You have to enter positive number!") 

    else:
        print(f"Something get wrong with request. Status code -> {response.status_code}")
        quit()


def delete_empty_lines():
    with open(PATH, 'r') as file:
        lines = file.readlines()

    new_lines = []
    for line in lines:
        if line.strip():
            new_lines.append(line.strip())

    with open(PATH, 'w') as file:
        file.write('\n'.join(new_lines))


def main():
    while True:
        print("\nWelcome in your Cryptocurrency portfolio! Check out the actions menu:"
            "\n1. View portfolio (amount)"
            "\n2. View portfolio (value)"
            "\n3. Add cryptocurrency to the portfolio"
            "\n4. Remove cryptocurrency from portfolio"
            "\n5. Quit")
        action = input("Select the action you would like to do: ").lower()

        if action == "1":
            view_amount()
        elif action == "2":
            view_actual_prices()
        elif action == "3":
            add()
        elif action == "4":
            remove()
        elif action == "5":
            print("Goodbye!")
            break        
        else:
            print("Invalid action!")

main()