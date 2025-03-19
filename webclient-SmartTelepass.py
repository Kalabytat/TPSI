import requests

def get_count_livorno():
    url = "http://www.smart-telepass.it/storico?id=1234&anno=2023"
    try:
        response = requests.get(url)
        response.raise_for_status()
        users = response.xml()

        transaction_model = [1 for user in users if user.ingresso]
        return transaction_model
    except requests.RequestException as e:
        print(f"Errore nella richiesta: {e}")
        return []
    
    if __name__ == "__main__":
        entrance = get_count_livorno()
        print(entrance)

