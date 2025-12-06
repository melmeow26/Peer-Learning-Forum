from tkinter import *
from tkinter import messagebox
import json
import os

class User:
    def __init__(self, user_id, name, password):
        self.user_id = user_id
        self.name = name
        self.password = password

class Student(User):
    def __init__(self, user_id, name, password):
        super().__init__(user_id, name, password)

class Teacher(User):
    def __init__(self, user_id, name, password):
        super().__init__(user_id, name, password)

class PeerLearningForum:
    def __init__(self):
        # File to store posts data
        self.data_file = "forum_data.json"
        
        # Initialize default posts structure
        self.default_posts_structure = [
            {
                "title": "How to prepare for Python exam?",
                "desc": "Any tips for revision and practice questions?",
                "user": "Melody Lee",
                "replies": [
                    {"text": "Try past year papers and review lecture notes.", "user": "Lim Wan Yoke"}
                ],
                "likes": 2,
                "liked_by": ["S001", "S002"]
            },
            {
                "title": "Share your favorite Python resource!",
                "desc": "What websites or YouTube channels help you learn Python?",
                "user": "Mr. Tan",
                "replies": [
                    {"text": "I recommend Real Python and Corey Schafer's YouTube channel.", "user": "Ng Wei Xian"}
                ],
                "likes": 3,
                "liked_by": ["S003", "S004", "T001"]
            }
        ]
        
        # Load all posts from file or use defaults
        self.all_posts = self.load_posts()
        
        self.users = {
            "S001": Student("S001", "Melody Lee", "melody123"),
            "S002": Student("S002", "Lim Wan Yoke", "lim123"),
            "S003": Student("S003", "Heng Yi Ching", "heng123"),
            "S004": Student("S004", "Tan Li Ying", "tan123"),
            "S005": Student("S005", "Chong Wei Ming", "chong123"),
            "S006": Student("S006", "Ng Wei Xian", "ng123"),
            "S007": Student("S007", "Lee Mei Ling", "lee123"),
            "S008": Student("S008", "Koh Hui Min", "koh123"),
            "S009": Student("S009", "Ong Siew Mei", "ong123"),
            "T001": Teacher("T001", "Mr. Tan", "tanadmin"),
            "T002": Teacher("T002", "Ms. Lim", "limadmin"),
            "T003": Teacher("T003", "Ms. Chia", "chiaadmin")
        }

        self.window = Tk()
        self.window.title("Peer Learning Forum")
        self.window.geometry("900x700")
        self.window.configure(bg="#fce4ec")  #background
        
        # Make sure to save data when the window is closed
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.current_user = None
        
        self.create_welcome_widgets()
        self.window.mainloop()

    def load_posts(self):
        """Load posts from the JSON file if it exists, otherwise use defaults"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    # Convert liked_by lists back to sets for consistency
                    for post in data:
                        post['liked_by'] = set(post['liked_by'])
                    return data
            except (json.JSONDecodeError, FileNotFoundError):
                # If file is corrupted, use default structure
                posts = self.default_posts_structure.copy()
                for post in posts:
                    post['liked_by'] = set(post['liked_by'])
                return posts
        else:
            # Use default structure if no file exists
            posts = self.default_posts_structure.copy()
            for post in posts:
                post['liked_by'] = set(post['liked_by'])
            return posts

    def save_posts(self):
        """Save all posts to the JSON file"""
        # Convert sets to lists for JSON serialization
        posts_to_save = []
        for post in self.all_posts:
            post_copy = post.copy()
            post_copy['liked_by'] = list(post['liked_by'])
            posts_to_save.append(post_copy)
            
        with open(self.data_file, 'w') as f:
            json.dump(posts_to_save, f, indent=4)

    def on_closing(self):
        """Save data when the application is closed"""
        self.save_posts()
        self.window.destroy()

    def create_welcome_widgets(self):
        # Clear the page
        for widget in self.window.winfo_children():
            widget.destroy()
            
        # Create welcome page
        welcome_frame = Frame(self.window, bg="#fce4ec")
        welcome_frame.pack(expand=True, fill=BOTH)
        
        # Add a header
        header_label = Label(welcome_frame, text="🌟 Welcome to the Peer Learning Forum 🌟", 
                           bg="#f8bbd0", fg="white", font=("Comic Sans MS", 20, "bold"),
                           pady=15, relief="raised", bd=3)
        header_label.pack(fill=X, pady=(0, 30))
        
        # Cute subtitle
        subtitle_label = Label(welcome_frame, text="Share knowledge, ask questions, and learn together!", 
                             bg="#fce4ec", fg="#880e4f", font=("Comic Sans MS", 14))
        subtitle_label.pack(pady=(0, 40))
        
        #login button 
        self.button = Button(welcome_frame, text="🎮 Login", command=self.show_login_frame, 
                           bg="#f48fb1", fg="white", font=("Comic Sans MS", 16, "bold"),
                           relief="raised", bd=3, padx=20, pady=10, cursor="hand2")
        self.button.pack(pady=20)
        
        # Add some decorative elements
        decor_frame = Frame(welcome_frame, bg="#fce4ec")
        decor_frame.pack(side=BOTTOM, pady=20)
        
        Label(decor_frame, text="💻 📚 🎓 ✏️ 📝", bg="#fce4ec", 
              fg="#ad1457", font=("Arial", 16)).pack()

    def show_login_frame(self):
        login_frame = Toplevel()
        login_frame.title("User Login")
        login_frame.geometry("400x350")
        login_frame.configure(bg="#fce4ec")
        login_frame.resizable(False, False)
        
        # Center the login window on the main window
        login_frame.transient(self.window)
        login_frame.grab_set()
        
        #center the login window
        self.window.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width() - 400) // 2
        y = self.window.winfo_y() + (self.window.winfo_height() - 250) // 2
        login_frame.geometry(f"400x350+{x}+{y}")
        
        # Create a main container to center the content
        main_container = Frame(login_frame, bg="#fce4ec")
        main_container.pack(expand=True, fill=BOTH)
        
        # login header
        header_label = Label(main_container, text="🔐 Login", bg="#f8bbd0", fg="white", 
                           font=("Comic Sans MS", 16, "bold"), pady=10, relief="raised", bd=2)
        header_label.pack(fill=X, pady=(0, 20))
        
        # Create a centered frame for the form
        form_container = Frame(main_container, bg="#fce4ec")
        form_container.pack(expand=True)
        
        # Login form with better spacing and centered
        form_frame = Frame(form_container, bg="#fce4ec")
        form_frame.pack(pady=10)
        
        # Configure grid weights for centering
        form_container.grid_columnconfigure(0, weight=1)
        form_container.grid_rowconfigure(0, weight=1)
        
        Label(form_frame, text="User ID:", bg="#fce4ec", fg="#880e4f", 
              font=("Comic Sans MS", 12)).grid(row=0, column=0, padx=10, pady=10, sticky=E)
        Label(form_frame, text="Password:", bg="#fce4ec", fg="#880e4f", 
              font=("Comic Sans MS", 12)).grid(row=1, column=0, padx=10, pady=10, sticky=E)

        self.user_id_var = StringVar()
        self.password_var = StringVar()

        Entry(form_frame, textvariable=self.user_id_var, width=20, 
              font=("Comic Sans MS", 11), bg="#f5f5f5").grid(row=0, column=1, padx=10, pady=10)
        Entry(form_frame, textvariable=self.password_var, show="*", width=20, 
              font=("Comic Sans MS", 11), bg="#f5f5f5").grid(row=1, column=1, padx=10, pady=10)

        Button(form_frame, text="Login", command=lambda: self.validate_login(login_frame), 
               bg="#f48fb1", fg="white", font=("Comic Sans MS", 12, "bold"),
               relief="raised", bd=2, padx=10, pady=3, cursor="hand2").grid(row=2, column=0, columnspan=2, pady=20)

    def validate_login(self, login_frame): #login validation
        uid = self.user_id_var.get()
        pwd = self.password_var.get()
        if uid in self.users and self.users[uid].password == pwd:
            user = self.users[uid]
            self.current_user = user
            login_frame.destroy()
            if isinstance(user, Student):
                messagebox.showinfo("Login Success", f"Welcome Student, {user.name}!")
            elif isinstance(user, Teacher):
                messagebox.showinfo("Login Success", f"Welcome Teacher/Admin, {user.name}!")
            self.open_peer_learning_page()
        else:
            messagebox.showerror("Login Failed", "Invalid user ID or password.")

    def open_peer_learning_page(self):
        # Clear the window
        for widget in self.window.winfo_children():
            widget.destroy()

    
        main_frame = Frame(self.window, bg="#fce4ec")
        main_frame.pack(fill=BOTH, expand=True)
        
        # Create a canvas for scrolling
        canvas = Canvas(main_frame, bg="#fce4ec", highlightthickness=0)
        scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg="#fce4ec")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Header with welcome message
        header_frame = Frame(scrollable_frame, bg="#f8bbd0", height=80, relief="raised", bd=2)
        header_frame.pack(fill=X, pady=(0, 15))
        header_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        welcome_label = Label(header_frame, 
                             text=f"🌸 Welcome to TARUMT Peer Learning Forum, {self.current_user.name}! 🌸", 
                             bg="#f8bbd0", fg="white", font=("Comic Sans MS", 16, "bold"))
        welcome_label.pack(expand=True)
        
        # Create a centered container for the content
        content_container = Frame(scrollable_frame, bg="#fce4ec")
        content_container.pack(expand=True, fill=BOTH, padx=20, pady=10)
        
        # Create post section
        post_frame = Frame(content_container, bg="#fce4ec", relief="groove", bd=2, padx=15, pady=15)
        post_frame.pack(fill=X, pady=10)
        
        Label(post_frame, text="💬 Create a New Post", bg="#fce4ec", fg="#880e4f", 
              font=("Comic Sans MS", 14, "bold")).grid(row=0, column=0, columnspan=2, sticky=W, pady=(0, 10))
        
        Label(post_frame, text="Title:", bg="#fce4ec", fg="#880e4f", 
              font=("Comic Sans MS", 12)).grid(row=1, column=0, sticky=W, pady=5)
        self.post_title = StringVar()
        Entry(post_frame, textvariable=self.post_title, width=40, 
              font=("Comic Sans MS", 11), bg="#f5f5f5").grid(row=1, column=1, padx=10, pady=5)
        
        Label(post_frame, text="Description:", bg="#fce4ec", fg="#880e4f", 
              font=("Comic Sans MS", 12)).grid(row=2, column=0, sticky=W, pady=5)
        self.post_desc = StringVar()
        Entry(post_frame, textvariable=self.post_desc, width=40, 
              font=("Comic Sans MS", 11), bg="#f5f5f5").grid(row=2, column=1, padx=10, pady=5)
        
        Button(post_frame, text="📝 Create Post", command=self.create_post, 
               bg="#f48fb1", fg="white", font=("Comic Sans MS", 12, "bold"),
               relief="raised", bd=2, padx=15, pady=5, cursor="hand2").grid(row=3, column=0, columnspan=2, pady=10)
        
        # Posts display area
        posts_label = Label(content_container, text="📋 Community Posts", bg="#fce4ec", 
                           fg="#880e4f", font=("Comic Sans MS", 14, "bold"))
        posts_label.pack(anchor=W, pady=(20, 10))
        
        self.posts_container = Frame(content_container, bg="#fce4ec")
        self.posts_container.pack(fill=BOTH, pady=(0, 20))
        
        # Logout button
        logout_frame = Frame(content_container, bg="#fce4ec")
        logout_frame.pack(fill=X, pady=10)
        
        logout_button = Button(logout_frame, text="🚪 Logout", command=self.logout, 
                              bg="#f48fb1", fg="white", font=("Comic Sans MS", 12, "bold"),
                              relief="raised", bd=2, padx=20, pady=5, cursor="hand2")
        logout_button.pack(pady=10)

        # Make the content container expand to center its children
        content_container.grid_columnconfigure(0, weight=1)
        for widget in content_container.winfo_children():
            if isinstance(widget, Frame):
                widget.grid_columnconfigure(1, weight=1)

        self.refresh_posts()

    def logout(self):
        # Save posts before logging out
        self.save_posts()
        self.current_user = None
        self.create_welcome_widgets()
        messagebox.showinfo("Logout", "You have been logged out successfully.")

    def create_post(self):
        title = self.post_title.get().strip()
        desc = self.post_desc.get().strip()

        if(len(title) > 100):
            messagebox.showwarning("Input Error", "Title cannot exceed 100 characters.")
            return

        if len(desc)>500:
            messagebox.showwarning("Input Error", "Description cannot exceed 500 characters.")
            return
        
        if title and desc:
            user = self.current_user
            self.all_posts.append({
                "title": title,
                "desc": desc,
                "user": user.name,
                "replies": [],
                "likes": 0,
                "liked_by": set()  # Track users who liked this post
            })
            self.post_title.set("")
            self.post_desc.set("")
            self.save_posts()  # Save after creating a new post
            self.refresh_posts()
        else:
            messagebox.showwarning("Input Error", "Both title and description are required.")

    def refresh_posts(self):
        for widget in self.posts_container.winfo_children():
            widget.destroy()
            
        if not self.all_posts:
            no_posts_label = Label(self.posts_container, text="No posts yet. Be the first to share something! 🌟", 
                                  bg="#fce4ec", fg="#880e4f", font=("Comic Sans MS", 12))
            no_posts_label.pack(pady=20)
        else:
            for idx, post in enumerate(self.all_posts):
                # Create a centered container for each post
                post_outer_frame = Frame(self.posts_container, bg="#fce4ec")
                post_outer_frame.pack(fill=X, pady=10)
                post_outer_frame.grid_columnconfigure(0, weight=1)
                
                # Create a cute post box that will be centered
                post_box = Frame(post_outer_frame, bg="white", relief="groove", bd=2)
                post_box.pack(fill=X, padx=5)
                
                # Post header with title and delete button
                header_frame = Frame(post_box, bg="#f3e5f5")
                header_frame.pack(fill=X, padx=10, pady=(10, 5))
                
                title_label = Label(header_frame, text=f"📌 {post['title']}", bg="#f3e5f5", 
                                   fg="#4a148c", font=("Comic Sans MS", 13, "bold"), anchor="w")
                title_label.pack(side=LEFT, fill=X, expand=True)
                
                # Add delete post button for admin users
                if isinstance(self.current_user, Teacher):
                    delete_post_btn = Button(header_frame, text="🗑️", font=("Arial", 10),
                                           command=lambda i=idx: self.delete_post(i),
                                           bg="#f3e5f5", fg="red", relief="flat", cursor="hand2")
                    delete_post_btn.pack(side=RIGHT, padx=5)
                
                # Post content
                content_frame = Frame(post_box, bg="white")
                content_frame.pack(fill=X, padx=15, pady=(0, 10))
                
                Label(content_frame, text=post['desc'], bg="white", 
                      font=("Comic Sans MS", 11), wraplength=700, justify=LEFT).pack(anchor="w")
                
                # Post footer with user info and like button
                footer_frame = Frame(post_box, bg="white")
                footer_frame.pack(fill=X, padx=15, pady=(0, 10))
                
                user_label = Label(footer_frame, text=f"👤 Posted by: {post['user']}", bg="white", 
                                  fg="#6a1b9a", font=("Comic Sans MS", 10, "italic"))
                user_label.pack(side=LEFT, anchor="w")
                
                # Like button and count
                like_frame = Frame(footer_frame, bg="white")
                like_frame.pack(side=RIGHT, anchor="e")
                
                # Check if current user has already liked this post
                user_has_liked = self.current_user.user_id in post['liked_by']
                
                like_button = Button(like_frame, text="👍" if not user_has_liked else "❤️", 
                                    command=lambda i=idx: self.add_like(i), 
                                    font=("Comic Sans MS", 10),
                                    bg="#e1bee7" if user_has_liked else "white",
                                    relief="raised", bd=1, cursor="hand2")
                like_button.pack(side=LEFT, padx=(10, 5))
                
                Label(like_frame, text=f"{post['likes']}", bg="white", 
                      font=("Comic Sans MS", 10)).pack(side=LEFT)
                
                # Replies section
                if post["replies"]:
                    replies_frame = Frame(post_box, bg="#f5f5f5", relief="sunken", bd=1)
                    replies_frame.pack(fill=X, padx=10, pady=(5, 10))
                    
                    Label(replies_frame, text="💬 Replies:", bg="#f5f5f5", 
                          font=("Comic Sans MS", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 5))
                    
                    for reply_idx, reply in enumerate(post["replies"]):
                        reply_frame = Frame(replies_frame, bg="#f5f5f5")
                        reply_frame.pack(fill=X, padx=15, pady=2)
                        
                        reply_text = Label(reply_frame, text=f"💭 {reply['text']}", bg="#f5f5f5", 
                                          font=("Comic Sans MS", 10), wraplength=650, justify=LEFT)
                        reply_text.pack(side=LEFT, anchor="w")
                        
                        reply_user = Label(reply_frame, text=f" - {reply['user']}", bg="#f5f5f5", 
                                          font=("Comic Sans MS", 9, "italic"), fg="#7b1fa2")
                        reply_user.pack(side=LEFT, padx=(5, 0))
                        
                        # Add delete reply button for admin users
                        if isinstance(self.current_user, Teacher):
                            delete_reply_btn = Button(reply_frame, text="🗑️", font=("Arial", 8),
                                                    command=lambda i=idx, r_i=reply_idx: self.delete_reply(i, r_i),
                                                    bg="#f5f5f5", fg="red", relief="flat", cursor="hand2")
                            delete_reply_btn.pack(side=RIGHT, padx=5)
                
                # Reply input section
                reply_input_frame = Frame(post_box, bg="white")
                reply_input_frame.pack(fill=X, padx=15, pady=(0, 15))
                
                reply_var = StringVar()
                reply_entry = Entry(reply_input_frame, textvariable=reply_var, width=50, 
                                   font=("Comic Sans MS", 10), bg="#f5f5f5")
                reply_entry.pack(side=LEFT, padx=(0, 10), fill=X, expand=True)
                
                Button(reply_input_frame, text="Reply", command=lambda i=idx, v=reply_var: self.add_reply(i, v), 
                      bg="#f48fb1", fg="white", font=("Comic Sans MS", 10, "bold"),
                      relief="raised", bd=1, cursor="hand2").pack(side=RIGHT)

    def add_like(self, post_index):
        post = self.all_posts[post_index]
        user_id = self.current_user.user_id
        
        # Check if user has already liked this post
        if user_id not in post['liked_by']:
            post['likes'] += 1
            post['liked_by'].add(user_id)
            self.save_posts()
            self.refresh_posts()
        else:
            messagebox.showinfo("Info", "You have already liked this post.")

    def add_reply(self, post_index, reply_var):
        reply = reply_var.get().strip()
        if reply:
            user = self.current_user
           
            self.all_posts[post_index]["replies"].append({"text": reply, "user": user.name})
            reply_var.set("")
            self.save_posts()
            self.refresh_posts()
            
    def delete_post(self, post_index):
        """Delete a post (admin only)"""
        if isinstance(self.current_user, Teacher):
            post = self.all_posts[post_index]
            confirm = messagebox.askyesno("Confirm Delete", 
                                         f"Are you sure you want to delete the post '{post['title']}'?")
            if confirm:
                self.all_posts.pop(post_index)
                self.save_posts()
                self.refresh_posts()
                messagebox.showinfo("Success", "Post deleted successfully.")
        else:
            messagebox.showerror("Permission Denied", "Only admin users can delete posts.")
            
    def delete_reply(self, post_index, reply_index):
        """Delete a reply (admin only)"""
        if isinstance(self.current_user, Teacher):
            post = self.all_posts[post_index]
            reply = post["replies"][reply_index]
            confirm = messagebox.askyesno("Confirm Delete", 
                                         f"Are you sure you want to delete this reply?")
            if confirm:
                post["replies"].pop(reply_index)
                self.save_posts()
                self.refresh_posts()
                messagebox.showinfo("Success", "Reply deleted successfully.")
        else:
            messagebox.showerror("Permission Denied", "Only admin users can delete replies.")


PeerLearningForum()