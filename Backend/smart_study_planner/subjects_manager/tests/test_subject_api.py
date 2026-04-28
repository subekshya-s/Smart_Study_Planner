import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from subjects_manager.models import Subjects


@pytest.mark.django_db
def test_create_subject_and_study_hours():
    client = APIClient()
    url = reverse("subject-list")

    data = {
        "subject_name": "Math",
        "study_hours": 5
    }

    response = client.post(url, data, format="json")

    assert response.status_code == 201


@pytest.mark.django_db
def test_list_subject_and_study_hours():
    Subjects.objects.create(subject_name="Science", study_hours=4)

    client = APIClient()
    url = reverse("subject-list")

    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["subject_name"] == "Science"


@pytest.mark.django_db
def test_retrieve_subject_and_study_hours():
    subject = Subjects.objects.create(subject_name="English", study_hours=3)

    client = APIClient()
    url = reverse("subject-detail", args=[subject.id])

    response = client.get(url)

    assert response.status_code == 200
    assert response.data["subject_name"] == "English"


@pytest.mark.django_db
def test_update_subject_and_study_hours():
    subject = Subjects.objects.create(subject_name="Old", study_hours=2)

    client = APIClient()
    url = reverse("subject-detail", args=[subject.id])

    data = {
        "subject_name": "New",
        "study_hours": 6
    }

    response = client.put(url, data, format="json")

    assert response.status_code == 200

    subject.refresh_from_db()
    assert subject.subject_name == "New"


@pytest.mark.django_db
def test_delete_subject():
    subject = Subjects.objects.create(subject_name="Delete Me", study_hours=1)

    client = APIClient()
    url = reverse("subject-detail", args=[subject.id])

    response = client.delete(url)

    assert response.status_code == 204
    assert Subjects.objects.count() == 0