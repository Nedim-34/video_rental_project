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
        self.ratings = {}  # Dictionary to store ratings: {username: rating}

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
                        print(f"Thank you, {username}, for rating '{selected_video.title}'!")
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
            print(f"'{video.title}' has no ratings yet.")
            return

        average = sum(video.ratings.values()) / len(video.ratings)
        print(f"Average rating for '{video.title}': {average:.2f} out of 5 stars based on {len(video.ratings)} votes.")

    def list_all_videos(self):
        """Lists all videos with a number for selection."""
        print("\n--- All Videos ---")
        video_list = list(self.videos.values())
        if not video_list:
            print("No videos in the store.")
            return
        
        for i, video in enumerate(video_list):
            print(f"{i + 1}. Title: {video.title} | Genre: {video.genre}")

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

    def main_menu(self):
        """Main menu for the user to interact with the system."""
        while True:
            print("\n--- Video Store Menu ---")
            print("1. Rate a video")
            print("2. See average ratings")
            print("3. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                self.rate_video()
            elif choice == '2':
                self.show_all_average_ratings()
            elif choice == '3':
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

# Example of how to use the new functionality:
# Create a VideoStore instance and add videos to it.
store = VideoStore()

# Add the previously created videos as well
store.add_video(matrix)
store.add_video(memento)
store.add_video(jumanji)


# Add customers if needed
store.add_customer(customer1)
store.add_customer(customer2)

# Start the main menu
if __name__ == "__main__":
    store.main_menu()



# Collections







### toDo section for inviduell tasks... ###


