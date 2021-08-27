#!/usr/bin/env bash

# Uncomment the following and define proper values (or specify as environment variables)

# GITLAB_HOST=https://gitlab.example.com
# GITLAB_USER=foo
# GITLAB_API_TOKEN=abc123
# GITLAB_PROJECT=sdwan-devops

# Delete project
curl --request DELETE -sSLk --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_HOST/api/v4/projects/$GITLAB_USER%2f$GITLAB_PROJECT/"
