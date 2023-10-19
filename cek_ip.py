import httpx

def get_ip():
    with httpx.Client() as client:
        response = client.get("http://ip.jsontest.com/")
    return response.json()

if __name__ == '__main__':
    print(get_ip())