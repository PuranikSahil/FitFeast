import os
from supabase import create_client,Client
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def enter_user(name,user_name,password,age,weight,height):
    response = (supabase
                .table('users')
                .insert({
        "user_name": user_name,
        "name": name,
        "user_password": password,
        "user_age": age,
        "user_weight": weight,
        "user_height": height
    })
                .execute())
    return None

def match_user_pwd(user_name,password):
    response = (supabase
                .table('users')
                .select('user_password')
                .eq("user_name", user_name)
                .execute()
    )
    return response.data[0]["user_password"]