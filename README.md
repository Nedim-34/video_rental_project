🎬 Video Rental System
======================

### 🎯 Goal

Students will build a console-based system for renting movies, returning them, and managing members.

### 🔑 Learning Focus

*   **Classes**: `Video`, `Customer`, `VideoStore`
    
*   **Functions**: rent, return, search, list
    
*   **Collections**: use of `dict` and `list` for efficient management
    

🎯 Learning Objectives
----------------------

By the end of this project, students will be able to:

*   **Apply Object-Oriented Programming (OOP) principles** by creating and using classes (`Video`, `Customer`, `VideoStore`).
    
*   **Encapsulate functionality** inside methods (e.g., rent, return, search, list).
    
*   **Use Python collections** (`list`, `dict`) to store and retrieve structured data efficiently.
    
*   **Implement control flow** with conditions and loops to manage system operations.
    
*   **Design modular code** by splitting responsibilities across classes and functions.
    
*   **Collaborate in groups**, practice version control (if used), and present solutions.
    

🗓️ Weekly Breakdown
--------------------

### **Day 1: Define Classes**

*   `Video`: attributes → `title`, `genre`, `video_id`, `available` (bool).
    
*   `Customer`: attributes → `name`, `customer_id`, `rented_videos` (list).
    
*   `VideoStore`: manages collections of videos and customers.
    

### **Day 1–3: Implement Core Functions**

In the `VideoStore` class:

*   `add_video(video)` – add a new movie.
    
*   `add_customer(customer)` – register a new customer.
    
*   `rent_video(customer_id, video_id)` – customer rents if available.
    
*   `return_video(customer_id, video_id)` – customer returns a video.
    
*   `list_available_videos()` – show available movies.
    
*   `list_customer_videos(customer_id)` – show what a customer has rented.
    

### **Day 3–6: Extensions (Group Work)**

Encourage groups to add **one or two enhancements**:

*   **Search feature**: by title or genre.
    
*   **Late fee system**: calculate fee if not returned on time.
    
*   **Ratings system**: customers rate videos.
    
*   **Collections**: Use a `dict` for quick lookups (e.g. `video_id -> Video`).
    

### **Day 7: Presentation & Review**

*   Groups demo renting/returning videos.
    
*   Discuss use of **OOP + collections**.
    
*   Compare different extensions.