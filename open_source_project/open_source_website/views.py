from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.template import loader
from .forms import contactForm, emailsForNewsletter
from .models import databaseForNewsletter, databaseForBlogs, databaseForCoordinates
from django.core.mail import send_mail
from datetime import datetime
from json import dumps
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .serializer import get_gps_coordinates_and_more


class General_data:
    marker_data = get_gps_coordinates_and_more(databaseForCoordinates.objects.values_list("name_of_locations",
                                                                                          "adresse",
                                                                                          "code_postal",
                                                                                          "localite",
                                                                                          "informations_supplementaires",
                                                                                          "url_coordinates"))


class Homepage(View):
    template_html = loader.get_template("open_source_website/index.html")
    # loading forms
    contact_form = contactForm()
    newsletter_form = emailsForNewsletter()
    # loading models
    last_blog = databaseForBlogs.objects.last()
    coordinates = General_data.marker_data
    data_as_JSON = dumps(coordinates)

    def get(self, request):
        context = {"contact_form": self.contact_form,
                   "newsletter_form": self.newsletter_form,
                   "last_blog": self.last_blog,
                   "map_positions": self.data_as_JSON}
        return HttpResponse(self.template_html.render(request=request, context=context))

    def post(self, request):
        contact_form_post = contactForm(request.POST)
        newsletter_form_post = emailsForNewsletter(request.POST)
        context = {"contact_form": contact_form_post,
                   "newsletter_form": newsletter_form_post,
                   "last_blog": self.last_blog,
                   "map_positions": self.data_as_JSON
                   }
        if contact_form_post.is_valid() or newsletter_form_post.is_valid():
            if "contact_form" in request.POST:  # handling data from the contact form
                sujet = contact_form_post.cleaned_data.get("sujet")
                email = contact_form_post.cleaned_data.get("email")
                text = contact_form_post.cleaned_data.get("message")
                if sujet and email and text:
                    send_mail(subject=sujet,
                              message=f"{text},"
                                      f"\n From: {email} \n"
                                      f" At: {datetime.now()}",
                              from_email=email,
                              recipient_list=["BakPak@outlook.fr"],
                              fail_silently=False)
                    context["state"] = True
                    context["message_contact"] = "Bien envoyé !"  # Send !
                    return HttpResponse(self.template_html.render(request=request, context=context))

                context[
                    "message"] = "Mauvaise adresse mail ou un champs est vide"  # Wrong address of the field is empty

                return HttpResponse(self.template_html.render(request=request, context=context))
            elif "newsletter_form" in request.POST:  # handling data from the newsletter subscription form
                email = newsletter_form_post.cleaned_data.get("email")
                double_email_check = databaseForNewsletter.objects.filter(email__icontains=email)

                if double_email_check.exists():
                    context["message_newsletter"] = "\n Nous avons reperé un doublons de mails, vous êtes déjà inscrit !\n"
                    # We found a duplicate, you have already subscribed !

                    return HttpResponse(self.template_html.render(request=request, context=context))

                context["message_newsletter"] = "\n Vous êtes bien inscrit ! \n"  # You are subscribed !
                context["state"] = True
                databaseForNewsletter.objects.create(email=email)
                return HttpResponse(self.template_html.render(request=request, context=context))


class Blogs(View):
    coordinates = General_data.marker_data
    data_as_JSON = dumps(coordinates)
    all_blogs = databaseForBlogs.objects.all()

    def get(self, request):
        paginator = Paginator(self.all_blogs, 5)
        page = request.GET.get('page')
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

        context = {"all_blog": blogs,
                   "map_positions": self.data_as_JSON,
                   "paginate": True}
        return render(request, "open_source_website/blog.html", context=context)


class One_blog(View):
    coordinates = General_data.marker_data
    data_as_JSON = dumps(coordinates)

    def get(self, request, pk):
        blog_specific = databaseForBlogs.objects.get(pk=pk)
        context = {"blog_specific": blog_specific,
                   "map_positions": self.data_as_JSON}
        return render(request, "open_source_website/blog_view.html", context=context)


class Unsubscribe(View):
    coordinates = General_data.marker_data
    data_as_JSON = dumps(coordinates)

    def get(self, request):
        newsletter_form = emailsForNewsletter()
        context = {"newsletter_form": newsletter_form,
                   "map_positions": self.data_as_JSON}
        return render(request, "open_source_website/unsubscribe.html", context=context)

    def post(self, request):
        newsletter_form = emailsForNewsletter(request.POST)
        context = {"newsletter_form": newsletter_form,
                   "map_positions": self.data_as_JSON}
        newsletter_for_post = emailsForNewsletter(request.POST)
        if newsletter_for_post.is_valid():
            email = newsletter_for_post.cleaned_data.get("email")
            email_to_delete = databaseForNewsletter.objects.filter(email__icontains=email)
            if email_to_delete.exists():
                email_to_delete.delete()
                context["state"] = True
                context["message_contact"] = "Vous ne recevrez plus de mails de notre part !"
                # You won't receive any mail from us !
                return render(request, "open_source_website/unsubscribe.html", context=context)

        context["message_contact"] = "Vous n'êtes pas inscrit ou votre syntaxe ne nous " \
                                     "permet pas de trouver votre adresse mail. " \
                                     "<a href='/bakpak/#ancre_newsletter_message'> S'inscrire !</a>"
        # You're not subscribed or your syntax doesn't allow us to find you.
        # <a href='/bakpak/#ancre_newsletter_message'> Subscribe !</a>
        return render(request, "open_source_website/unsubscribe.html", context=context)


class Legal_Stuff(View):

    def get(self, request):
        return render(request, "open_source_website/legal_stuff.html")
