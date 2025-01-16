from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Task, Group, GroupUser, UserTask
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta
User = get_user_model()

class CreateGroupTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", username="testuser", password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.url = '/api/groups/create'

    def test_create_group_success(self):
        data = {
            "name": "Test Group"  # Ključ "image" nije potreban
        }

        response = self.client.post(self.url, data)

        # Provjera odgovora
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["message"], "Group created successfully, and user added as a member.")

        # Provjera baze podataka
        self.assertEqual(Group.objects.count(), 1)
        self.assertEqual(Group.objects.first().name, "Test Group")
        self.assertEqual(GroupUser.objects.count(), 1)
        self.assertEqual(GroupUser.objects.first().user, self.user)

    def test_create_group_missing_name(self):
        # Podaci bez polja "name"
        data = {
            "image": ""  # Ovo polje nije obavezno, pa ga ostavljamo praznim
        }

        # Slanje zahtjeva na endpoint za kreiranje grupe
        response = self.client.post(self.url, data)

        # Provjera odgovora
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Očekujemo 400 BAD REQUEST
        self.assertIn("name", response.data)  # Provjeravamo da odgovor sadrži informaciju o grešci za polje "name"


    def test_delete_group_not_implemented(self):
        # Simuliraj zahtjev za nepostojeći endpoint za brisanje grupe
        url = '/api/groups/delete'
        response = self.client.delete(url)

        # Provjera odgovora
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Očekujemo 404 NOT FOUND


    def test_get_all_members_nonexistent_group(self):
        # Ulazni podaci s nepostojećim group_id
        data = {"group_id": 99999}  # Pretpostavljamo da ovaj ID ne postoji

        # Slanje zahtjeva
        response = self.client.post('/api/groups/getAllMembers', data)

        # Provjera odgovora
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)  # Očekujemo 404 NOT FOUND
        self.assertEqual(response.data["message"], "Group not found.")  # Provjera poruke o grešci

    def test_get_all_groups(self):
        # Kreiraj nekoliko grupa i poveži ih s korisnikom
        group1 = Group.objects.create(name="Group 1")
        group2 = Group.objects.create(name="Group 2")
        group3 = Group.objects.create(name="Group 3")

        GroupUser.objects.create(user=self.user, group=group1)
        GroupUser.objects.create(user=self.user, group=group2)

        # Ne dodaj korisnika u grupu 3 (testiramo filtriranje)

        # Pošalji GET zahtjev na endpoint za dohvat grupa
        response = self.client.get('/api/groups/')

        # Dodaj ispis za dijagnostiku ako nešto pođe po zlu
        print(response.status_code, response.data)

        # Provjeri statusni kod
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Provjeri sadržaj odgovora
        self.assertIn("groups", response.data)
        groups = response.data["groups"]
        self.assertEqual(len(groups), 2)  # Korisnik je član samo 2 grupe

        # Provjeri podatke o grupama
        group_names = [group["name"] for group in groups]
        self.assertIn("Group 1", group_names)
        self.assertIn("Group 2", group_names)
        self.assertNotIn("Group 3", group_names)  # Korisnik nije član grupe 3



class TaskTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", username="testuser", password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.group = Group.objects.create(name="Test Group")
        GroupUser.objects.create(user=self.user, group=self.group)

    def test_join_task_full_capacity(self):
        task = Task.objects.create(
            name="Test Task",
            deadline=now() + timedelta(days=1),
            group=self.group,
            max_capacity=2,
            points=50
        )

        # Dodaj dva korisnika kako bi kapacitet bio popunjen
        user2 = User.objects.create_user(username="testuser2", email="testuser2@example.com", password="password123")
        UserTask.objects.create(user=self.user, task=task)
        UserTask.objects.create(user=user2, task=task)

        # Pokušaj dodavanja trećeg korisnika
        user3 = User.objects.create_user(username="testuser3", email="testuser3@example.com", password="password123")
        GroupUser.objects.create(user=user3, group=self.group)  # Dodaj user3 u grupu
        self.client.force_authenticate(user=user3)  # Autentificiraj novog korisnika
        data = {"taskId": task.id}
        response = self.client.post('/api/tasks/join', data)  # Ispravan URL

        # Dodaj ispis statusa i odgovora
        print(response.status_code, response.data)

        # Provjera odgovora
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Očekujemo 400 BAD REQUEST
        self.assertEqual(response.data["error"], "Task is at maximum capacity.")  # Provjera poruke o grešci

        # Provjera da treći korisnik nije dodan u zadatak
        self.assertEqual(UserTask.objects.filter(task=task).count(), 2)  # Kapacitet ostaje 2
        