python -m nuitka ^
  --standalone ^
  --clang ^
  --assume-yes-for-downloads ^
  --enable-plugin=numpy ^
  --enable-plugin=pyside6 ^
  --include-data-files=data\dmc_readable.parquet=data\dmc_readable.parquet ^
  --include-data-files=data\InputAnImage.png=data\InputAnImage.png ^
  .\StitchBuilderGraphical\stitchbuildergraphical.py
