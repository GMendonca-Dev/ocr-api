import requests
import json
from datetime import datetime, timedelta
from config import auth_url, email, senha, api_url

# Variável global para armazenar o token
token_info = {
    "token": None,
    "expires_at": None
}


def get_auth_token():
    headers = {'Content-Type': 'application/json'}
    payload = {'email': email, 'senha': senha}
    try:
        response = requests.post(auth_url, data=json.dumps(payload), headers=headers, verify=False)
        response.raise_for_status()
        token = response.json().get('token')
        
        if token:
            token_info['token'] = token
            token_info['expires_at'] = datetime.now() + timedelta(hours=23)
            return token
        else:
            print("Token não encontrado.")
            return None
    except requests.RequestException as e:
        print(f"Erro ao obter token: {e}")
        return None


def is_token_valid():
    return token_info['token'] and datetime.now() < token_info['expires_at']


def ensure_valid_token():
    if not is_token_valid():
        #print("Token inválido ou expirado. Renovando token...")
        return get_auth_token()
    else:
        print("Token ainda é válido.")
        return token_info['token']


def fetch_data_from_api(page_number):
    token = ensure_valid_token()
    if not token:
        return []
    
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get(f"{api_url}?pagina={page_number}", headers=headers, verify=False)
        response.raise_for_status()
        registros = response.json().get("registros", [])
        return registros
    except requests.RequestException as e:
        print(f"Erro ao buscar dados da API: {e}")
        return []
