release: clean
	python3 setup.py sdist bdist_wheel

test:
	twine upload -r testpypi dist/*

prepare:
	python3 -m pip install --upgrade setuptools wheel

clean:
	rm -rf build dist	

