<<<<<<< HEAD
=======
<<<<<<< HEAD
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
=======

>>>>>>> 189608c909cf437c2d8bfea0aafa445bf4172ede
>>>>>>> 9ff2f24294ef21ce0325f374f0cc082d46302804
import os
import sys
from dotenv import load_dotenv

<<<<<<< HEAD
load_dotenv()

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

=======

<<<<<<< HEAD
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
=======


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')
>>>>>>> 189608c909cf437c2d8bfea0aafa445bf4172ede
>>>>>>> 9ff2f24294ef21ce0325f374f0cc082d46302804
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
