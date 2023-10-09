#!/bin/bash

python generate_db.py 1000 1000000 &
python reconcillation_tl.py 