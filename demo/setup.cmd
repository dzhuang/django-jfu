virtualenv venv
venv\scripts\activate
pip install -r requirments.txt
pushd ..
python setup.py install
popd
mkdir media
mkdir static
python manage.py bower install --noinput
python manage.py syncdb --noinput
python manage.py collectstatic --noinput
echo "Setup Complete."
