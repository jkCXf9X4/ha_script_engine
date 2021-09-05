echo "Removing docs"
rm -r .\docs
echo "Docs removed"

echo "Creating docs"
pdoc -o .\docs --skip-errors .\custom_components\script_engine
echo "Docs created"