from pymongo import MongoClient
from config import MONGO_DB
from config import MONGODB_LINK

mdb = MongoClient(MONGODB_LINK)[MONGO_DB]

def search_or_save_user(mdb, effective_user, message):
    user = mdb.users.find_one({"user_id": effective_user.id}) # поиск в коллекции users по users.id
    if not user:
        user = {
            'user_id': effective_user.id,
            'first_name': effective_user.first_name,
            'last_name': effective_user.last_name,
            'chat_id': message.chat.id,
            'first_time': True,
            'selected_photo': None,
            'the_most_similar_photo': None,
        }
        mdb.users.insert_one(user) # сохраняем в коллекцию users
    return user

def update_user(mdb, user):
    user_old = mdb.users.find_one({'user_id': user['user_id']})
    user = {'$set': user}
    mdb.users.update_one(user_old, user)