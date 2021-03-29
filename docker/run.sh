helpFunction()
{
   echo ""
   echo "Usage: $0 -d directoryPath -s sourceCodeFileName -m modelFileName"
   echo -e "\t-m name of the model file e.g. 'model.onnx'"
   exit 1 # Exit script after printing help
}

while getopts "m:" opt
do
   case "$opt" in
      m ) parameterM="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$parameterM" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

cp -u ../requirements.txt ./ml-starter-backend
cp -u -r ../app ./ml-starter-backend

export MODEL_FILE_NAME=$parameterM


#docker-compose up
