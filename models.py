"""
Data models and in-memory storage for the API
"""
from datetime import datetime
from threading import RLock

class UserStore:
    """In-memory user storage with thread safety"""
    
    def __init__(self):
        self.users = {}
        self.next_id = 1
        self.lock = RLock()  # Using RLock to allow reentrant locking
        self._init_sample_data()
    
    def _init_sample_data(self):
        """Initialize with sample users for testing"""
        sample_users = [
            {
                "name": "Admin User",
                "email": "admin@example.com",
                "age": 30,
                "role": "admin"
            },
            {
                "name": "John Doe",
                "email": "john@example.com",
                "age": 25,
                "role": "user"
            }
        ]
        
        for user_data in sample_users:
            self.create_user(user_data)
    
    def create_user(self, user_data):
        """Create a new user"""
        with self.lock:
            user_id = self.next_id
            user = {
                "id": user_id,
                "name": user_data["name"],
                "email": user_data["email"],
                "age": user_data["age"],
                "role": user_data.get("role", "user"),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            self.users[user_id] = user
            self.next_id += 1
            return user
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        return self.users.get(user_id)
    
    def get_user_by_email(self, email):
        """Get user by email"""
        for user in self.users.values():
            if user["email"].lower() == email.lower():
                return user
        return None
    
    def get_all_users(self):
        """Get all users"""
        return list(self.users.values())
    
    def update_user(self, user_id, user_data):
        """Update an existing user"""
        with self.lock:
            if user_id not in self.users:
                return None
            
            user = self.users[user_id]
            
            # Update only provided fields
            if "name" in user_data:
                user["name"] = user_data["name"]
            if "email" in user_data:
                user["email"] = user_data["email"]
            if "age" in user_data:
                user["age"] = user_data["age"]
            if "role" in user_data:
                user["role"] = user_data["role"]
            
            user["updated_at"] = datetime.utcnow().isoformat()
            return user
    
    def delete_user(self, user_id):
        """Delete a user"""
        with self.lock:
            if user_id in self.users:
                deleted_user = self.users.pop(user_id)
                return deleted_user
            return None
    
    def email_exists(self, email, exclude_user_id=None):
        """Check if email already exists"""
        for user_id, user in self.users.items():
            if user["email"].lower() == email.lower():
                if exclude_user_id is None or user_id != exclude_user_id:
                    return True
        return False
    
    def reset(self):
        """Reset the data store (useful for testing)"""
        with self.lock:
            self.users = {}
            self.next_id = 1
            self._init_sample_data()


# Global user store instance
user_store = UserStore()
