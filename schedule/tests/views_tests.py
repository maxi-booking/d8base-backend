"""The views tests module."""
import arrow
import pytest
from django.db.models.query import QuerySet
from django.test.client import Client
from django.urls import reverse
from pytest_mock.plugin import MockerFixture

from users.models import User

pytestmark = pytest.mark.django_db


def test_professional_calendar_list_error(
    availability_slots: QuerySet,
    client_with_token: Client,
):
    """Should return an error."""
    professional = availability_slots.first().professional
    start = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    end = start.shift(days=-2)
    response = client_with_token.get(
        reverse("schedule-calendar-list"), {
            "professional": professional.pk,
            "start_datetime": start.format("YYYY-MM-DD"),
            "end_datetime": end.format("YYYY-MM-DD")
        })
    assert response.status_code == 400


def test_professional_calendar_list(
    availability_slots: QuerySet,
    client_with_token: Client,
):
    """Should return a professional schedules list."""
    professional = availability_slots.first().professional
    start = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    end = start.shift(days=2)
    response = client_with_token.get(
        reverse("schedule-calendar-list"), {
            "professional": professional.pk,
            "start_datetime": start.format("YYYY-MM-DD"),
            "end_datetime": end.format("YYYY-MM-DD")
        })
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["professional"] == professional.pk


def test_professional_calendar_service_list(
    availability_slots: QuerySet,
    client_with_token: Client,
):
    """Should return a professional schedules list for a service."""
    service = availability_slots.filter(service__isnull=False).first().service
    start = arrow.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    end = start.shift(days=2)
    response = client_with_token.get(
        reverse("schedule-calendar-list"), {
            "professional": service.professional.pk,
            "service": service.pk,
            "start_datetime": start.format("YYYY-MM-DD"),
            "end_datetime": end.format("YYYY-MM-DD")
        })
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["service"] == service.pk


def test_user_professional_schedule_list(
    user: User,
    client_with_token: Client,
    professional_schedules: QuerySet,
):
    """Should return a professional schedules list."""
    query = professional_schedules.filter(professional__user=user)
    obj = query.first()
    response = client_with_token.get(
        reverse("user-professional-schedule-list"))
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == query.count()
    assert data["results"][0]["day_of_week"] == obj.day_of_week


def test_user_professional_schedule_detail(
    user: User,
    client_with_token: Client,
    professional_schedules: QuerySet,
):
    """Should return a user professional schedules."""
    obj = professional_schedules.filter(professional__user=user).first()
    response = client_with_token.get(
        reverse("user-professional-schedule-detail", args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data["start_time"] == str(obj.start_time)


def test_user_professional_schedule_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_schedules: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_schedules.filter(professional__user=admin).first()
    response = client_with_token.patch(
        reverse("user-professional-schedule-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_user_professional_schedule_create(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should be able to create a user professional schedule object."""
    obj = professionals.filter(user=user).first()
    response = client_with_token.post(
        reverse("user-professional-schedule-list"),
        {
            "day_of_week": 2,
            "start_time": "09:00",
            "end_time": "14:00",
            "professional": obj.pk,
        },
    )
    schedule = obj.schedule.first()
    assert response.status_code == 201
    assert schedule.day_of_week == 2
    assert str(schedule.start_time) == "09:00:00"
    assert str(schedule.end_time) == "14:00:00"


def test_user_professional_schedule_set(
    user: User,
    admin: User,
    client_with_token: Client,
    professionals: QuerySet,
    mocker: MockerFixture,
):
    """Should be able to set professional schedule objects."""
    signal = mocker.patch("schedule.signals.generate_for_professional")
    professional = professionals.filter(user=user).first()
    professional_last = professionals.filter(user=user).last()
    admin_professional = professionals.filter(user=admin).first()
    response = client_with_token.post(
        reverse("user-professional-schedule-set"),
        {
            "day_of_week": 0,
            "start_time": "09:00",
            "end_time": "14:00",
            "professional": professional.pk,
        },
        format="json",
    )
    assert response.status_code == 400

    response = client_with_token.post(
        reverse("user-professional-schedule-set"),
        [
            {
                "day_of_week": 0,
                "start_time": "09:00",
                "end_time": "14:00",
                "professional": professional.pk,
            },
            {
                "day_of_week": 2,
                "start_time": "09:00",
                "end_time": "14:00",
                "professional": admin_professional.pk,
            },
        ],
        format="json",
    )

    assert response.status_code == 400

    response = client_with_token.post(
        reverse("user-professional-schedule-set"),
        [
            {
                "day_of_week": 0,
                "start_time": "09:00",
                "end_time": "14:00",
                "professional": professional.pk,
            },
            {
                "day_of_week": 1,
                "start_time": "09:00",
                "end_time": "14:00",
                "professional": professional.pk,
            },
            {
                "day_of_week": 2,
                "start_time": "09:00",
                "end_time": "14:00",
                "professional": professional.pk,
            },
        ],
        format="json",
    )
    assert response.status_code == 201
    assert professional.schedule.count() == 3
    assert signal.call_count == 4

    response = client_with_token.post(
        reverse("user-professional-schedule-set"),
        [
            {
                "day_of_week": 0,
                "start_time": "09:00",
                "end_time": "14:00",
                "professional": professional.pk,
            },
            {
                "day_of_week": 1,
                "start_time": "09:00",
                "end_time": "14:00",
                "professional": professional.pk,
            },
        ],
        format="json",
    )
    assert response.status_code == 201
    assert professional.schedule.count() == 2
    assert professional_last.schedule.count() == 0

    assert signal.call_count == 4 + 5

    response = client_with_token.post(
        reverse("user-professional-schedule-set"),
        [
            {
                "day_of_week": 0,
                "start_time": "09:00",
                "end_time": "14:00",
                "professional": professional_last.pk,
            },
            {
                "day_of_week": 1,
                "start_time": "09:00",
                "end_time": "14:00",
                "professional": professional_last.pk,
            },
        ],
        format="json",
    )
    assert response.status_code == 201
    assert professional.schedule.count() == 2
    assert professional_last.schedule.count() == 2
    assert signal.call_count == 4 + 5 + 2


def test_user_professional_schedule_update(
    user: User,
    client_with_token: Client,
    professional_schedules: QuerySet,
):
    """Should be able to update a user professional schedule."""
    professional_schedules.filter(day_of_week=6).delete()
    obj = professional_schedules.filter(professional__user=user).first()
    start_time = obj.start_time
    end_time = obj.end_time
    response = client_with_token.patch(
        reverse("user-professional-schedule-detail", args=[obj.pk]),
        {
            "day_of_week": 6,
            "professional": obj.professional.pk,
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.day_of_week == 6
    assert obj.start_time == start_time
    assert obj.end_time == end_time
    assert obj.professional.user == user
    assert obj.modified_by == user


def test_user_professional_schedule_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_schedules: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_schedules.filter(professional__user=admin).first()
    response = client_with_token.post(
        reverse("user-professional-schedule-detail", args=[obj.pk]),
        {"day_of_week": 1})
    assert response.status_code == 405


def test_user_professional_schedule_delete(
    user: User,
    client_with_token: Client,
    professional_schedules: QuerySet,
):
    """Should be able to delete a user professional schedule."""
    obj = professional_schedules.filter(professional__user=user).first()
    response = client_with_token.delete(
        reverse("user-professional-schedule-detail", args=[obj.pk]))
    assert response.status_code == 204
    assert professional_schedules.filter(pk=obj.pk).count() == 0


def test_user_professional_schedule_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_schedules: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_schedules.filter(professional__user=admin).first()
    response = client_with_token.delete(
        reverse("user-professional-schedule-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_user_service_schedule_list(
    user: User,
    client_with_token: Client,
    service_schedules: QuerySet,
):
    """Should return a service schedules list."""
    query = service_schedules.filter(service__professional__user=user)
    obj = query.first()
    response = client_with_token.get(reverse("user-service-schedule-list"))
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == query.count()
    assert data["results"][0]["day_of_week"] == obj.day_of_week


def test_user_service_schedule_detail(
    user: User,
    client_with_token: Client,
    service_schedules: QuerySet,
):
    """Should return a user service schedules."""
    obj = service_schedules.filter(service__professional__user=user).first()
    response = client_with_token.get(
        reverse("user-service-schedule-detail", args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data["start_time"] == str(obj.start_time)


def test_user_service_schedule_restricted_entry(
    admin: User,
    client_with_token: Client,
    service_schedules: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = service_schedules.filter(service__professional__user=admin).first()
    response = client_with_token.patch(
        reverse("user-service-schedule-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_user_service_schedule_create(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should be able to create a user service schedule object."""
    obj = services.filter(professional__user=user).first()
    obj.is_base_schedule = False
    obj.save()
    response = client_with_token.post(
        reverse("user-service-schedule-list"),
        {
            "day_of_week": 2,
            "start_time": "09:00",
            "end_time": "14:00",
            "service": obj.pk,
        },
    )
    schedule = obj.schedule.first()
    assert response.status_code == 201
    assert schedule.day_of_week == 2
    assert str(schedule.start_time) == "09:00:00"
    assert str(schedule.end_time) == "14:00:00"


def test_user_service_schedule_set(
    user: User,
    admin: User,
    client_with_token: Client,
    services: QuerySet,
    mocker: MockerFixture,
):
    """Should be able to set service schedule objects."""
    signal = mocker.patch("schedule.signals.generate_for_service")
    service = services.filter(professional__user=user).first()
    service.is_base_schedule = False
    service.save()
    service_last = services.filter(professional__user=user).last()
    service_last.is_base_schedule = False
    service_last.save()
    admin_service = services.filter(professional__user=admin).first()
    response = client_with_token.post(
        reverse("user-service-schedule-set"),
        {
            "day_of_week": 0,
            "start_time": "09:00",
            "end_time": "14:00",
            "service": service.pk,
        },
        format="json",
    )
    assert response.status_code == 400

    response = client_with_token.post(
        reverse("user-service-schedule-set"),
        [
            {
                "day_of_week": 0,
                "start_time": "09:00",
                "end_time": "14:00",
                "service": service.pk,
            },
            {
                "day_of_week": 2,
                "start_time": "09:00",
                "end_time": "14:00",
                "service": admin_service.pk,
            },
        ],
        format="json",
    )

    assert response.status_code == 400

    response = client_with_token.post(
        reverse("user-service-schedule-set"),
        [
            {
                "day_of_week": 0,
                "start_time": "09:00",
                "end_time": "14:00",
                "service": service.pk,
            },
            {
                "day_of_week": 1,
                "start_time": "09:00",
                "end_time": "14:00",
                "service": service.pk,
            },
            {
                "day_of_week": 2,
                "start_time": "09:00",
                "end_time": "14:00",
                "service": service.pk,
            },
        ],
        format="json",
    )
    assert response.status_code == 201
    assert service.schedule.count() == 3
    assert signal.call_count == 6

    response = client_with_token.post(
        reverse("user-service-schedule-set"),
        [
            {
                "day_of_week": 0,
                "start_time": "09:00",
                "end_time": "14:00",
                "service": service.pk,
            },
            {
                "day_of_week": 1,
                "start_time": "09:00",
                "end_time": "14:00",
                "service": service.pk,
            },
        ],
        format="json",
    )
    assert response.status_code == 201
    assert service.schedule.count() == 2
    assert service_last.schedule.count() == 0

    assert signal.call_count == 6 + 5

    response = client_with_token.post(
        reverse("user-service-schedule-set"),
        [
            {
                "day_of_week": 0,
                "start_time": "09:00",
                "end_time": "14:00",
                "service": service_last.pk,
            },
            {
                "day_of_week": 1,
                "start_time": "09:00",
                "end_time": "14:00",
                "service": service_last.pk,
            },
        ],
        format="json",
    )
    assert response.status_code == 201
    assert service.schedule.count() == 2
    assert service_last.schedule.count() == 2
    assert signal.call_count == 6 + 5 + 2


def test_user_service_schedule_update(
    user: User,
    client_with_token: Client,
    service_schedules: QuerySet,
):
    """Should be able to update a user service schedule."""
    service_schedules.filter(day_of_week=6).delete()
    obj = service_schedules.filter(service__professional__user=user).first()
    service = obj.service
    service.is_base_schedule = False
    service.save()
    start_time = obj.start_time
    end_time = obj.end_time
    response = client_with_token.patch(
        reverse("user-service-schedule-detail", args=[obj.pk]),
        {
            "day_of_week": 6,
            "service": obj.service.pk,
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.day_of_week == 6
    assert obj.start_time == start_time
    assert obj.end_time == end_time
    assert obj.service.professional.user == user
    assert obj.modified_by == user


def test_user_service_schedule_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    service_schedules: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = service_schedules.filter(service__professional__user=admin).first()
    response = client_with_token.post(
        reverse("user-service-schedule-detail", args=[obj.pk]),
        {"day_of_week": 1})
    assert response.status_code == 405


def test_user_service_schedule_delete(
    user: User,
    client_with_token: Client,
    service_schedules: QuerySet,
):
    """Should be able to delete a user service schedule."""
    obj = service_schedules.filter(service__professional__user=user).first()
    response = client_with_token.delete(
        reverse("user-service-schedule-detail", args=[obj.pk]))
    assert response.status_code == 204
    assert service_schedules.filter(pk=obj.pk).count() == 0


def test_user_service_schedule_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    service_schedules: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = service_schedules.filter(service__professional__user=admin).first()
    response = client_with_token.delete(
        reverse("user-service-schedule-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_user_service_closed_periods_list(
    user: User,
    client_with_token: Client,
    service_closed_periods: QuerySet,
):
    """Should return a service closed periods list."""
    query = service_closed_periods.filter(service__professional__user=user)
    obj = query.first()
    response = client_with_token.get(
        reverse("user-service-closed-periods-list"))
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == query.count()
    assert data["results"][0]["start_datetime"] == obj.start_datetime.\
        isoformat().replace("+00:00", "Z")


def test_user_service_closed_periods_detail(
    user: User,
    client_with_token: Client,
    service_closed_periods: QuerySet,
):
    """Should return a user service closed period."""
    obj = service_closed_periods.filter(
        service__professional__user=user).first()
    response = client_with_token.get(
        reverse("user-service-closed-periods-detail", args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data["end_datetime"] == obj.end_datetime.\
        isoformat().replace("+00:00", "Z")


def test_user_service_closed_periods_restricted_entry(
    admin: User,
    client_with_token: Client,
    service_closed_periods: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = service_closed_periods.filter(
        service__professional__user=admin).first()
    response = client_with_token.patch(
        reverse("user-service-closed-periods-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_user_service_closed_periods_create(
    user: User,
    client_with_token: Client,
    services: QuerySet,
):
    """Should be able to create a user service closed period object."""
    obj = services.filter(professional__user=user).first()

    start = arrow.utcnow().shift(days=2)
    end = arrow.utcnow().shift(days=4)
    response = client_with_token.post(
        reverse("user-service-closed-periods-list"),
        {
            "start_datetime": start.isoformat(),
            "end_datetime": end.isoformat(),
            "service": obj.pk,
        },
    )
    entry = obj.closed_periods.first()
    assert response.status_code == 201
    assert entry.start_datetime == start.datetime
    assert entry.end_datetime == end.datetime


def test_user_service_closed_periods_update(
    user: User,
    client_with_token: Client,
    service_closed_periods: QuerySet,
):
    """Should be able to update a user service closed period."""
    obj = service_closed_periods.filter(
        service__professional__user=user).first()
    start = arrow.utcnow().shift(days=10)
    end = arrow.utcnow().shift(days=12)
    response = client_with_token.patch(
        reverse("user-service-closed-periods-detail", args=[obj.pk]),
        {
            "is_enabled": False,
            "start_datetime": start.isoformat(),
            "end_datetime": end.isoformat(),
            "service": obj.service.pk,
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.is_enabled is False
    assert obj.start_datetime == start.datetime
    assert obj.end_datetime == end.datetime
    assert obj.service.professional.user == user
    assert obj.modified_by == user


def test_user_service_closed_periods_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    service_closed_periods: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = service_closed_periods.filter(
        service__professional__user=admin).first()
    response = client_with_token.post(
        reverse("user-service-closed-periods-detail", args=[obj.pk]),
        {"day_of_week": 1})
    assert response.status_code == 405


def test_user_service_closed_periods_delete(
    user: User,
    client_with_token: Client,
    service_closed_periods: QuerySet,
):
    """Should be able to delete a user service closed period."""
    obj = service_closed_periods.filter(
        service__professional__user=user).first()
    response = client_with_token.delete(
        reverse("user-service-closed-periods-detail", args=[obj.pk]))
    assert response.status_code == 204
    assert service_closed_periods.filter(pk=obj.pk).count() == 0


def test_user_service_closed_periods_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    service_closed_periods: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = service_closed_periods.filter(
        service__professional__user=admin).first()
    response = client_with_token.delete(
        reverse("user-service-closed-periods-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_user_professional_closed_periods_list(
    user: User,
    client_with_token: Client,
    professional_closed_periods: QuerySet,
):
    """Should return a professional closed periods list."""
    query = professional_closed_periods.filter(professional__user=user)
    obj = query.first()
    response = client_with_token.get(
        reverse("user-professional-closed-periods-list"))
    data = response.json()
    assert response.status_code == 200
    assert data["count"] == query.count()
    assert data["results"][0]["start_datetime"] == obj.start_datetime.\
        isoformat().replace("+00:00", "Z")


def test_user_professional_closed_periods_detail(
    user: User,
    client_with_token: Client,
    professional_closed_periods: QuerySet,
):
    """Should return a user professional closed period."""
    obj = professional_closed_periods.filter(professional__user=user).first()
    response = client_with_token.get(
        reverse("user-professional-closed-periods-detail", args=[obj.pk]))
    data = response.json()
    assert response.status_code == 200
    assert data["end_datetime"] == obj.end_datetime.\
        isoformat().replace("+00:00", "Z")


def test_user_professional_closed_periods_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_closed_periods: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_closed_periods.filter(professional__user=admin).first()
    response = client_with_token.patch(
        reverse("user-professional-closed-periods-detail", args=[obj.pk]))
    assert response.status_code == 404


def test_user_professional_closed_periods_create(
    user: User,
    client_with_token: Client,
    professionals: QuerySet,
):
    """Should be able to create a user professional closed period object."""
    obj = professionals.filter(user=user).first()

    start = arrow.utcnow().shift(days=2)
    end = arrow.utcnow().shift(days=4)
    response = client_with_token.post(
        reverse("user-professional-closed-periods-list"),
        {
            "start_datetime": start.isoformat(),
            "end_datetime": end.isoformat(),
            "professional": obj.pk,
        },
    )
    entry = obj.closed_periods.first()
    assert response.status_code == 201
    assert entry.start_datetime == start.datetime
    assert entry.end_datetime == end.datetime


def test_user_professional_closed_periods_update(
    user: User,
    client_with_token: Client,
    professional_closed_periods: QuerySet,
):
    """Should be able to update a user professional closed period."""
    obj = professional_closed_periods.filter(professional__user=user).first()
    start = arrow.utcnow().shift(days=10)
    end = arrow.utcnow().shift(days=12)
    response = client_with_token.patch(
        reverse("user-professional-closed-periods-detail", args=[obj.pk]),
        {
            "is_enabled": False,
            "start_datetime": start.isoformat(),
            "end_datetime": end.isoformat(),
            "professional": obj.professional.pk,
        },
    )
    obj.refresh_from_db()
    assert response.status_code == 200
    assert obj.is_enabled is False
    assert obj.start_datetime == start.datetime
    assert obj.end_datetime == end.datetime
    assert obj.professional.user == user
    assert obj.modified_by == user


def test_user_professional_closed_periods_update_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_closed_periods: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_closed_periods.filter(professional__user=admin).first()
    response = client_with_token.post(
        reverse("user-professional-closed-periods-detail", args=[obj.pk]),
        {"is_enabled": 1})
    assert response.status_code == 405


def test_user_professional_closed_periods_delete(
    user: User,
    client_with_token: Client,
    professional_closed_periods: QuerySet,
):
    """Should be able to delete a user professional closed period."""
    obj = professional_closed_periods.filter(professional__user=user).first()
    response = client_with_token.delete(
        reverse("user-professional-closed-periods-detail", args=[obj.pk]))
    assert response.status_code == 204
    assert professional_closed_periods.filter(pk=obj.pk).count() == 0


def test_user_professional_closed_periods_delete_restricted_entry(
    admin: User,
    client_with_token: Client,
    professional_closed_periods: QuerySet,
):
    """Should deny access to someone else"s record."""
    obj = professional_closed_periods.filter(professional__user=admin).first()
    response = client_with_token.delete(
        reverse("user-professional-closed-periods-detail", args=[obj.pk]))
    assert response.status_code == 404
