rm *.png
for f in $(find . | grep .py | grep -v .pyc); do
../pyan.py "$f" --dot >> "$(basename $f).gv"
done
for f in $(ls *.gv); do
dot "$f" -Tpng -O
done
rm *.gv
