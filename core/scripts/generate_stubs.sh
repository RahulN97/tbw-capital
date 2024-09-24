#!/bin/bash

openapi-generator generate -i core/generated/gds/gds_api_spec.yaml -g python -o . --additional-properties=packageName=core.generated.gds
