import requests

api_key = 'AIzaSyCQMxTQME6YQNODItA5d1VajPht8e5Wurs'
user_ip = '146.70.173.180'

def search_books(query):
    base_url = 'https://www.googleapis.com/books/v1/volumes'
    params = {
        'q': query,
        'key': api_key,
        'userIp': user_ip,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        books_data = response.json()

        if 'items' in books_data:
            return books_data['items']
        else:
            print('No books found.')
    else:
        print(f'Request failed with status code {response.status_code}')

def main():
    query = 'spiritual not religious community building'
    books = search_books(query)

    if books:
        print('Books found:')
        for book in books:
            volume_info = book['volumeInfo']
            title = volume_info.get('title', 'Unknown Title')
            authors = volume_info.get('authors', [])

            print(f'- {title} by {", ".join(authors)}')

if __name__ == '__main__':
    main()

