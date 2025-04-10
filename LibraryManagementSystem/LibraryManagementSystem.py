from datetime import datetime, timedelta
import getpass
import os

# Represents/Manages each book
class Book:
    def __init__(self,title,author,ISBN):
        self.title = title
        self.author = author
        self.ISBN = ISBN

    def __str__(self):
        return self.title, self.author, self.ISBN

        
# Represents a library user
# Will borrow books creating a "loan" object
class Patron:
    def __init__(self,name,ID):
        self.name = name
        self.ID = ID

    def __str__(self):
        return f"{self.name} ({self.ID})"

# Tracks borrowed books
# Will handle the borrowing and return process
class Loan:
    def __init__(self,book_borrowed_title,borrow_date,return_date,associated_patron_name):
        self.book_borrowed_title = book_borrowed_title
        self.borrow_date = borrow_date
        self.return_date = return_date
        self.associated_patron_name = associated_patron_name


# Central manager of books and patrons
# Will manage books and patrons
class Library:
    def __init__(self):
        self.books_list = []
        self.patrons_list = []
        self.loans_list = []
        
    def add_book(self,book):
        self.books_list.append(book)

    def list_books(self):
        # List all books in the library
        for index, book in enumerate(self.books_list, start=1):
            print(f"{index}. Title: {book.title}, Author:{book.author}, ISBN:{book.ISBN}")

    def save_books(self):
        file_path = "BookManager.txt"
        file_empty = os.path.getsize(file_path) == 0

        with open(file_path,'a') as wf:
            for book in self.books_list:
                line = f"{book.title}, {book.author}, {book.ISBN}"
                if not file_empty:
                    wf.write('\n' + line)
                else:
                    wf.write(line)
                    file_empty = False
          
    def register_patron(self,patron):
        self.patrons_list.append(patron)

    def list_patrons(self):
        for index, patron in enumerate(self.patrons_list, start=1):
            print(f"{index}. Name: {patron.name}, ID: {patron.ID}")
    
    def save_patrons(self):
        file_path = "PatronManager.txt"
        file_empty = os.path.getsize(file_path) == 0

        with open(file_path,'a') as wf:
            for patron in self.patrons_list:
                line = f"{patron.name}, {patron.ID}"
                if not file_empty:
                    wf.write('\n' + line)
                else:
                    wf.write(line)
                    file_empty = False
            
    def load_books(self):
        try:
            with open('BookManager.txt','r') as rf:
                book_content = rf.readline()
                while book_content:
                    final_book_content = book_content.rstrip("\n").split(",")
                    if len(final_book_content) != 3:
                        print("Invalid data format!")
                        book_content = rf.readline()
                        continue 

                    # Unpacking the final_conent into title,author and ISBN
                    title,author,ISBN = final_book_content

                    # Creating a book instance with the newly unpacked content
                    bookInstance = Book(title,author,ISBN)

                    # Adding the bookInstance to the library's books list
                    self.books_list.append(bookInstance)

                    # Read the next line
                    book_content = rf.readline()

        except FileNotFoundError:
            print("No previous book records found. Starting a fresh...")

    
    def load_patrons(self):
        try:
            with open('PatronManager.txt','r') as rf:
                patron_content = rf.readline()
                while patron_content:
                    final_patron_content = patron_content.rstrip("\n").split(",")
                    if len(final_patron_content) != 2:
                        print("Invalid data format!")
                        patron_content = rf.readline()
                        continue
                    name,ID = final_patron_content
                    patronInstance = Patron(name,ID)
                    self.patrons_list.append(patronInstance)
                    patron_content = rf.readline() 


        except FileNotFoundError:
            print("No previous patron records found. Starting a fresh...")


# We must first load the books before searching.
    def search_books(self,search_type,input_value):
        book_matches = []
        try:
                with open('BookManager.txt','r') as rf:
                    book_content = rf.readline()

                    while book_content:
                        final_book_content = book_content.rstrip("\n").split(",")
                        if len(final_book_content) != 3:
                            print(f"Invalid data format:{book_content}")
                            book_content = rf.readline()
                            continue 

                        # Unpacking the final_content into title,author and ISBN
                        title,author,ISBN = final_book_content
                        
                        # Using "in" for partial matching
                        if search_type == "title" and input_value in title:
                            bookInstance = Book(title,author,ISBN)
                            book_matches.append(bookInstance) # Adding the matching book to the list
                            
                            

                        elif search_type == "author" and input_value in author:
                            bookInstance = Book(title,author,ISBN)
                            book_matches.append(bookInstance)
                            

                        elif search_type == "ISBN" and input_value in ISBN:
                            bookInstance = Book(title,author,ISBN)
                            book_matches.append(bookInstance)
                            
                        # Read the next line
                        book_content = rf.readline()

                    if not book_matches:
                            print("No matching books found!")
                            return None
                    
                    else:
                        return book_matches
                    
        except FileNotFoundError:
            print("No previous book records found. Starting a fresh...")


    def search_patrons(self,search_type,input_value):
        patron_matches = []
        try:
            with open('PatronManager.txt','r') as rf:
                patron_content = rf.readline()

                while patron_content:
                    final_patron_content = patron_content.rstrip("\n").split(",")
                    if len(final_patron_content) != 2:
                        print("Invalid data format!")
                        patron_content = rf.readline()
                        continue

                    name,ID = final_patron_content
                    
                    if search_type == "name" and input_value in name:
                        patronInstance = Patron(name,ID)
                        patron_matches.append(patronInstance)

                    elif search_type == "ID" and input_value in ID:
                        patronInstance = Patron(name,ID)
                        patron_matches.append(patronInstance)

                    patron_content = rf.readline()

                if not patron_matches:
                    print("No matching patrons found!")
                    return None
                else:
                    return patron_matches 


        except FileNotFoundError:
            print("No previous patron records found. Starting a fresh...")


    def delete_book(self,search_type,input_value):
        if not self.books_list:
            print("KINDLY load your books first!")
            return None
        # Searching for the book
        book_matches = []
        try:
                with open('BookManager.txt','r') as rf:
                    book_content = rf.readline()
                    found = False # To track if the book is found

                    while book_content:
                        final_book_content = book_content.rstrip("\n").split(",")
                        if len(final_book_content) != 3:
                            print(f"Invalid data format:{book_content}")
                            book_content = rf.readline()
                            continue 

                        # Unpacking the final_content into title,author and ISBN
                        title,author,ISBN = final_book_content
                        
                        # Using "in" for partial matching
                        if search_type == "title" and input_value in title:
                            bookInstance = Book(title,author,ISBN)
                            book_matches.append(bookInstance) # Adding the matching book to the list
                            
                            

                        elif search_type == "author" and input_value in author:
                            bookInstance = Book(title,author,ISBN)
                            book_matches.append(bookInstance)
                            

                        elif search_type == "ISBN" and input_value in ISBN:
                            bookInstance = Book(title,author,ISBN)
                            book_matches.append(bookInstance)
                            
                        # Read the next line
                        book_content = rf.readline()

                    # Handling search result
                    if not book_matches: # This line automatically checks if the list is empty
                            print("No matching books found!")
                            return None
                    
                    if len(book_matches) > 1:
                        print("Here are the available books:-")
                        print()
                        for index, book in enumerate(book_matches, start=1):
                            print(f"{index}. Title: {book.title}, Author: {book.author}, ISBN: {book.ISBN}")

                        print()

                        # Validating the input
                        while True:

                            choice = input("Enter the index of the book to delete: ")
                            try:
                                int_choice = int(choice) - 1 # Convert input to zero-based index
                                if int_choice < 0 or int_choice >= len(book_matches):
                                    print("Invalid input. Please choose a valid number.")
                                else:
                                    break

                            except ValueError:
                                print("Invalid input! Please enter a number.")

                        # Deleting the book
                        book_to_delete = book_matches[int_choice]
                        for book in self.books_list:
                            if book.title == book_to_delete.title and book.author == book_to_delete.author and book.ISBN == book_to_delete.ISBN:
                                self.books_list.remove(book)
                                break

                        # Updating the bookManager text file
                        with open('BookManager.txt','w') as wf:
                            for book in self.books_list:
                                wf.write(f"{book.title},{book.author},{book.ISBN}\n")
                        print()
                        print("Book deleted successfully.")


                    else:
                        # Deleting the book
                        book_to_delete = book_matches[0]
                        for book in self.books_list:
                            if book.title == book_to_delete.title and book.author == book_to_delete.author and book.ISBN == book_to_delete.ISBN:
                                self.books_list.remove(book)
                                break

                        # Updating the bookManager text file
                        with open('BookManager.txt','w') as wf:
                            for book in self.books_list:
                                wf.write(f"{book.title},{book.author},{book.ISBN} \n")
                        print()
                        print("Book deleted successfully.")
                   
        except FileNotFoundError:
            print("No previous book records found. Starting a fresh...")


    def delete_patron(self,search_type,input_value):
        self.load_patrons()
        if not self.patrons_list:
            print("KINDLY load your patrons first!")
            return None
        # Searching for the patron
        patron_matches = []
        try:
            with open('PatronManager.txt','r') as rf:
                patron_content = rf.readline()

                while patron_content:
                    final_patron_content = patron_content.rstrip("\n").split(",")
                    if len(final_patron_content) != 2:
                        print("Invalid data format!")
                        patron_content = rf.readline()
                        continue
                    # Unpacking and parsing values...
                    name,ID = final_patron_content
                    
                    if search_type == "name" and input_value in name:
                        patronInstance = Patron(name,ID)
                        patron_matches.append(patronInstance)

                    elif search_type == "ID" and input_value in ID:
                        patronInstance = Patron(name,ID)
                        patron_matches.append(patronInstance)

                    patron_content = rf.readline()

                # Handling search result
                if not patron_matches:
                    print("No matching patrons found!")
                    return None

                if len(patron_matches) > 1:
                        print("Here are the available patrons:-")
                        print()
                        for index, patron in enumerate(patron_matches, start=1):
                            print(f"{index}. Name: {patron.name}, ID: {patron.ID}")

                        print()

                        # Validating the input
                        while True:
                            choice = input("Enter the index of the patron to delete: ")
                            try:
                                int_choice = int(choice) - 1 # Convert input to zero-based index
                                if int_choice < 0 or int_choice >= len(patron_matches):
                                    print("Invalid input. Please choose a valid number.")
                                else:
                                    break

                            except ValueError:
                                print("Invalid input! Please enter a number.")

                        # Deleting the patron
                        patron_to_delete = patron_matches[int_choice]
                        for patron in self.patrons_list:
                            if patron.name == patron_to_delete.name and patron.ID == patron_to_delete.ID:
                                self.patrons_list.remove(patron)
                                break

                        # Updating the PatronManager text file
                        with open('PatronManager.txt','w') as wf:
                            for patron in self.patrons_list:
                                wf.write(f"{patron.name},{patron.ID}\n")
                        print()
                        # print("New Patrons List:",self.patrons_list)
                        print("Patron deleted successfully.")


                else:
                    # Deleting the patron
                    patron_to_delete = patron_matches[0]
                    for patron in self.patrons_list:
                        if patron.name == patron_to_delete.name and patron.ID == patron_to_delete.ID:
                            self.patrons_list.remove(patron)
                            break
                        
                    # Updating the PatronManager text file
                    with open('PatronManager.txt','w') as wf:
                        for patron in self.patrons_list:
                            wf.write(f"{patron.name},{patron.ID}\n")

                    print()

                    # Printing the patron_list content before writing to the file...
                    print("Patron deleted successfully.")
                    # print("New Patrons List:",self.patrons_list)
                     

        except FileNotFoundError:
            print("No previous patron records found. Starting a fresh...")

 

    def loan_book(self,patron_name,book_title): # Can also be named "add_loan"
        self.load_books() # Loads books to books_list
        self.load_patrons() # Loads patrons to patrons_list

        # Search for the patron
        patron = next((p for p in self.patrons_list if patron_name in p.name),None)
        if not patron:
            print(f"No patron found with name '{patron_name}'.")
            return None
        
        # Extracting patron name out of the whole patron object
        loaningPatronName = patron.name
        
        # Search for the book
        book = next((b for b in self.books_list if book_title in b.title),None)
        if not book:
            print(f"No book found with title '{book_title}'.")
            return None
        
        # Extracting book title out of the whole book object
        loanedBookTitle = book.title

        # Check if the book is already loaned
        for loan in self.loans_list:
            if loan.book_borrowed_title == loanedBookTitle:
                print(f"The book '{book_title}' is already loaned out.")
                return
            

        # Calculate dates
        date_borrowed = datetime.now().strftime("%Y-%m-%d")
        date_to_return = (datetime.now() + timedelta(days = 14)).strftime("%Y-%m-%d") # 2 weeks

        # Create loan object & add the loan 
        loan = Loan(loanedBookTitle,date_borrowed,date_to_return,loaningPatronName)
        self.loans_list.append(loan)

        # Print statement to show the loan was successful
        print(f"Book '{loanedBookTitle}' loaned to '{loaningPatronName}' on {date_borrowed}. Return by {date_to_return}.")

    

    def save_loan(self):
        file_path = "LoanManager.txt"
        file_empty = os.path.getsize(file_path) == 0  # Check if file is empty

        with open(file_path, "a") as wf:
            for loan in self.loans_list:
                line = f"{loan.book_borrowed_title}, {loan.borrow_date}, {loan.return_date}, {loan.associated_patron_name}"
                if not file_empty:
                    wf.write("\n" + line)  # Append on a new line if the file is not empty
                else:
                    wf.write(line)  # Write normally if it's the first entry
                    file_empty = False  # Ensure next writes append properly    

        
    def return_book(self,book_title): # Can also be named "delete_loan"
        # Find the loan for the given book
        loan = next((l for l in self.loans_list if l.book_borrowed.title == book_title),None)
        if not loan:
            print(f"No active loan found for book '{book_title}'.")
            return None
        
        # Remove the loan
        self.loans_list.remove(loan)
        print(f"Book '{book_title}' returned successfully.")

    def load_loans(self):
        try:
            with open('LoanManager.txt','r') as rf:
                loan_content = rf.readline()
                while loan_content:
                    final_loan_content = loan_content.rstrip("\n").split(",")
                    if len(final_loan_content) != 4:
                        print("Invalid data format!")
                        loan_content = rf.readline()
                        continue
                    book_borrowed_title, borrow_date, return_date, associated_patron_name = final_loan_content
                    loanInstance = Loan(book_borrowed_title, borrow_date, return_date, associated_patron_name)
                    self.loans_list.append(loanInstance)
                    loan_content = rf.readline() 


        except FileNotFoundError:
            print("No previous patron records found. Starting a fresh...")



    def list_loans(self):
        print("Active Loans:")
        for index, loan in enumerate(self.loans_list, start=1):
            print(f"{index}. Book: {loan.book_borrowed_title}, Borrow Date:{loan.borrow_date}, Return Date:{loan.return_date}, Patron:{loan.associated_patron_name}")
        
                 
    
def menu():

    library = Library()
    
    while True:
        print("\nLIBRARY MANAGEMENT SYSTEM")
        print()
        print("1. Add a Book (Admin Role)")
        print("2. Register a Patron (Admin Role)")
        print("3. Search a Book")
        print("4. Delete a Book (Admin Role)")
        print("5. Search a Patron")
        print("6. Delete a Patron (Admin Role)")
        print("7. View available Books")
        print("8. View available Patrons")
        print("9. Loan a Book (Admin Role)")
        print("10. Return a Book (Admin Role)")
        print("11. View Active Loans")
        print("*. Exit Programme")
        print()
        
        choice = input("Enter your choice: ")
        print()

        if choice == "1":
            password = getpass.getpass("This is an Admin's role. Please enter password: ")
            if password == "nedotaliban1861":
                title = input("Enter book title: ")
                author = input("Enter book author: ")
                ISBN = input("Enter book ISBN: ")
                book = Book(title,author,ISBN)
                library.add_book(book)
                library.save_books()
                print()
                print(f"{book.title} saved successfully!")
            else:
                print("Wrong password! Exiting programme.")
                print()
                break


        elif choice == "2":
            password = getpass.getpass("This is an Admin's role. Please enter password: ")
            if password == "nedotaliban1861":
                name = input("Enter patron name: ")
                ID = input("Enter patron ID: ")
                patron = Patron(name,ID)
                library.register_patron(patron)
                library.save_patrons()
                print()
                print(f"{patron.name} saved successfully!")
            else:
                print("Wrong Password! Exiting programme.")
                print()
                break

        elif choice == "3":
            search_type = input("Search by 'title', 'author' or 'ISBN': ")
            print()
            value = input("Enter search value (hint): ")
            print()
            book_matches = library.search_books(search_type,value)

            if not book_matches:
               print("No matching books found!")
            else:
                print("Here are the matching book(s):")
                print()
                for index, book in enumerate(book_matches, start=1):
                    print(f"{index}. Title: {book.title}, Author:{book.author}, ISBN:{book.ISBN}")
            print()

        elif choice == "4":
            password = getpass.getpass("This is an Admin's role. Please enter password: ")
            if password == "nedotaliban1861":
                search_type = input("Search by 'title', 'author' or 'ISBN': ")
                value = input("Enter search value (hint): ")
                library.delete_book(search_type,value)

            else:
                print("Wrong Password! Exiting programme.")
                print()
                break

        elif choice == "5":
            search_type = input("Search by 'name' or 'ID': ")
            print()
            value = input("Enter search value (hint): ")
            print()
            patron_matches = library.search_patrons(search_type, value)
            if not patron_matches:
               print("No matching patrons found!")
            else:
                print("Here are the matching patron(s):")
                print()
                for index, patron in enumerate(patron_matches, start=1):
                    print(f"{index}. Name: {patron.name}, ID:{patron.ID}")
            print()

        elif choice == "6":
            password = getpass.getpass("This is an Admin's role. Please enter password: ")
            if password == "nedotaliban1861":
                search_type = input("Search by 'name' or 'ID': ")
                value = input("Enter search value (hint): ")
                library.delete_patron(search_type, value)

            else:
                print("Wrong password! Exiting programme.")
                print()
                break

        elif choice == "7":
            if not library.books_list:
                library.load_books()

                if library.books_list:
                    print("Here are the availabe books:- \n")
                    library.list_books()

                if not library.books_list:
                    print("No books available in the library!")

            else:
                print("Here are the availabe books:- \n")
                library.list_books()

        elif choice == "8":
            if not library.patrons_list:
                library.load_patrons()

                if library.patrons_list:
                    print("Here are the available patrons:- \n")
                    library.list_patrons()

                if not library.patrons_list:
                    print("No patron has been registred!")

            else:
                print("Here are the available patrons:- \n")
                library.list_patrons()
            

        elif choice == "9":
            password = getpass.getpass("This is an Admin's role. Please enter password: ")
            if password == "nedotaliban1861":
                patron_name = input("Enter the name of the patron: ")
                book_title = input("Enter the title of the book: ")
                library.loan_book(patron_name,book_title)
                library.save_loan()

            else:
                print("Wrong password! Exiting programme.")
                print()
                break

        elif choice == "10":
            password = getpass.getpass("This is an Admin's role. Please enter password: ")
            if password == "nedotaliban1861":
                book_title = input("Enter the title of the book to return: ")
                library.return_book(book_title)

            else:
                print("Wrong password! Exiting programme.")
                print()
                break

        elif choice == "11":
            if not library.loans_list:
                library.load_loans()

                if library.loans_list:
                    print("Here are the active loans:- \n")
                    library.list_loans()

                if not library.loans_list:
                    print("No active loans in the library!")

            else:
                print("Here are the active loans:- \n")
                library.list_loans()

        elif choice == "*":
            print("Exiting the Library Management System. GoodBye!")
            break

        else:
            print("Invalid choice. Please try again!")


if __name__ == "__main__":
    menu()
