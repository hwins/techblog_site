The settings folder and its files allow easy modification for development
testing via files in the control folder and override_settings module.

To overlay specific django settings from what would be in production,
add them to override_settings.py. 

Example:

DEBUG = True

and so on.

Do not include override_settings.py in production.

Put secret keys and database passwords in .private files in control folder.
This way they can be more secure. In addition they can have different values.
Use (*.private) in .gitignore.