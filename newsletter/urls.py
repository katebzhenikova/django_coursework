from django.urls import path

from newsletter import views
from newsletter.apps import NewsletterConfig
from newsletter.views import ClientCreateView, ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView, \
    NewsletterMessageListView, NewsletterMessageDetailView, NewsletterMessageCreateView, NewsletterMessageUpdateView, \
    NewsletterMessageDeleteView, NewsletterSettingsListView, NewsletterSettingsDetailView, NewsletterSettingsCreateView, \
    NewsletterSettingsUpdateView, NewsletterSettingsDeleteView, NewsletterLogView, NewsletterSettingsModerationView, \
    HomepageView

app_name = NewsletterConfig.name


urlpatterns = [

    path('client/', ClientListView.as_view(), name='client_list'),
    path('client/view/<int:pk>/', ClientDetailView.as_view(), name='view_client'),
    path('client/create/', ClientCreateView.as_view(), name='create_client'),
    path('client/edit/<int:pk>/', ClientUpdateView.as_view(), name='edit_client'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),

    path('newslettermessage/', NewsletterMessageListView.as_view(), name='newslettermessage_list'),
    path('newslettermessage/view/<int:pk>/', NewsletterMessageDetailView.as_view(), name='view_newslettermessage'),
    path('newslettermessage/create/', NewsletterMessageCreateView.as_view(), name='create_newslettermessage'),
    path('newslettermessage/edit/<int:pk>/', NewsletterMessageUpdateView.as_view(), name='edit_newslettermessage'),
    path('newslettermessage/delete/<int:pk>/', NewsletterMessageDeleteView.as_view(), name='delete_newslettermessage'),

    path('newslettersettings/', NewsletterSettingsListView.as_view(), name='mail_list'),
    path('newslettersettings/view/<int:pk>/', NewsletterSettingsDetailView.as_view(), name='view_mail'),
    path('newslettersettings/create/', NewsletterSettingsCreateView.as_view(), name='create_mail'),
    path('newslettersettings/edit/<int:pk>/', NewsletterSettingsUpdateView.as_view(), name='edit_mail'),
    path('newslettersettings/delete/<int:pk>/', NewsletterSettingsDeleteView.as_view(), name='delete_mail'),
    # path('mail/activity/<int:pk>/', toogle_activity, name='toogle_activity'),
    path('newslettersettings/<int:pk>/newsletterlog/', NewsletterLogView.as_view(), name='newsletterlog_list'),
    path('sending/<int:pk>/moderate', NewsletterSettingsModerationView.as_view(), name='sending_moderation'),
    path('newslettersettings/', HomepageView.as_view(), name='homepage'),
]









