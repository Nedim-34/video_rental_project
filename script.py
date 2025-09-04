import colorama as clr

""" Video Rental Project"""


### Define Classes ###
# Video attributes

class Video:
    def __init__(self, title, genre, video_id):
        self.title = title
        self.genre = genre
        self.video_id = video_id
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

matrix = Video("M A T R I X", "Sci-Fi", "670267")
matrix.available=False
print(matrix)
print(repr(matrix))

memento = Video("M E M E N T O", "Thriller", "195647")
print(memento)

jumanji = Video("J U M A N J I", "Adventure", "850985")
print(jumanji)



# Customer: attributes





# video store


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




