#!/usr/bin/env bash
pylint Raytracer -d invalid-name -d unused-argument -d no-self-use --max-attributes 20
