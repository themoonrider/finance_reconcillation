# Reconcillation reports with YAML config \
1. Users define report parameters in the config file\
2. Provide MODULE_NAME as the directory name that holds stage_logic and config file 
(`reconcillation`) and FILENAME of the config file in the main script `reconcillation_tl.py`\
3. Run the main script `python reconcillation_tl.py`\
4. Reports will be generated in MODULE_NAME/reports directory\

# Build and run in Docker container\

1. Clone the repo
`git clone https://github.com/themoonrider/finance_reconcillation.git`

2. Build docker image
`docker build --no-cache -t reconcillation:v1 .`

3. Run the image in container
`docker run reconcillation:v1`

4. Once finished, export all reports to host to view
`docker cp {container_id}:/app/reconcillation/reports ./reconcillation/reports`

