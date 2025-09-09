import colorama as clr
import hashlib

""" Video Rental Project"""


### Define Classes ###

def gen_id(source: str):
    return hashlib.md5(source.encode()).hexdigest()[:6]


# Video attributes
class Video:
    def __init__(self, title, genre):
        self.title = title
        self.genre = genre
        self.video_id = gen_id(title+genre)
        self.available = True

    def __str__(self):
        x, div, = 20, " : "
        sep = "\n" + (":" * (x+2))
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

matrix = Video("Matrix", "Sci-Fi")
matrix.available=False
print(matrix)
print(repr(matrix))

memento = Video("Memento", "Thriller")
print(memento)

jumanji = Video("Jumanji", "Adventure")
print(jumanji)



# Customer: attributes
class Customer:
    def __init__(self, name, rented_videos=[]): #needs to be an empty list, for customer creation
        self.customer_id = gen_id(name)
        self.name = name
        self.rented_videos = rented_videos

    def __str__(self):
        rented_titles = [video.title for video in self.rented_videos]
        return f"ID = {self.customer_id} | Name = {self.name} | Rented = {rented_titles}"
        
customer1 = Customer("Harvey Dent", [matrix])
customer2 = Customer("Tony Sopranos", [jumanji, memento])

print(customer1)
print(customer2)




# video store
class VideoStore:
    """Manages the collection of videos and customers."""
    def __init__(self, videos={}, customers={}):         #while creating new VideoStore, no data will be needed
        self.videos = videos                             #default: empty dictionary / will be handled by add_video function
        self.customers = customers                       #default: empty dictionary / will be handled by add_customer function


### Implement Core Functions ###
# In the VideoStore class: 1-2

    def add_video(self, video_obj):
        if isinstance(video_obj, Video):
            self.videos[video_obj.video_id] = video_obj

            
    def add_customer(self, customer_obj):
        if isinstance(customer_obj, Customer):
            self.customers[customer_obj.customer_id] = customer_obj
        


### In the VideoStore class: 3-4 ###
# rent_video(customer_id, video_id) – customer rents if available.
    def rent_video(self, customer_id, video_id):
        customer = self.customers.get(customer_id)
        video = self.videos.get(video_id)

        if not customer:
            print(f"Customer {customer_id} not found.")
            return
        if not video:
            print(f"Video {video_id} not found.")
            return
        
        if video.available:
            video.available = False
            customer.rented_videos.append(video)
            print(f"{customer.name} rented {video.title}.")
        else:
            print(f"{video.title} is not available.")


# return_video(customer_id, video_id) – customer returns a video.
    def return_video(self, customer_id, video_id):
        customer = self.customers.get(customer_id)
        video = self.videos.get(video_id)

        if not customer:
            print(f"Customer {customer_id} not found.")
            return
        if not video:
            print(f"Video {video_id} not found.")
            return
        
        if video in customer.rented_videos:
            video.available = True
            customer.rented_videos.remove(video)
            print(f"{customer.name} returned {video.title}.")
        else:
            print(f"{customer.name} did not rent {video.title}.")


# In the VideoStore class: 5-6
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
            print(f"Error: Customer with ID {customer_id} not found.")
            return

        print(f"\n--- Videos Rented by {customer.name} ---")
        if customer.rented_videos:
            for video in customer.rented_videos:
                print(f"ID: {video.video_id} | Title: {video.title} | Genre: {video.genre}")
        else:
            print(f"{customer.name} has not rented any videos.")


### Extensions (Group Work) ###
# Search feature

    def search_video(self, title=None, genre=None, separate_lists=False):
        match_title = []
        match_genre = []
        if title == None and genre == None:
            self.list_available_videos()
        else:
            for id,video in self.videos.items():
                video: Video = video
                if title != None:
                    lib_title = video.title.lower()
                    vid_title = title.lower()
                    if lib_title == vid_title or lib_title in vid_title or vid_title in lib_title:
                        match_title.append(video)
                if genre != None:
                    lib_genre = video.genre.lower()
                    vid_genre = genre.lower()
                    if lib_genre == vid_genre or lib_genre in vid_genre or vid_genre in lib_genre:
                        match_genre.append(video)
        if separate_lists:  
            return (match_title, match_genre)
        else:
            matches = {}
            for vid in match_title:
                vid:Video = vid
                matches[vid.video_id] = vid
            for vid in match_genre:
                vid:Video = vid
                matches[vid.video_id] = vid
            return list(matches.values())


# Late fee system




# Ratings system
movies = {
    "The Matrix - Sci-Fi - 1999": {
        "ratings": [],
        "raters": [""]
    },
    "Inception - Sci-Fi - 2010": {
        "ratings": [],
        "raters": [""]
    },
    "Memento - Thriller - 2000": {
        "ratings": [],
        "raters": [""]
    },
    "Jumanji - Adventure - 2017": {
        "ratings": [],
        "raters": [""]
    }
}

def add_rating(movie_title, user_name, rating):
    """
    Adds a new rating for a movie.

    Args:
        movie_title (str): The title of the movie.
        user_name (str): The username of the rater.
        rating (int): The rating score (1-5).
    """
    # The rest of this function remains the same
    if movie_title not in movies:
        movies[movie_title] = {"ratings": [], "raters": []}
        print(f"🎬 New movie '{movie_title}' added to the board.")

    if user_name in movies[movie_title]["raters"]:
        print(f"🚫 Sorry, {user_name}, you have already rated '{movie_title}'.")
        return

    if not 1 <= rating <= 5:
        print("⚠️  Invalid rating. Please enter a score between 1 and 5.")
        return

    movies[movie_title]["ratings"].append(rating)
    movies[movie_title]["raters"].append(user_name)
    print(f"✅ {user_name} has successfully rated '{movie_title}' with a score of {rating}.")

def get_average_rating(movie_title):
    """
    Calculates and prints the average rating for a movie.

    Args:
        movie_title (str): The title of the movie.
    """
    # The rest of this function remains the same
    if movie_title not in movies:
        print(f"🧐 '{movie_title}' is not on the board yet.")
        return

    ratings = movies[movie_title]["ratings"]
    if not ratings:
        print(f"✨ '{movie_title}' has no ratings yet.")
        return

    average = sum(ratings) / len(ratings)
    formatted_average = "{:.1f}".format(average)
    
    print(f"📊 The average rating for '{movie_title}' is {formatted_average} "
          f"based on {len(ratings)} ratings.")

def list_movies():
    """
    Prints a list of all movies currently on the board with a number.
    """
    if not movies:
        print("There are no movies on the board yet.")
    else:
        print("\n--- Movies on the Board ---")
        # Use enumerate to get both the index and the movie title
        for i, movie_title in enumerate(movies.keys()):
            print(f"{i + 1}. {movie_title}") # Start numbering from 1
        print("---------------------------")

def add_movie():
    """
    Prompts the user for a new movie title and adds it to the board.
    """
    # This function remains the same
    movie_title = input("Enter the (title - genre - year of publication) of the new movie: ")
    if movie_title in movies:
        print(f"🚫 The movie '{movie_title}' is already on the board.")
    else:
        movies[movie_title] = {"ratings": [], "raters": []}
        print(f"✅ '{movie_title}' has been added to the board. It's now ready to be rated!")

def get_movie_by_number(prompt):
    """
    Helper function to get a movie title from a user's number choice.
    Returns the movie title or None if the choice is invalid.
    """
    list_movies()  # Show the numbered list of movies first
    try:
        # Get the list of movie titles
        movie_titles = list(movies.keys())
        choice = int(input(prompt))
        # Validate that the choice is within the valid range
        if 1 <= choice <= len(movie_titles):
            # Return the movie title from the list based on the user's choice
            return movie_titles[choice - 1] # Use choice - 1 to get the correct index
        else:
            print("🚫 Invalid number. Please choose a number from the list.")
            return None
    except ValueError:
        print("🚫 Invalid input. Please enter a number.")
        return None

def main_menu():
    """
    Displays the main menu and handles user input.
    """
    while True:
        print("\n--- Movie Ratings System ---")
        print("1. Add a rating")
        print("2. Get a movie's average rating")
        print("3. List all movies")
        print("4. Add a new movie")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            # Use the new helper function to get the movie title
            movie_title = get_movie_by_number("Enter the number of the movie you want to rate: ")
            if movie_title: # Only proceed if a valid movie was selected
                user_name = input("Enter your username: ")
                try:
                    rating = int(input("Enter your rating (1-5): "))
                    add_rating(movie_title, user_name, rating)
                except ValueError:
                    print("🚫 Invalid input. Please enter a number for the rating.")
        
        elif choice == '2':
            # Use the new helper function to get the movie title
            movie_title = get_movie_by_number("Enter the number of the movie to get its average rating: ")
            if movie_title:
                get_average_rating(movie_title)
            
        elif choice == '3':
            list_movies()
            
        elif choice == '4':
            add_movie()

        elif choice == '5':
            print("👋 Goodbye!")
            break
            
        else:
            print("🚫 Invalid choice. Please try again.")

# Run the main menu
if __name__ == "__main__":
    main_menu()



# Collections







### toDo section for inviduell tasks... ###


