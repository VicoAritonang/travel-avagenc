# main/supabase_client.py
import os
from supabase import create_client, Client
from django.conf import settings

# Konfigurasi Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://wtlhnrymcfroecyzhrya.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind0bGhucnltY2Zyb2VjeXpocnlhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDkzNjU1MSwiZXhwIjoyMDY2NTEyNTUxfQ.HIfOoYGSli2KxGV3S6FRfewmXk-mXt0NwTKQXUjfUVw')

# Buat client Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class SupabaseManager:
    def __init__(self):
        self.client = supabase
    
    # Pesawat methods
    def get_all_pesawat(self):
        """Ambil semua data pesawat"""
        try:
            response = self.client.table('pesawat').select('*').execute()
            return response.data
        except Exception as e:
            print(f"Error fetching pesawat: {e}")
            return []
    
    def create_pesawat(self, data):
        """Tambah data pesawat baru"""
        try:
            response = self.client.table('pesawat').insert(data).execute()
            return response.data
        except Exception as e:
            print(f"Error creating pesawat: {e}")
            return None
    
    # Hotel methods
    def get_all_hotel(self):
        """Ambil semua data hotel"""
        try:
            response = self.client.table('hotel').select('*').execute()
            return response.data
        except Exception as e:
            print(f"Error fetching hotel: {e}")
            return []
    
    def create_hotel(self, data):
        """Tambah data hotel baru"""
        try:
            response = self.client.table('hotel').insert(data).execute()
            return response.data
        except Exception as e:
            print(f"Error creating hotel: {e}")
            return None
    
    # Chat methods
    def get_all_chats(self):
        """Ambil semua data chat"""
        try:
            response = self.client.table('chat').select('id, title, created_at').order('created_at', desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching chats: {e}")
            return []
    
    def get_chat_by_id(self, chat_id):
        """Ambil data chat berdasarkan ID"""
        try:
            response = self.client.table('chat').select('*').eq('id', chat_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching chat by id: {e}")
            return None
    
    def create_chat(self, data):
        """Buat chat baru"""
        try:
            response = self.client.table('chat').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating chat: {e}")
            return None
    
    def update_chat(self, chat_id, data):
        """Update data chat"""
        try:
            response = self.client.table('chat').update(data).eq('id', chat_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating chat: {e}")
            return None
    
    def delete_chat(self, chat_id):
        """Hapus chat"""
        try:
            response = self.client.table('chat').delete().eq('id', chat_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting chat: {e}")
            return False

# Instance global
db = SupabaseManager()