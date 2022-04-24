from setuptools import setup

setup(
    name='gjrbotlib',
    version='0.3.0',    
    description='Common files for the GJR telegram bots',
    url='https://github.com/gj-regensburg/gjr-telegram-common',
    author='Benjamin Huth',
    author_email='benjamin.huth@gj-regensburg.de',
    license='MIT License',
    packages=['gjrbotlib'],
    install_requires=['python-telegram-bot',
                      'arrow',                     
                      'icalendar',
                      'recurring_ical_events'],
)
