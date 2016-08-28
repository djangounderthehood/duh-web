============
Slakslakslak
============

Welcome to ``slakslakslak``, the over-engineered Slack auto-inviter with a
terrible name!

Here are the workflows that are currently supported:


Tito Webhook
------------

1) An attendee signs up and get a ticket on Tito
2) Tito triggers a webhook on our end
3) We save the attendee data and send them an email with a unique link
4) When visiting that link, the attendee can edit their data before signing up
   to out Slack (name, email, channels to join)
5) When submitting the form, we use a private Slack API to invite the attendee
6) They receive an email from Slack to finalize their account creation.


Manual CSV upload
-----------------

1) Download the attendee CSV on tito
2) Use the "Upload CSV" button in the "Slakslakslak/Invitation" admin page
3) Select invitations to send (use filtering) and choose the "send emails"
   admin action.
4) The rest is the same as the previous workflow.


The ``send_invites`` command
----------------------------

Optionally, you can use ``./manage.py send_invites`` to send all pending
invitations.
