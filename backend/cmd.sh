 #!/bin/sh

if [ -z "$PORT" ]
then
      export PORT=8081
      echo Exported port $PORT
fi
