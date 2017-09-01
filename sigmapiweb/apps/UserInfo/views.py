from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.template.defaultfilters import stringfilter, register
from django.utils.html import strip_tags

from . import utils
from .models import UserInfo, EditUserInfoForm, PledgeClass

def users(request):
    """
        Provides the collections of brothers in the house.
        Organizes them based on year and exec positions.
    """

    # Find out what current year is the senior year grad date.
    senior_year = utils.get_senior_year()

    # Get the execs.  Use try/catch to avoid crashing the site if an exec is missing.
    try:
        sage = User.objects.get(groups__name='Sage')
    except:
        sage = None
    try:
        second = User.objects.get(groups__name='2nd Counselor')
    except:
        second = None
    try:
        third = User.objects.get(groups__name='3rd Counselor')
    except:
        third = None
    try:
        fourth = User.objects.get(groups__name='4th Counselor')
    except:
        fourth = None
    try:
        first = User.objects.get(groups__name='1st Counselor')
    except:
        first = None
    try:
        herald = User.objects.get(groups__name='Herald')
    except:
        herald = None

    # Get the rest of the users.  Exclude pledges or any execs.
    seniors = User.objects.filter(groups__name='Brothers')
    seniors = seniors.filter(userinfo__graduationYear__lte=senior_year).prefetch_related('userinfo').order_by("last_name")

    juniors = User.objects.filter(userinfo__graduationYear=(senior_year + 1)).prefetch_related('userinfo').order_by("last_name")
    juniors = juniors.exclude(groups__name='Pledges')
    juniors = juniors.exclude(groups__name='Alumni')

    sophomores = User.objects.filter(userinfo__graduationYear=(senior_year + 2)).prefetch_related('userinfo').order_by("last_name")
    sophomores = sophomores.exclude(groups__name='Pledges')
    sophomores = sophomores.exclude(groups__name='Alumni')

    freshmen = User.objects.filter(userinfo__graduationYear=(senior_year + 3)).prefetch_related('userinfo').order_by("last_name")
    freshmen = freshmen.exclude(groups__name='Pledges')
    freshmen = freshmen.exclude(groups__name='Alumni')

    # Exclude the execs, if applicable.
    if sage is not None:
        seniors = seniors.exclude(username=sage.username)
        juniors = juniors.exclude(username=sage.username)
        sophomores = sophomores.exclude(username=sage.username)
        freshmen = freshmen.exclude(username=sage.username)

    if second is not None:
        seniors = seniors.exclude(username=second.username)
        juniors = juniors.exclude(username=second.username)
        sophomores = sophomores.exclude(username=second.username)
        freshmen = freshmen.exclude(username=second.username)

    if third is not None:
        seniors = seniors.exclude(username=third.username)
        juniors = juniors.exclude(username=third.username)
        sophomores = sophomores.exclude(username=third.username)
        freshmen = freshmen.exclude(username=third.username)

    if fourth is not None:
        seniors = seniors.exclude(username=fourth.username)
        juniors = juniors.exclude(username=fourth.username)
        sophomores = sophomores.exclude(username=fourth.username)
        freshmen = freshmen.exclude(username=fourth.username)

    if first is not None:
        seniors = seniors.exclude(username=first.username)
        juniors = juniors.exclude(username=first.username)
        sophomores = sophomores.exclude(username=first.username)
        freshmen = freshmen.exclude(username=first.username)

    if herald is not None:
        seniors = seniors.exclude(username=herald.username)
        juniors = juniors.exclude(username=herald.username)
        sophomores = sophomores.exclude(username=herald.username)
        freshmen = freshmen.exclude(username=herald.username)

    context = {
        'sage': sage,
        'second': second,
        'third': third,
        'fourth': fourth,
        'first': first,
        'herald': herald,
        'seniors': seniors,
        'juniors': juniors,
        'sophomores': sophomores,
        'freshmen': freshmen
    }

    return render(request, 'userinfo/public/brothers.html', context)

@permission_required('UserInfo.manage_users', login_url='secure-index')
def add_users(request):
    """
        Provides a view for adding a user
    """
    context = {
        'message': []
    }

    if request.method == 'POST':
        add_type = request.POST['type']

        if add_type == "SINGLE":
            to_add = strip_tags(request.POST['username'])
            first_name = strip_tags(request.POST['firstname'])
            last_name = strip_tags(request.POST['lastname'])
            major = strip_tags(request.POST['major'])
            year = strip_tags(request.POST['class'])

            exists = User.objects.filter(username=to_add).count()
            if exists:
                context['message'].append("Username " + to_add + " is taken.")
            else:
                try:
                    utils.create_user(to_add, first_name, last_name, major, year)
                    context['message'].append("User " + to_add + " successfully added.")
                except:
                    context['message'].append("Error adding " + to_add + ".")
    return render(request, 'userinfo/secure/add.html', context)

@permission_required('UserInfo.manage_users', login_url='secure-index')
def manage_users(request):
    """
        Provides a view to manage all of the users in the system.
    """

    all_users = User.objects.all().order_by("last_name")

    context = {
        'all_users': all_users
    }

    return render(request, 'userinfo/secure/manage.html', context)

@permission_required('UserInfo.manage_users', login_url='secure-index')
def reset_password(request, user):
    """
        Resets a single user's password.
    """

    # TODO: This should be changed over to being a POST request in the future.
    requested_user = User.objects.get(username__exact=user)

    utils.reset_password(requested_user)

    return redirect("userinfo-manage_users")

@login_required
def edit_user(request, user):
    """
        Provides a view to edit a single user.
    """
    requested_user = User.objects.get(username__exact=user)
    if (not requested_user == request.user) and not request.user.is_staff:
        return redirect('pub-permission_denied')
    message = ""
    if request.method == 'POST':
        try:
            form = EditUserInfoForm(request.POST, instance=requested_user.userinfo)
            if form.is_valid():
                form.save()
                message = "Profile successfully updated"
        except UserInfo.DoesNotExist:
            new_userinfo, created = UserInfo.objects.get_or_create(user=requested_user,
                                           pledgeClass=PledgeClass.objects.get(id=request.POST["pledgeClass"]),
                                           phoneNumber=request.POST["phoneNumber"],
                                           major=request.POST["major"],
                                           hometown=request.POST["hometown"],
                                           activities=request.POST["activities"],
                                           interests=request.POST["interests"],
                                           favoriteMemory=request.POST["favoriteMemory"])
            form = EditUserInfoForm(request.POST, new_userinfo)
            message = "Profile successfully updated"
    else:
        try:
            form = EditUserInfoForm(instance=requested_user.userinfo)
        except UserInfo.DoesNotExist as e:
            form = EditUserInfoForm()

    context = {
        'requested_user': requested_user,
        'form': form,
        'error': form.errors
    }
    if message is not "":
        context['message'] = [message]

    return render(request, 'userinfo/secure/edit.html', context)

@login_required
def change_password(request):
    """
        Provides a view where a user can change their change_password
    """

    context = {
        'message': []
    }

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            context['message'].append("Password successfully changed.")
        else:
            context['message'].append("Error changing password.  Check that your passwords match and that your old password is correct.")

    context['form'] = PasswordChangeForm(user=request.user)

    return render(request, 'userinfo/secure/reset_password.html', context)


@register.filter
@stringfilter
def profile_image(url):
    if len(url) == 0:
        return "/static/img/user-placeholder.png"
    else:
        return "/content/" + url