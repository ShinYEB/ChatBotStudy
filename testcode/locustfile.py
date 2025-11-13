from locust import HttpUser, task, between, TaskSet, constant_pacing
import random
import time

from generate_prompts import getPrompts

PROMPT_LIST = getPrompts()
print("프롬프트 생성 완료")

class UserBehavior(TaskSet):

    @task
    def get_chat(self):
        data = {
            "prompt": f"{random.choice(PROMPT_LIST)}"
        }
        self.client.post("/chat", json=data)

class LocustUser(HttpUser):
    host = "http://127.0.0.1:8000"
    tasks = [UserBehavior]
    wait_time = between(30, 60)

