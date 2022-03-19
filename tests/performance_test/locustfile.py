from locust import HttpUser, task

class ProjectPerfTest(HttpUser):

    @task
    def competition_list(self):
        self.client.get("/clubs")


    @task
    def update_places(self):
        self.client.post("/purchasePlaces", {"club": "Iron Temple","competition": "Spring Festival","places": "3"})