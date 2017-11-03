========
Commands
========

The app contains some additional commands that can be run from ``manage.py``.

.. _clean-email-confirmations:

Cleaning Expired Email Confirmations
====================================

Command: ``cleanemailconfirmations``

This command deletes any old, expired email confirmations. The duration that an expired confirmation will be saved is specified in the :ref:`confirmation-save-period` setting.
