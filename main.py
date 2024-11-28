import json
from typing import List, Optional, Dict


FILE_NAME = "library.json"


class Book:
    def __init__(self, id: int, title: str, author: str, year: int, status: str = "в наличии"):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict:
        return {"id": self.id, "title": self.title, "author": self.author, "year": self.year, "status": self.status}

    @staticmethod
    def from_dict(data: Dict) -> 'Book':
        return Book(data["id"], data["title"], data["author"], data["year"], data["status"])



class Library:
    def __init__(self):
        self.books: List[Book] = []
        self.load_books()

    def load_books(self) -> None:
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                books_data = json.load(file)
                self.books = [Book.from_dict(book) for book in books_data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Ошибка при чтении файла данных.")

    def save_books(self) -> None:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int) -> None:
        new_id = max([book.id for book in self.books], default=0) + 1
        new_book = Book(new_id, title, author, year)
        self.books.append(new_book)
        self.save_books()
        print(f"Книга '{title}' добавлена с ID: {new_id}.")

    def delete_book(self, book_id: int) -> None:

        book = self.find_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self.save_books()
            print(f"Книга с ID {book_id} удалена.")
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def find_book_by_id(self, book_id: int) -> Optional[Book]:

        return next((book for book in self.books if book.id == book_id), None)

    def search_books(self, query: str, field: str) -> List[Book]:

        query = query.lower()
        if field == "title":
            return [book for book in self.books if query in book.title.lower()]
        elif field == "author":
            return [book for book in self.books if query in book.author.lower()]
        elif field == "year":
            return [book for book in self.books if str(book.year) == query]
        else:
            print("Поле поиска должно быть 'title', 'author' или 'year'.")
            return []

    def list_books(self) -> None:

        if not self.books:
            print("Библиотека пуста.")
            return
        for book in self.books:
            print(f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}")

    def change_status(self, book_id: int, new_status: str) -> None:

        if new_status not in ["в наличии", "выдана"]:
            print("Статус должен быть 'в наличии' или 'выдана'.")
            return
        book = self.find_book_by_id(book_id)
        if book:
            book.status = new_status
            self.save_books()
            print(f"Статус книги с ID {book_id} изменён на '{new_status}'.")
        else:
            print(f"Книга с ID {book_id} не найдена.")



def main():
    library = Library()
    print("Добро пожаловать в библиотеку!")

    while True:
        print("\nВыберите действие:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Введите номер действия: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания: "))
            library.add_book(title, author, year)

        elif choice == "2":
            book_id = int(input("Введите ID книги для удаления: "))
            library.delete_book(book_id)

        elif choice == "3":
            field = input("Искать по (title/author/year): ").lower()
            query = input("Введите запрос для поиска: ")
            results = library.search_books(query, field)
            if results:
                for book in results:
                    print(f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}")
            else:
                print("Книги не найдены.")

        elif choice == "4":
            library.list_books()

        elif choice == "5":
            book_id = int(input("Введите ID книги: "))
            new_status = input("Введите новый статус ('в наличии' или 'выдана'): ").strip()
            library.change_status(book_id, new_status)

        elif choice == "6":
            print("До свидания!")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()