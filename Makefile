trans_init:
	mkdir translations -p
	pybabel extract -F babel.cfg -k lazy_gettext -o translations/messages.pot .
	pybabel init -i translations/messages.pot -d translations -l uk
	pybabel init -i translations/messages.pot -d translations -l ru

trans_update:
	pybabel extract -F babel.cfg -k lazy_gettext -o translations/messages.pot .
	pybabel update -i translations/messages.pot -d translations
	pybabel compile -d translations -f
