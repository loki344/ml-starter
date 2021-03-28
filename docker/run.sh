helpFunction()
{
   echo ""
   echo "Usage: $0 -d directoryPath -s sourceCodeFileName -m modelFileName"
   echo -e "\t-d Path to the directory where the model and the sourceCodeFile is located"
   echo -e "\t-s name of the pythonFile containing the pre- and postprocess methods e.g. 'methods.py'"
   echo -e "\t-m name of the model file e.g. 'model.onnx'"
   exit 1 # Exit script after printing help
}

while getopts "d:s:m:" opt
do
   case "$opt" in
      d ) parameterD="$OPTARG" ;;
      s ) parameterS="$OPTARG" ;;
      m ) parameterM="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$parameterD" ] || [ -z "$parameterS" ] || [ -z "$parameterM" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

cp -u ../requirements.txt ./ml-starter-backend
cp -u -r ../app ./ml-starter-backend

export MODEL_FILE_NAME=$parameterM
export SOURCE_CODE_FILE=$parameterS
export DIRECTORY_PATH=$parameterD


docker-compose up
