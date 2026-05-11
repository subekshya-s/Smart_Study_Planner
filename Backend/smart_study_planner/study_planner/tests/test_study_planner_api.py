import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from study_planner.models import StudyPlanner
from subjects_manager.models import Subjects


@pytest.mark.django_db
def test_create_study_planner():
    client = APIClient()
    url = reverse("study-planner-list")

    subject = Subjects.objects.create(
        subject_name="English",
        study_hours=5
    )

    data = {
        "subject": subject.id,
        "date": "2025-01-02",
        "start_time": "07:30:00",
        "end_time": "09:30:00",
        "completed": True
    }

    response = client.post(url, data, format="json")

    assert response.status_code == 201


@pytest.mark.django_db
def test_list_study_planner():
    subject = Subjects.objects.create(
        subject_name="English",
        study_hours=5
    )

    StudyPlanner.objects.create(
        subject=subject,
        date="2026-04-29",
        start_time="08:00",
        end_time="09:00",
        completed=False
    )

    client = APIClient()
    url = reverse("study-planner-list")

    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_update_study_planner():
    subject1 = Subjects.objects.create(
        subject_name="English",
        study_hours=5
    )

    subject2 = Subjects.objects.create(
        subject_name="Math",
        study_hours=4
    )

    planner = StudyPlanner.objects.create(
        subject=subject1,
        date="2025-01-02",
        start_time="07:30:00",
        end_time="09:30:00",
        completed=False
    )

    client = APIClient()
    url = reverse("study-planner-detail", args=[planner.id])

    data = {
        "subject": subject2.id,
        "date": "2025-01-02",
        "start_time": "08:00:00",
        "end_time": "10:00:00",
        "completed": True
    }

    response = client.put(url, data, format="json")

    assert response.status_code == 200

    planner.refresh_from_db()
    assert planner.subject == subject2
    assert planner.completed is True


@pytest.mark.django_db
def test_delete_study_planner():
    subject = Subjects.objects.create(
        subject_name="Management",
        study_hours=3
    )

    planner = StudyPlanner.objects.create(
        subject=subject,
        date="2025-01-02",
        start_time="07:30:00",
        end_time="09:30:00",
        completed=False
    )

    client = APIClient()
    url = reverse("study-planner-detail", args=[planner.id])

    response = client.delete(url)

    assert response.status_code == 204
    assert StudyPlanner.objects.count() == 0