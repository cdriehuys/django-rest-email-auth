Changelog
=========


v0.4.3
------

Bugfixes
  * :issue:`44`: Fix issue with templates not being included in distribution.


v0.4.2
------

Bugfixes
  * :issue:`43`: Fix issue with registration view not respecting overridden registration serializer setting.


v0.4.1
------

Bugfixes
  * :issue:`40`: Fix issue with invalid admin fields.


v0.4.0
------

Features
  * :issue:`30`: Add endpoints to request/perform a password reset.
  * :issue:`37`: Allow a custom registration serializer to be provided.

Documentation
  * :issue:`29`: Fix typo with installation instructions.

Miscellaneous
  * :issue:`33`: Fix issue with deployment process breaking example project requirements.


v0.3.1
------

Make dependency versions less strict.


v0.3.0
------

Features
  * :issue:`9,25`: Add documentation and example project.
  * :issue:`10`: Add custom authentication backend.
  * :issue:`22`: Add endpoints for managing email addresses.
  * :issue:`24`: Add field to track a user's primary email address.


v0.2.1
------

Bugfixes
  * :issue:`20`: Fix for tagged releases not being deployed.


v0.2
----

Features
  * :issue:`4`: Send a verification email after registration.
  * :issue:`5`: Add an endpoint for verifying email addresses.
  * :issue:`6`: Add an endpoint for resending an email verification.
  * :issue:`7`: Add a command for cleaning up expired email confirmations.

Miscellaneous
  * :issue:`14`: Email addresses must be unique


v0.1
----

Bare-bones intial release. This is not ready for any sort of use.

Features
  * :issue:`2`: Add endpoint to register new users.
