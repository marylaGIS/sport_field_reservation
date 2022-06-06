from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import date

from .models import SportField, SportDiscipline, SportFieldReservation
from .forms import AddSportFieldForm, EditSportFieldForm, SportFieldReservationForm, \
    SearchByNameForm, SearchByDisciplineForm, ContactForm, \
    SignUpForm


class IndexView(View):
    def get(self, request):
        return render(request, "index.html")


class SportFieldListView(View):
    def get(self, request):
        sport_fields = SportField.objects.all()
        paginator = Paginator(sport_fields, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        ctx = {"sport_fields": sport_fields,
               "page_obj": page_obj}
        return render(request, "sport-field-list.html", ctx)


class SportFieldDetailsView(View):
    def get(self, request, sport_field_id):
        sport_field = SportField.objects.get(id=sport_field_id)

        sfd = sport_field.disciplines.all()

        sport_field_reservations = SportFieldReservation.objects. \
            filter(sport_field=sport_field).filter(date__gte=date.today())

        latitude = sport_field.latitude
        longitude = sport_field.longitude
        ctx = {"sport_field": sport_field,
               "sfd": sfd,
               "x": latitude,
               "y": longitude,
               "sport_field_reservations": sport_field_reservations}
        return render(request, "sport-field-details.html", ctx)


class EditSportFieldView(View):
    def get(self, request, sport_field_id):
        sport_field = SportField.objects.get(id=sport_field_id)
        sport_field.disciplines.clear()
        form = EditSportFieldForm(initial={"name": sport_field.name,
                                          "size": sport_field.size,
                                          "lighting": sport_field.lighting,
                                          "latitude": sport_field.latitude,
                                          "longitude": sport_field.longitude})
        latitude = sport_field.latitude
        longitude = sport_field.longitude
        ctx = {"form": form,
               "x": latitude,
               "y": longitude}
        return render(request, "edit-sport-field.html", ctx)

    def post(self, request, sport_field_id):
        form = EditSportFieldForm(request.POST)
        if form.is_valid():
            sport_field = SportField.objects.get(id=sport_field_id)

            sport_field.name = form.cleaned_data['name']
            sport_field.size = form.cleaned_data['size']
            disciplines = form.cleaned_data['disciplines']
            sport_field.lighting = form.cleaned_data['lighting']
            sport_field.latitude = form.cleaned_data['latitude']
            sport_field.longitude = form.cleaned_data['longitude']

            disciplines_set = []
            for discipline in disciplines:
                d = SportDiscipline.objects.get(id=discipline)
                disciplines_set.append(d)
            sport_field.disciplines.set(disciplines_set)

            sport_field.save()
        return redirect(f"/sport-field/{sport_field_id}/")


class DeleteSportFieldView(View):
    def get(self, request, sport_field_id):
        sport_field = SportField.objects.get(id=sport_field_id)
        sport_field.delete()
        return redirect("/sport-field-list/")


class BookSportFieldView(View):
    def get(self, request, sport_field_id):
        today = date.today()
        form = SportFieldReservationForm(initial={"date": today})
        sport_field = SportField.objects.get(id=sport_field_id)
        name = sport_field.name
        latitude = sport_field.latitude
        longitude = sport_field.longitude
        ctx = {"form": form,
               "name": name,
               "x": latitude,
               "y": longitude}
        return render(request, "sport-field-reservation.html", ctx)

    def post(self, request, sport_field_id):
        form = SportFieldReservationForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data["date"]
            comment = form.cleaned_data["comment"]
            sport_field = SportField.objects.get(id=sport_field_id)
            reservation = SportFieldReservation.objects.create(sport_field=sport_field,
                                                               date=date, comment=comment)
            return redirect(f"/sport-field/{sport_field_id}/")


class AddFieldView(View):
    def get(self, request):
        form = AddSportFieldForm()
        return render(request, "add-sport-field.html", {"form": form})

    def post(self, request):
        form = AddSportFieldForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            size = form.cleaned_data['size']
            disciplines = form.cleaned_data['disciplines']
            lighting = form.cleaned_data['lighting']
            latitude = form.cleaned_data['latitude']
            longitude = form.cleaned_data['longitude']

            disciplines_set = []
            for discipline in disciplines:
                d = SportDiscipline.objects.get(id=discipline)
                disciplines_set.append(d)

            s = SportField.objects.create(name=name, size=size, lighting=lighting,
                                          latitude=latitude, longitude=longitude)
            s.disciplines.set(disciplines_set)
            s_id = s.id
            return redirect(f"/sport-field/{s_id}/")


class SearchView(View):
    def get(self, request):
        name_form = SearchByNameForm()
        discipline_form = SearchByDisciplineForm()
        ctx = {"name_form": name_form,
               "discipline_form": discipline_form}
        return render(request, "search.html", ctx)

    def post(self, request):
        name_form = SearchByNameForm(request.POST)
        if name_form.is_valid():
            name = name_form.cleaned_data["name"]
            sport_fields = SportField.objects.filter(name__contains=name)
            name_form = SearchByNameForm()
            discipline_form = SearchByDisciplineForm()
            ctx = {"sport_fields": sport_fields,
                   "name_form": name_form,
                   "discipline_form": discipline_form}
            return render(request, "search.html", ctx)

        discipline_form = SearchByDisciplineForm(request.POST)
        if discipline_form.is_valid():
            discipline = discipline_form.cleaned_data["discipline"]
            sport_fields = SportField.objects.filter(disciplines=discipline)
            discipline_form = SearchByDisciplineForm()
            name_form = SearchByNameForm()
            ctx = {"sport_fields": sport_fields,
                   "discipline_form": discipline_form,
                   "name_form": name_form}
            return render(request, "search.html", ctx)


class CalendarView(View):
    def get(self, request):
        reservations = SportFieldReservation.objects.all().order_by("date")
        ctx = {"reservations": reservations}
        return render(request, "calendar.html", ctx)


class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, "contact.html", {"form": form})


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, "sign-up.html", {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            if not User.objects.filter(username=username).exists():
                form.save()
                messages.success(request, 'Account created successfully. Now you can sign in.')
        else:
            messages.error(request, 'User already exists!')
            return redirect("sign-up")

        return redirect("sign-in")


class SignInView(LoginView):
    template_name = "sign-in.html"


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")
