# Update existing Conda environment based on environment.yml
conda-clean:
	conda env update -f environment.yml --prune
