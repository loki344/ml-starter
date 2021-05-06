import json

from file_helper import get_file
from configuration.configuration_exception import ConfigurationException


class ConfigurationService:
    """Service to provide the key value pairs of the configMap.json"""

    def __init__(self):
        """Initializes values and loads the configuration from the configMap.json.
        Also validates the configuration."""

        self.config_map = get_file('configMap.json')
        self.model_output_names = None
        self.db_name = ''
        self.db_credentials = ''
        self.db_user = ''
        self.cluster_name = ''
        self.request_object = {}
        self.input_fields = []
        self.description = "Please provide the data in the input fields below and start the prediction."
        self.application_name = "My ML-starter demo application"
        self.supported_field_types = {'number': 1, 'str': 1, "image": 1}

        self.read_config()
        self.validate()

    def read_config(self) -> None:
        """Reads the available config-keys from the configMap.json"""

        if self.config_map.is_file():
            print("-------------------------------------------------------------------------------------------------------")
            print("Loading config file...")
            config = json.load(open(self.config_map))
            if 'modelOutputNames' in config:
                self.model_output_names = config['modelOutputNames']

            if 'input' in config:
                self.input_fields = config['input']

            if 'applicationName' in config:
                self.application_name = config['applicationName']

            if 'description' in config:
                self.description = config['description']

            if 'requestObject' in config:
                self.request_object = config['requestObject']

            if 'dbName' in config:
                self.db_name = config['dbName']

            if 'dbCredentials' in config:
                self.db_credentials = config['dbCredentials']

            if 'dbUser' in config:
                self.db_user = config['dbUser']

            if 'clusterName' in config:
                self.cluster_name = config['clusterName']

    def validate(self) -> None:
        """Validates the configuration. More precisely checks if all field types of the inputFields
         are supported and all of them are used in the requestObject

         :return: None
         """

        print("-------------------------------------------------------------------------------------------------------")
        print("Validating config file...")

        for attribute in self.__dict__:
            print("Found key: " + str(attribute) + " with value: " + str(self.__dict__.get(attribute)))

        print("Found " + str(len(self.input_fields)) + " input_fields to validate")
        for input_field in self.input_fields:

            print("validating.. " + str(input_field))

            if not self.request_object.__str__().__contains__(input_field['id']):
                raise ConfigurationException(input_field['id'], "The inputfield with the key " + input_field['id'] + " is defined in the input_fields but never used in the requestObject")

            if self.supported_field_types.get(input_field['type'], -1) == -1:
                raise ConfigurationException(input_field['id'], "The inputfield with the key " + input_field['id'] +
                                             " has an unsupported field type: " + input_field['type'] +
                                             ". Should be one of: " + str(self.supported_field_types))

        #TODO print a prototype of the requestobject
        print("")

        print("finished input_field validation")

