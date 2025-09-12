import hashlib
import colorama as clr
from datetime import datetime, timedelta

""" Video Rental Project """

### Define Classes ###

def gen_id(source: str):
    return hashlib.md5(source.encode()).hexdigest()[:6]

# Video attributes
class Video:
    def __init__(self, title, genre):
        self.title = title
        self.genre = genre
        self.video_id = gen_id(title + genre)
        self.available = True
        self.ratings = {}  # Dictionary to store ratings: {username: rating}

    def __str__(self):
        x, div, = 20, " : "
        sep = "\n" + (":" * (x + 2))
        ct = clr.Fore.LIGHTYELLOW_EX
        c = clr.Fore.LIGHTGREEN_EX if self.available else clr.Fore.LIGHTRED_EX
        r = clr.Fore.RESET
        t = f"\n{'Title':>{x}}{div}{ct}{self.title:<}{r}"
        g = f"\n{'Genre':>{x}}{div}{self.genre:<}"
        i = f"\n{'ID':>{x}}{div}{self.video_id:<}"
        a = f"\n{'Available':>{x}}{div}{c}{str(self.available):<}{r}"
        return f"{sep}{t}{g}{i}{a}{sep}"
    
    def __repr__(self):
        return "title={}, genre={}, video_id={}, available={}".format(
            self.title,
            self.genre,
            self.video_id,
            self.available)

# Customer: attributes
class Customer:
    _id_counter = 1  # class-level counter for sequential IDs

    def __init__(self, name, rented_videos=None):
        self.customer_id = f"{Customer._id_counter:04d}"  # 0001, 0002, ...
        Customer._id_counter += 1
        self.name = name
        self.rented_videos = rented_videos if rented_videos else []

    def __str__(self):
        x, div = 20, " : "
        sep = "\n" + (":" * (x + 2))
        name_color = clr.Fore.CYAN
        rented_color = clr.Fore.RED
        none_color = clr.Fore.LIGHTGREEN_EX
        reset = clr.Fore.RESET

        # Name line
        name_line = f"\n{'Name':>{x}}{div}{name_color}{self.name:<}{reset}"
        # ID line
        id_line = f"\n{'ID':>{x}}{div}{self.customer_id:<}"
        # Rented line
        if not self.rented_videos:
            rented_info = f"{none_color}None{reset}"
        else:
            rented_info = ", ".join(
                f"{rental['video'].title} (Due: {rental['due_date'].strftime('%b %d, %Y')})"
                for rental in self.rented_videos
            )
            rented_info = f"{rented_color}{rented_info}{reset}"
        rented_line = f"\n{'Rented':>{x}}{div}{rented_info}"

        return f"{sep}{name_line}{id_line}{rented_line}{sep}"

# video store
class VideoStore:
    """Manages the collection of videos and customers."""
    def __init__(self, videos={}, customers={}):
        self.videos = videos
        self.customers = customers

### Implement Core Functions ###
# In the VideoStore class: 1-2

    def add_video(self, video_obj):
        if isinstance(video_obj, Video):
            self.videos[video_obj.video_id] = video_obj
            print(clr.Fore.GREEN + f"Successfully added video: {video_obj.title}" + clr.Fore.RESET)
            return True
        return False

    def add_customer(self, customer_obj):
        if isinstance(customer_obj, Customer):
            self.customers[customer_obj.customer_id] = customer_obj
            print(clr.Fore.GREEN + f"Successfully added customer: {customer_obj.name} with ID {customer_obj.customer_id}" + clr.Fore.RESET)
            return True
        return False

    def _find_video(self, identifier):
        """Helper function to find a video by ID or title (case-insensitive)."""
        # Try to find by video_id first
        video = self.videos.get(identifier)
        if video:
            return video
        
        # If not found by ID, try to find by title
        for video in self.videos.values():
            if video.title.lower() == identifier.lower():
                return video
        
        return None

### In the VideoStore class: 3-4 ###
# rent_video(customer_id, video_id) – customer rents if available.
    def rent_video(self, customer_id, video_identifier, rental_days=3):
        customer = self.customers.get(customer_id)
        video = self._find_video(video_identifier)

        if not customer:
            print(clr.Fore.RED + f"Customer {customer_id} not found." + clr.Fore.RESET)
            return
        if not video:
            print(clr.Fore.RED + f"Video '{video_identifier}' not found." + clr.Fore.RESET)
            return

        if video.available:
            video.available = False
            rental_date = datetime.now()
            due_date = rental_date + timedelta(days=rental_days)
            customer.rented_videos.append({
                "video": video,
                "rental_date": rental_date,
                "due_date": due_date
            })
            print(clr.Fore.GREEN + f"{customer.name} rented {video.title}. Due on {due_date.date()}." + clr.Fore.RESET)
        else:
            print(clr.Fore.RED + f"{video.title} is not available." + clr.Fore.RESET)

# return_video(customer_id, video_id) – customer returns a video.
    def return_video(self, customer_id, video_identifier):
        customer = self.customers.get(customer_id)
        video_to_return = self._find_video(video_identifier)

        if not customer:
            print(clr.Fore.RED + f"Customer {customer_id} not found." + clr.Fore.RESET)
            return
        if not video_to_return:
            print(clr.Fore.RED + f"Video '{video_identifier}' not found." + clr.Fore.RESET)
            return

        # Find the rental dict for this video
        rental_entry = next((rental for rental in customer.rented_videos if rental["video"].video_id == video_to_return.video_id), None)

        if rental_entry:
            video_to_return.available = True
            customer.rented_videos.remove(rental_entry)
            fee = self.calculate_late_fee(rental_entry["due_date"])
            if fee > 0:
                print(clr.Fore.RED + f"{customer.name} returned {video_to_return.title}. LATE! Fee: €{fee:.2f}" + clr.Fore.RESET)
            else:
                print(clr.Fore.GREEN + f"{customer.name} returned {video_to_return.title} on time." + clr.Fore.RESET)
        else:
            print(clr.Fore.YELLOW + f"{customer.name} did not rent {video_to_return.title}." + clr.Fore.RESET)

# In the VideoStore class: 5-6
    def list_all_customers(self):
        """Lists all customers with their ID and name."""
        print("\n--- All Customers ---")
        print("–––––––––––––––––––––––––––––––––––––––") 
        if not self.customers:
            print("No customers in the system.")
            return

        for customer in self.customers.values():
            print(f"ID: {customer.customer_id} | Name: {customer.name}")
        print("–––––––––––––––––––––––––––––––––––––––") 

    def list_available_videos(self):
        """Shows a list of all available videos."""
        print("\n--- Available Videos ---")
        available_count = 0
        for video in self.videos.values():
            if video.available:
                print(f"ID: {video.video_id} | Title: {video.title} | Genre: {video.genre}")
                available_count += 1
        if available_count == 0:
            print("There are currently no videos available.")

    def list_customer_videos(self, customer_id):
        """Shows a list of videos a customer has rented."""
        customer = self.customers.get(customer_id)
        if not customer:
            print(clr.Fore.RED + f"Error: Customer with ID {customer_id} not found." + clr.Fore.RESET)
            return

        print(f"\n--- Videos Rented by {customer.name} ---")
        if customer.rented_videos:
            for video_entry in customer.rented_videos:
                video = video_entry['video']
                print(f"ID: {video.video_id} | Title: {video.title} | Genre: {video.genre}")
        else:
            print(f"{customer.name} has not rented any videos.")


### Extensions (Group Work) ###
# Search feature

    def search_video(self, title=None, genre=None, separate_lists=False):
        match_title = []
        match_genre = []
        if title is None and genre is None:
            self.list_available_videos()
        else:
            for video in self.videos.values():
                if title:
                    lib_title = video.title.lower()
                    vid_title = title.lower()
                    if lib_title == vid_title or vid_title in lib_title:
                        match_title.append(video)
                if genre:
                    lib_genre = video.genre.lower()
                    vid_genre = genre.lower()
                    if lib_genre == vid_genre or vid_genre in lib_genre:
                        match_genre.append(video)
        if separate_lists:
            return (match_title, match_genre)
        else:
            matches = {vid.video_id: vid for vid in match_title + match_genre}
            return list(matches.values())

# Collections    
    def get_video(self, video_id):
        return self.videos.get(video_id)
    
# Late fee system    
    def calculate_late_fee(self, due_date, fee_per_day=1.50):
        """Calculates a late fee based on the due date."""
        today = datetime.now()
        if today > due_date:
            days_late = (today - due_date).days
            return days_late * fee_per_day
        return 0.0


# Ratings system
    def rate_video(self):
        """Allows a user to rate a video and shows the average rating."""
        while True:
            self.list_all_videos()
            user_input = input("Enter the number of the video you want to rate (or 'q' to quit): ").strip()

            if user_input.lower() == 'q':
                print(clr.Fore.GREEN + "Thank you for using our rating system! We hope to see you again soon." + clr.Fore.RESET)
                return

            if not user_input.isdigit():
                print(clr.Fore.RED + "Invalid input. Please enter a number." + clr.Fore.RESET)
                continue
            
            try:
                choice = int(user_input)
                video_list = list(self.videos.values())
                if 1 <= choice <= len(video_list):
                    selected_video = video_list[choice - 1]
                    username = input("Enter your username: ").strip()
                    if not username:
                        print(clr.Fore.RED + "Username cannot be empty." + clr.Fore.RESET)
                        continue
                    
                    rating_input = input(f"Enter your rating for '{selected_video.title}' (1-5): ").strip()

                    if not rating_input.isdigit():
                        print(clr.Fore.RED + "Invalid input. Please enter a number between 1 and 5." + clr.Fore.RESET)
                        continue
                    
                    rating = int(rating_input)
                    if 1 <= rating <= 5:
                        selected_video.ratings[username] = rating
                        print(clr.Fore.CYAN + f"Thank you, {username}, for rating '{selected_video.title}'!" + clr.Fore.RESET)
                        self.show_average_rating(selected_video)
                    else:
                        print(clr.Fore.RED + "Invalid rating. Please enter a number between 1 and 5." + clr.Fore.RESET)
                else:
                    print(clr.Fore.RED + "Invalid number. Please choose a video from the list." + clr.Fore.RESET)
            except ValueError:
                print(clr.Fore.RED + "Invalid input. Please enter a valid number." + clr.Fore.RESET)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    def show_average_rating(self, video):
        """Calculates and prints the average rating for a given video."""
        if not video.ratings:
            print(clr.Fore.YELLOW + f"'{video.title}' has no ratings yet." + clr.Fore.RESET)
            return

        average = sum(video.ratings.values()) / len(video.ratings)
        print(clr.Fore.GREEN + f"Average rating for '{video.title}': {average:.2f} out of 5 stars based on {len(video.ratings)} votes." + clr.Fore.RESET)

    def list_all_videos(self):
        """Lists all videos with a number for selection."""
        print("\n--- All Videos ---")
        video_list = list(self.videos.values())
        if not video_list:
            print("No videos in the store.")
            return

        for i, video in enumerate(video_list):
            print(f"ID: {video.video_id} | Title: {video.title} | Genre: {video.genre}")

    def show_all_average_ratings(self):
        """Shows the average rating for all videos."""
        print("\n--- Average Ratings for All Videos ---")
        if not self.videos:
            print("No videos in the store to rate.")
            return

        for video in self.videos.values():
            if video.ratings:
                average = sum(video.ratings.values()) / len(video.ratings)
                print(f"'{video.title}': {average:.2f} stars ({len(video.ratings)} ratings)")
            else:
                print(f"'{video.title}': No ratings yet.")

# Menu System
    def start_menu(self):
        """The main entry point for the video store application."""
        while True:
            print("\n--- 📼 Welcome to Video Store 📼 ---")
            print("\n1. Video Management")
            print("2. Customer Management")
            print("3. Rent/Return Videos")
            print("4. Search & List")
            print("5. Video Ratings")
            print("6. Exit")
            print("-----------------------------------------------")
            choice = input("\nEnter your choice: ").strip()
            print()
            
            if choice == '1':
                self.video_management_menu()
            elif choice == '2':
                self.customer_management_menu()
            elif choice == '3':
                self.rent_return_menu()
            elif choice == '4':
                self.search_menu()
            elif choice == '5':
                self.video_ratings_menu()
            elif choice == '6':
                confirm = input("‼️ Are you sure you want to exit? (y/n): ").strip().lower()
                if confirm == 'y':
                    print("👋 Goodbye!")
                    break
                elif confirm == 'n':
                    continue
                else:
                    print(clr.Fore.RED + "🚫 Invalid input. Please type 'y' or 'n'." + clr.Fore.RESET)
            else:
                print(clr.Fore.RED + "🚫 Invalid choice. Please enter 1, 2, or 3." + clr.Fore.RESET)

    def video_management_menu(self):
        """Menu for managing video rentals."""
        while True:
            print("\n--- 🎬 Video Management Menu 🎬 ---")
            print("–––––––––––––––––––––––––––––––––––––––") 
            print("| 1. Add a new video                  |")
            print("| 2. List of all videos               |")
            print("| 3. List all available videos        |")
            print("| 4. Back to Main Menu                |")
            print("–––––––––––––––––––––––––––––––––––––––") 
            choice = input("\nEnter your choice: ").strip()

            if choice == '1':
                self.add_video_menu()
            elif choice == '2':
                self.list_all_videos()
            elif choice == '3':
                self.list_available_videos()
            elif choice == '4':
                break
            else:
                print(clr.Fore.RED + "🚫 Invalid choice. Please enter a number from 1 to 4." + clr.Fore.RESET)

    def customer_management_menu(self):
        """Menu for managing video rentals."""
        while True:
            print("\n  --- 👤 Customer Management Menu 👤 ---")
            print("–––––––––––––––––––––––––––––––––––––––") 
            print("| 1. Add a new customer               |")
            print("| 2. List all customers               |")
            print("| 3. List a customer's rented videos  |")
            print("| 4. Back to Main Menu                |")
            print("–––––––––––––––––––––––––––––––––––––––") 
            choice = input("\nEnter your choice: ").strip()

            if choice == '1':
                self.add_customer_menu()
            elif choice == '2':
                self.list_all_customers()
            elif choice == '3':
                self.list_all_customers()
                customer_id = input("Enter customer ID: ").strip()
                self.list_customer_videos(customer_id)
            elif choice == '4':
                break
            else:
                print(clr.Fore.RED + "🚫 Invalid choice. Please enter a number from 1 to 4." + clr.Fore.RESET)

    def rent_return_menu(self):
        """Menu for managing video rentals."""
        while True:
            print("\n  --- 📀 Rent & Return Menu 📀 ---")
            print("–––––––––––––––––––––––––––––––––––––––") 
            print("| 1. Rent a video                     |")
            print("| 2. Return a video                   |")
            print("| 3. Back to Main Menu                |")
            print("–––––––––––––––––––––––––––––––––––––––") 
            choice = input("\nEnter your choice: ").strip()

            if choice == '1':
                self.list_all_customers()
                customer_id = input("Enter customer ID to rent: ").strip()
                video_identifier = input("Enter video name or ID to rent: ").strip()
                self.rent_video(customer_id, video_identifier)
            elif choice == '2':
                self.list_all_customers()
                customer_id = input("Enter customer ID to return: ").strip()
                self.list_customer_videos(customer_id)
                video_identifier = input("Enter video name or ID to return: ").strip()
                self.return_video(customer_id, video_identifier)
            elif choice == '3':
                break
            else:
                print(clr.Fore.RED + "🚫 Invalid choice. Please enter a number from 1 to 3." + clr.Fore.RESET)


    def search_menu(self):
        """Menu for searching videos."""
        while True:
            print("\n     --- 🔎 Search Menu 🔎 ---")
            print("–––––––––––––––––––––––––––––––––––––––") 
            print("| 1. Search by title                  |")
            print("| 2. Search by genre                  |")
            print("| 3. Available videos                 |")
            print("| 4. Rented videos                    |")
            print("| 5. Back to Main Menu                |")
            print("–––––––––––––––––––––––––––––––––––––––") 
            choice = input("\nEnter your choice: ").strip()

            if choice == '1':
                title_query = input("Enter video title to search for: ").strip()
                results = self.search_video(title=title_query)
                if results:
                    print(f"\n--- 🔎 Results for '{title_query}' ---")
                    for video in results:
                        print(video)
                else:
                    print(clr.Fore.RED + f"🚫 No videos found with the title '{title_query}'." + clr.Fore.RESET)
            elif choice == '2':
                genre_query = input("Enter video genre to search for: ").strip()
                results = self.search_video(genre=genre_query)
                if results:
                    print(f"\n--- 🔎 Results for '{genre_query}' genre ---")
                    for video in results:
                        print(video)
                else:
                    print(clr.Fore.RED + f"🚫 No videos found in the genre '{genre_query}'." + clr.Fore.RESET)
            elif choice == '3':
                self.list_available_videos()
            elif choice == '4':
                self.list_all_customers()
                customer_id = input("Enter customer ID: ").strip()
                self.list_customer_videos(customer_id)
            elif choice == '5':
                break
            else:
                print(clr.Fore.RED + "🚫 Invalid choice. Please enter a number from 1 to 9." + clr.Fore.RESET)


    def add_video_menu(self):
        """Menu for adding a new video with confirmation."""
        print("\n--- ➕ Add a New Video ---")
        title = input("Enter the title of the video: ").strip()
        genre = input("Enter the genre of the video: ").strip()

        print("\n--- Confirmation ---")
        print(f"Title: {title}")
        print(f"Genre: {genre}")

        confirmation = input("Are you sure you want to add this video? (y/n): ").strip().lower()
        if confirmation == 'y':
            new_video = Video(title, genre)
            self.add_video(new_video)
        elif confirmation == 'n':
            print(clr.Fore.YELLOW + "Video not added. Returning to menu." + clr.Fore.RESET)
        else:
            print(clr.Fore.RED + "Invalid input. Video not added. Returning to menu." + clr.Fore.RESET)
    
    def add_customer_menu(self):
        """Menu for adding a new customer with confirmation."""
        print("\n--- 👤 Add a New Customer ---")
        name = input("Enter the full name of the customer: ").strip()

        if not name:
            print(clr.Fore.RED + "Name cannot be empty. Returning to menu." + clr.Fore.RESET)
            return

        print("\n--- Confirmation ---")
        print(f"Customer Name: {name}")
        confirmation = input("Are you sure you want to add this customer? (y/n): ").strip().lower()

        if confirmation == 'y':
            new_customer = Customer(name)
            self.add_customer(new_customer)
        elif confirmation == 'n':
            print(clr.Fore.YELLOW + "Customer not added. Returning to menu." + clr.Fore.RESET)
        else:
            print(clr.Fore.RED + "Invalid input. Customer not added. Returning to menu." + clr.Fore.RESET)

    def video_ratings_menu(self):
        """Submenu for handling video ratings."""
        while True:
            print("\n--- ⭐ Video Ratings Menu ⭐ ---")
            print("1. Rate a video")
            print("2. See average ratings")
            print("3. Back to Main Menu")
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                self.rate_video()
            elif choice == '2':
                self.show_all_average_ratings()
            elif choice == '3':
                break
            else:
                print(clr.Fore.RED + "🚫 Invalid choice. Please enter 1, 2, or 3." + clr.Fore.RESET)

# Initializing and running the store
if __name__ == "__main__":
    store = VideoStore()

    # Initial videos
    store.add_video(Video("Matrix", "Sci-Fi"))
    store.add_video(Video("Memento", "Thriller"))
    store.add_video(Video("Jumanji", "Adventure"))
    
    
    # Quick video lookup by video_id
    vid = store.get_video("e4ca63")
    vid2 = store.get_video(gen_id(" mAtrix"+ "sci-Fi")) #in case you have no video_id / using title + genre
    #print(f"\n Video found by video_id: ",vid)
    #print(f"\n Video found by video_id: ",vid2)


    # Initial customers
    customer1 = Customer("Harvey Dent")
    customer2 = Customer("Tony Sopranos")
    store.add_customer(customer1)
    store.add_customer(customer2)

    print("\n -----------------------------------------------------------")
    print("|                                                            |")
    print("| .-——.     .––-.   .-----.   \-\     /-/   |-|   |-|____|   |")
    print("| | |\ \   / /| |   | |-| |    \ \   / /    | |   | |____    |")
    print("| | |  \ \/ / | |   | |-| |     \ \_/ /     | |   | |____|   |")
    print("| | |   \__/  | |   | |-| |      \   /      | |   | |____    |")
    print("| |_|         |_|   ._____.       \_/       |_|   |______|   |")
    print("|                                                            |")
    print(" -----------------------------------------------------------")


    # Start the main application menu
    store.start_menu()







### toDo section for inviduell tasks... ###


