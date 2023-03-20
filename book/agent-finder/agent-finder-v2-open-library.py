import requests
import csv

def search_books(query):
    base_url = 'http://openlibrary.org/search.json'
    params = {
        'q': query,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        books_data = response.json()

        if 'docs' in books_data:
            return books_data['docs']
        else:
            print('No books found.')
    else:
        print(f'Request failed with status code {response.status_code}')

def save_books_to_csv(books, file_name):
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'authors', 'publish_date', 'isbn', 'publisher']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for book in books:
            writer.writerow({
                'title': book.get('title', 'Unknown Title'),
                'authors': ', '.join(book.get('author_name', [])),
                'publish_date': book.get('publish_date', ''),
                'isbn': ', '.join(book.get('isbn', [])),
                'publisher': ', '.join(book.get('publisher', [])),
            })

def main():
    query = input('Search term: ')
    books = search_books(query)

    if books:
        print('Books found:')
        for book in books:
            title = book.get('title', 'Unknown Title')
            authors = book.get('author_name', [])

            print(f'- {title} by {", ".join(authors)}')

        save_choice = input('Do you want to save the results to a file? (y/n): ').lower()
        if save_choice == 'y':
            file_name = input('File name (default: results.csv): ')
            if not file_name:
                file_name = 'results.csv'

            if not file_name.endswith('.csv'):
                file_name += '.csv'

            save_books_to_csv(books, file_name)
            print(f'Results saved to {file_name}')

if __name__ == '__main__':
    main()
