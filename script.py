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




# Late fee system




# Ratings system




# Collections







### toDo section for inviduell tasks... ###


