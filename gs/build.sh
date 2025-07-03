export CC=/usr/bin/gcc-11
export CXX=/usr/bin/g++-11

python setup.py clean
rm -rf build
pip install -e .
