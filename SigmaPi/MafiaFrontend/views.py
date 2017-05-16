
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseServerError
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from Mafia import mafia
from Mafia.models import *
from Mafia.errors import *
from .forms import *

@login_required
def index(request):
    return redirect('MafiaFrontend.views.play')


##############################################
# Playing
##############################################

@login_required
def play(request):
    running_games = Game.objects.exclude(day_number=0).order_by('created')
    running_games.reverse()
    game_infos = []
    for g in running_games:
        players = Player.objects.filter(game=g)
        users = [p.user for p in players]
        joined = request.user in users
        if joined:
            game_infos.append({
                'pk': g.pk,
                'name': g.name,
                'created': g.created,
                'creator_name': g.creator.get_full_name(),
                'status': g.status_string,
            })
    return render(request, 'mafia_play.html', {'game_infos': game_infos})

@login_required
def play_game(request, game_id):
    game = _id_to_game(game_id)
    return _not_implemented()


##############################################
# Joining/Leaving
##############################################

@login_required
def join(request):
    accepting_games = Game.objects.filter(
        day_number=0
    ).order_by(
        'created'
    ).exclude(
        creator=request.user
    )
    accepting_games.reverse()
    game_infos = []
    for g in accepting_games:
        players = Player.objects.filter(game=g)
        users = [p.user for p in players]
        joined = request.user in users
        game_infos.append({
            'pk': g.pk,
            'name': g.name,
            'created': g.created,
            'creator_name': g.creator.get_full_name(),
            'joined': joined,
        })
    return render(request, 'mafia_join.html', {'game_infos': game_infos})

@login_required
def join_game(request, game_id):
    if request.method != 'POST':
        return _expected_post()
    game = _id_to_game(game_id)
    return _do_and_redirect(
        fn=mafia.add_user,
        fn_args=(game, request.user,),
        redirect_to='MafiaFrontend.views.join',
    )

@login_required
def leave_game(request, game_id):
    if request.method != 'POST':
        return _expected_post()
    game = _id_to_game(game_id)
    return _do_and_redirect(
        fn=mafia.remove_user,
        fn_args=(game, request.user,),
        redirect_to='MafiaFrontend.views.join',
    )


##############################################
# Spectating
##############################################

@login_required
def spectate(request):
    running_games = Game.objects.exclude(day_number=0).order_by('created')
    running_games.reverse()
    game_infos = [
        {
            'pk': g.pk,
            'name': g.name,
            'created': g.created,
            'creator_name': g.creator.get_full_name(),
            'status': g.status_string,
        }
        for g in running_games
    ]
    return render(request, 'mafia_spectate.html', {'game_infos': game_infos})

@login_required
def spectate_game(request, game_id):
    game = _id_to_game(game_id)
    return _not_implemented()


##############################################
# Moderating
##############################################

@login_required
def moderate(request):
    games = Game.objects.filter(creator=request.user).order_by('created')
    games.reverse()
    game_infos = [
        {
            'pk': g.pk,
            'name': g.name,
            'created': g.created,
            'status': g.status_string,
        }
        for g in games
    ]
    return render(request, 'mafia_moderate.html', {'game_infos': game_infos})

@login_required
def moderate_game(request, game_id):
    game = _id_to_game(game_id)
    _check_creator(request, game)
    if game.is_accepting:
        players = Player.objects.filter(game=game).order_by('user__first_name')
        signed_up_users = [
            (
                p.user.get_full_name(),
                Role.get_instance(p.role).faction if p.role else '',
                p.role if p.role else '',
                p.user.username
            )
            for p in players
        ]
        add_user_form = AddUserToGameForm(game)
        role_errors = mafia.check_role_counts(game) + mafia.check_faction_counts(game)
        roles = [('', '(Unassigned)')] + [
            (role.code, role.name) for role in Role.get_instances()
        ]
        return render(request, 'mafia_moderate_game_accepting.html', {
            'game': game,
            'signed_up_users': signed_up_users,
            'add_user_form': add_user_form,
            'roles': roles,
            'role_errors': role_errors,
        })
    else:
        return _not_implemented()

@login_required
def add_game(request):
    if request.method == 'POST':
        form = AddGameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            game = Game(name=name, created=datetime.now(), creator=request.user)
            game.save()
            return redirect('MafiaFrontend.views.moderate')
        else:
            return render(request, 'mafia_add_game.html', {'form': form})
    else:
        form = AddGameForm()
        return render(request, 'mafia_add_game.html', {'form': form})

@login_required
def add_user_to_game(request, game_id, username=None):
    game = _id_to_game(game_id)
    _check_creator(request, game)
    if request.method == 'POST':
        form = AddUserToGameForm(None, request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            return _do_and_redirect(
                fn=mafia.add_user,
                fn_args=(game, user),
                redirect_to='MafiaFrontend.views.moderate_game',
                game_id=game_id,
            )
        else:
            return redirect(reverse('MafiaFrontend.views.moderate_game', args=(game_id,)))
    
    else:
        return _expected_post()

@login_required
def remove_user_from_game(request, game_id):
    try:
        (username,) = _get_post_data(request, 'username')
    except BadPostRequestError as e:
        return _bad_request(e)
    game = _id_to_game(game_id)
    _check_creator(request, game)
    user = _username_to_user(username)
    return _do_and_redirect(
        fn=mafia.remove_user,
        fn_args=(game, user),
        redirect_to='MafiaFrontend.views.moderate_game',
        game_id=game_id,
    )

@login_required
def assign_role(request, game_id):
    try:
        (username, role_code) = _get_post_data(request, 'username', 'role_code')
    except BadPostRequestError as e:
        return _bad_request(e)
    game = _id_to_game(game_id)
    _check_creator(request, game)
    user = _username_to_user(username)
    return _do_and_redirect(
        fn=mafia.assign_role,
        fn_args=(game, user, role_code),
        redirect_to='MafiaFrontend.views.moderate_game',
        game_id=game_id,
    )


##############################################
# Utilities
##############################################

class BadPostRequestError(Exception):
    pass

def _get_post_data(request, *keys):
    if request.method != 'POST':
        raise BadPostRequestError('Endpoint only accepts POST requests')
    result = []
    for key in keys:
        if key not in request.POST:
            raise BadPostRequestError('POST data missing key: ' + key)
        result.append(request.POST[key])
    return tuple(result)

def _expected_post():
    return _bad_request('Endpoint only accepts POST requests')

def _id_to_game(game_id):
    try:
        return Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404('Invalid game ID: ' + game_id2)

def _username_to_user(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404('Invalid username: ' + username)

def _do_and_redirect(fn, fn_args, redirect_to, **redirect_kwargs):
    try:
        fn(*fn_args)
    except MafiaUserError as e:
        raise Http404(e.message)
    except MafiaError as e:
        return _server_error(e)
    return redirect(reverse(redirect_to, kwargs=redirect_kwargs))

def _bad_request(err):
    return HttpResponse(
        '<h1>400: Bad Request</h1><p>' + err.message + '</p>',
        status=400
    )

def _server_error(err):
    print 'INTERNAL MAFIA ERROR: ' + `err`
    return HttpResponseServerError('''
        <h1>500: Internal server error</h1>
        <h3>Please contact the webmaster</h3>
    ''')

def _not_implemented():
    return HttpResponse('''
        <h1>501: Not implemented</h1>
        <h3>Please contact the webmaster</h3>
    ''', status=501)

def _check_creator(request, game):
    if game.creator != request.user:
        raise PermissionDenied()