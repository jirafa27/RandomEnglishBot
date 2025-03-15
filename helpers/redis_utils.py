import redis
import os

from dotenv import load_dotenv


class RedisClient:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv("REDIS_HOST")
        self.port = int(os.getenv("REDIS_PORT"))
        self.db = int(os.getenv("REDIS_DB"))
        self.username = os.getenv("REDIS_USERNAME")
        self.redis_client = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            username=os.getenv("REDIS_USERNAME"),
            password="",
        )

    def set_dialog(self, user_id, partner_id):
        user_id = str(user_id)
        partner_id = str(partner_id)
        self.redis_client.hset("active_dialogs", user_id, partner_id)
        self.redis_client.hset("active_dialogs", partner_id, user_id)

    def get_partner(self, user_id):
        user_id = str(user_id)
        partner = self.redis_client.hget("active_dialogs", user_id)
        print(partner)
        return partner.decode() if partner else None

    def is_in_active_dialog(self, user_id):
        user_id = str(user_id)
        print(user_id, self.redis_client.hkeys("active_dialogs"))
        return user_id in self.redis_client.hkeys("active_dialogs")

    def is_in_waiting_queue(self, user_id):
        return self.redis_client.lpos("waiting_queue", user_id) is not None

    def is_waiting_queue_empty(self, user_id):
        return self.redis_client.llen("waiting_queue") == 0

    def remove_dialog(self, user_id):
        partner = self.get_partner(user_id)
        if partner:
            self.redis_client.hdel("active_dialogs", user_id)
            self.redis_client.hdel("active_dialogs", partner)
        return partner

    def add_to_queue(self, user_id):
        self.redis_client.rpush("waiting_queue", user_id)

    def pop_from_queue(self):
        user = self.redis_client.lpop("waiting_queue")
        return user.decode() if user else None

    def add_message(self, key, text):
        self.redis_client.hset("messages", key, text)

    def delete_message(self, key):
        self.redis_client.hdel("messages", key)
