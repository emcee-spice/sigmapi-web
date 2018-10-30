"""
URLs for PartyListV2 app.
"""

from django.conf.urls import url
from django.views.generic import RedirectView

from . import views, api

urlpatterns = [
    url(
        regex=r'^$',
        view=RedirectView.as_view(pattern_name='partylist-index'),
        name='partylist-index-redirect',
    ),
    url(
        regex=r'^all/$',
        view=views.index,
        name='partylist-index',
    ),
    url(
        regex=r'^add/$',
        view=views.add_party,
        name='partylist-add_party',
    ),
    url(
        regex=r'^restricted-guests/$',
        view=views.restricted_lists,
        name='partylist-restricted_lists',
    ),
    url(
        regex=r'^restricted-guests/blacklist/remove/(?P<bl_id>[\d]+)/$',
        view=views.remove_blacklisting,
        name='partylist-remove_blacklisting',
    ),
    url(
        regex=r'^restricted-guests/graylist/remove/(?P<gl_id>[\d]+)/$',
        view=views.remove_graylisting,
        name='partylist-remove_graylisting',
    ),
    url(
        regex=r'^manage/$',
        view=views.manage_parties,
        name='partylist-manage_parties',
    ),
    url(
        regex=r'^edit/(?P<party_id>[\d]+)/$',
        view=views.edit_party,
        name='partylist-edit_party',
    ),
    url(
        regex=r'^delete/(?P<party_id>[\d]+)/$',
        view=views.delete_party,
        name='partylist-delete_party',
    ),
    url(
        regex=r'^view/(?P<party_id>[\d]+)/guests/$',
        view=views.guests,
        name='partylist-guests',
    ),
    url(
        regex=r'^view/(?P<party_id>[\d]+)/stats/$',
        view=views.stats,
        name='partylist-stats',
    ),
    # API ENDPOINTS
    url(
        regex=r'^api/(?P<party_id>[\d]+)/details/$',
        view=api.get_details,
        name='partylist-api-details',
    ),
    url(
        regex=r'^api/(?P<party_id>[\d]+)/guests/create/$',
        view=api.create_guest,
        name='partylist-api-create',
    ),
    url(
        regex=(
            r'^api/(?P<party_id>[\d]+)/guests/destroy/'
            r'(?P<party_guest_id>[\d]+)/$'
        ),
        view=api.destroy_guest,
        name='partlist-api-destroy',
    ),
    url(
        regex=(
            r'^api/(?P<party_id>[\d]+)/guests/signIn/'
            r'(?P<party_guest_id>[\d]+)/$'
        ),
        view=api.sign_in,
        name='partylist-api-signin',
    ),
    url(
        regex=(
            r'^api/(?P<party_id>[\d]+)/guests/signOut/'
            r'(?P<party_guest_id>[\d]+)/$'
        ),
        view=api.sign_out,
        name='partylist-api-signout',
    ),
    url(
        regex=r'^api/(?P<party_id>[\d]+)/guests/export/$',
        view=api.export_list,
        name='partylist-api-export_list',
    ),
    url(
        regex=(
            r'^api/(?P<party_id>[\d]+)/guests/$'
        ),
        view=api.get_guests,
        name='partylist-api-get_all',
    ),
    url(
        regex=r'^api/(?P<party_id>[\d]+)/restricted/$',
        view=api.get_restricted_guests,
        name='partylist-api-restricted_guests',
    ),
    url(
        regex=r'^api/(?P<party_id>[\d]+)/permissions/$',
        view=api.get_permissions,
        name='partylist-api-get_permissions',
    ),
    url(
        regex=r'^api/(?P<party_id>[\d]+)/pulse/$',
        view=api.party_pulse,
        name='partylist-api-pulse',
    ),
    url(
        regex=r'^api/(?P<party_id>[\d]+)/guests/delta/(?P<update_counter>[\d]+)',
        view=api.get_delta_guests,
        name='partylist-api-delta_guests',
    ),
    url(
        regex=r'^api/(?P<party_id>[\d]+)/partyCount',
        view=api.modify_party_count,
        name='partylist-api-modify_party_count',
    ),
    url(
        regex=r'^api/refresh-guest-json',
        view=api.refresh_guest_json,
        name='partylist-api-refresh_guest_json',
    ),
]
