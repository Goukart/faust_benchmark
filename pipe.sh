# !/bin/bash

# Requires images in "render_out"
# RUN
# ./pipe.sh imageRegex="./mm_out/.*[0]-.*.png" resolution=348 output="render" skipTo=0

# necesarry parameters:
# expression to select images -> will be used in micmac as well
for P; do
  eval $P
done

# things to consider:
# mm_out and those directories should be created by script

# Inject the rendered images with real meta data
conda activate faust
python3 inject.py ".*render.*png"
conda deactivate

# Prepare directory for micmac and run micmac
# rm -r $(find mm_out/ -mindepth 1 -maxdepth 1 ! -name "micmac.sh")
mv injection_out/* mm_out/
./micmac.sh imageRegex=$imageRegex resolution=$resolution output=$output skipTo=$skipTo

# copy to path and create if it does not exist
# mkdir -p /foo/bar && cp myfile "$_"
# mkdir -p "$d" && cp file "$d"
# rsync -a myfile /foo/bar/
