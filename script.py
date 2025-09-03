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
    def __init__(self):
        self.videos = {video_id}  
        self.customers = {customer_id}  

### Implement Core Functions ###
# In the VideoStore class: 1-2




# In the VideoStore class: 3-4




# In the VideoStore class: 5-6




### Extensions (Group Work) ###
# Search feature




# Late fee system




# Ratings system




# Collections







### toDo section for inviduell tasks... ###




