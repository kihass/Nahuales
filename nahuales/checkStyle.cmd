echo off
cls
:: http://aboumrad.info/essential-python-tools-quality.html
:: python -m this
:: pip install pep8
:: pip install pyflakes
:: pip install flake8
:: pip install hacking
:: pip install pylint
:: pip install radon
:: pip install mastool

:: pep8 --ignore=W191 acoatl.py
:: pep8 --ignore=W191 chaahk.py
:: pep8 --ignore=W191 cipher.py
:: pep8 --ignore=W191 descipher.py
:: pep8 --ignore=W191 myBytesTools.py
:: pep8 --ignore=W191 myCircularFileLists.py
:: pep8 --ignore=W191 myTools.py
:: pep8 --ignore=W191 nahuales.py
:: pep8 --ignore=W191 tests_nahuales.py

:: pyflakes acoatl.py
:: pyflakes chaahk.py
:: pyflakes cipher.py
:: pyflakes descipher.py
:: pyflakes myBytesTools.py
:: pyflakes myCircularFileLists.py
:: pyflakes myTools.py
:: pyflakes nahuales.py
:: pyflakes tests_nahuales.py

flake8 --ignore=W191,H903 nahuales.py

flake8 --ignore=W191,H903 acoatl.py
flake8 --ignore=W191,H903 chaahk.py
flake8 --ignore=W191,H903 cipher.py
flake8 --ignore=W191,H903 descipher.py
flake8 --ignore=W191,H903 myBytesTools.py
flake8 --ignore=W191,H903 myCircularFileLists.py
flake8 --ignore=W191,H903 myTools.py
flake8 --ignore=W191,H903 unitary_tests/tests_nahuales.py

flake8 --ignore=W191,H903 gnpas/dpbprw.py

:: pylint coatl.py
:: pylint chaahk.py
:: pylint cipher.py
:: pylint descipher.py
:: pylint myBytesTools.py
:: pylint myCircularFileLists.py
:: pylint myTools.py
:: pylint nahuales.py
:: pylint tests_nahuales.py

:: radon cc acoatl.py
:: radon cc chaahk.py
:: radon cc cipher.py
:: radon cc descipher.py
:: radon cc myBytesTools.py
:: radon cc myCircularFileLists.py
:: radon cc myTools.py
:: radon cc nahuales.py
:: radon cc tests_nahuales.py

:: mastool acoatl.py
:: mastool chaahk.py
:: mastool cipher.py
:: mastool descipher.py
:: mastool myBytesTools.py
:: mastool myCircularFileLists.py
:: mastool myTools.py
:: mastool nahuales.py
:: mastool tests_nahuales.py

PAUSE
echo on
