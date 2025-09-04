""" Video Rental Project"""


### Define Classes ###
# Video attributes




# Customer: attributes
class Customer:
    def __init__(self, customer_id, name, rented_videos: list):
        self.customer_id = customer_id
        self.name = name
        self.rented_videos = rented_videos

    def __str__(self):
        return f"ID = {self.customer_id} | Name = {self.name} | Rented = {self.rented_videos}"
        
customer1 = Customer("0001", "Harvey Dent", ["The Great Gatsby", "The Matrix"])
customer2 = Customer("0002", "Tony Sopranos", ["Your Name", "Game of Thrones", "Oldboy"])

print(customer1)
print(customer2)




# video store
class VideoStore:
    """Manages the collection of videos and customers."""
    def __init__(self, video_id, customer_id):
        self.videos = {video_id}  
        self.customers = {customer_id}  

### Implement Core Functions ###
# In the VideoStore class: 1-2




# In the VideoStore class: 3-4




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




