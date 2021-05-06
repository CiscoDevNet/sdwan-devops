#!/usr/bin/env bash

# Uncomment the following and define proper values (or specify as environment variables)

# GITLAB_HOST=https://gitlab.example.com
# GITLAB_USER=foo
# GITLAB_API_TOKEN=abc123
# GITLAB_PROJECT=sdwan-devops
# VIRL_HOST=cml.example.com
# VIRL_USERNAME=foo
# VIRL_PASSWORD=bar
# VIRL_LAB=sdwan-devops

# Add new project
curl --request POST -sSLk --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_HOST/api/v4/projects" --form "name=$GITLAB_PROJECT"

# Add new vars
curl --request POST -sSLk --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_HOST/api/v4/projects/$GITLAB_USER%2f$GITLAB_PROJECT/variables" --form "key=VIRL_HOST" --form "value=$VIRL_HOST"
curl --request POST -sSLk --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_HOST/api/v4/projects/$GITLAB_USER%2f$GITLAB_PROJECT/variables" --form "key=VIRL_USERNAME" --form "value=$VIRL_USERNAME"
curl --request POST -sSLk --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_HOST/api/v4/projects/$GITLAB_USER%2f$GITLAB_PROJECT/variables" --form "key=VIRL_PASSWORD" --form "value=$VIRL_PASSWORD"
curl --request POST -sSLk --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_HOST/api/v4/projects/$GITLAB_USER%2f$GITLAB_PROJECT/variables" --form "key=VIRL_LAB" --form "value=$VIRL_LAB"
curl --request POST -sSLk --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" "$GITLAB_HOST/api/v4/projects/$GITLAB_USER%2f$GITLAB_PROJECT/variables" --form "key=VMANAGE_ORG" --form "value=$VMANAGE_ORG"
