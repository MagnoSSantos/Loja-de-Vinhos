#!/bin/bash

host="$1"
shift
cmd="$@"

until mysqladmin ping -h "$host" --silent; do
  >&2 echo "MySQL está indisponível - aguardando"
  sleep 3
done

>&2 echo "MySQL está pronto - executando comando"
exec $cmd
