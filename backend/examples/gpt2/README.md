# Example with the GPT-2

:exclamation: In order to try this example you have to download the GPT2 LM-Head model from https://github.com/onnx/models/blob/master/text/machine_comprehension/gpt-2/model/gpt2-lm-head-10.onnx and copy it into the directory <strong>ml-starter/backend/app/custom_model</strong> with the name <strong>custom_model.onnx</strong> :exclamation:

:exclamation: The postprocessing is not working properly yet, instead of a text, the function returns the tensor :exclamation:

## Instructions

### Local deployment

```commandline
git clone https://github.com/loki344/ml-starter.git
cd ./ml-starter
find ./backend/app/custom_model -type f ! -name '__init__.py' -delete
cp -a ./backend/examples/gpt2/. ./backend/app/custom_model
docker build -t ml-starter-gpt2-example .
docker run -d -p 80:3000 -p 8800:8800 ml-starter-gpt2-example
```
Access your browser on localhost (frontend) or localhost:8800/docs (backend)

## Result

<img style="width: 100%" src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/gpt2/gpt-1.png"/>
<br/>
<img style="width: 100%" src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/gpt2/gpt-2.png"/>





## Model input

A string to be used as a base for gpt2 to generate text. <br/>
Example: 
```json
"This is a test input to show"
```

## Configuration

The applicationName and the description are interchangeable, whereas the configuration of the input and the requestObject should match the above definition of the input data.

```json
{
  "applicationName": "My demo-application with GPT-2",
  "description": "This GPT-2 model will generate some text based on the input below. Try it out!",
  "input": [
    {
    "id": "inputText",
    "label": "Please enter some text and GPT-2 will continue",
    "type": "str"
    }
  ],
  "requestObject": {"inputData": "inputText"}

}
```

### Preprocessing

The preprocessing method uses the tokenizer to transform the input string to a tensor which is interpretable by the GPT-2 model. It wraps it in a dictionary and uses the list of input names from the input_metadata of the ONNX inferenceSession.

```python
def pre_process(self, input_data, input_metadata):

    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    inputs = torch.tensor(
        [[tokenizer.encode(input_data, add_special_tokens=True)]])
    inputs_flatten = flatten(inputs)
    inputs_flatten = update_flatten_list(inputs_flatten, [])

    ort_inputs = dict((input_metadata[i].name, to_numpy(input)) for i, input in enumerate(inputs_flatten))

    return ort_inputs
```

## Model output

The raw output of the model is a tensor, which represents the predictet tokens. #TODO explain the method as soon as it does not return tensors anymore.

Example:
```json
tensor([ -35.8891, -35.2050, -39.1337, ..., -103.8397, -107.2803, -99.9341])
```

### Postprocessing

The postprocessing is WIP at the moment and returns the tensor instead of the text.

```python
def post_process(self, model_output):
    outputs_flatten = model_output[0].flatten()
    outputs_flatten = outputs_flatten.flatten()

    predictions = torch.tensor(outputs_flatten)
    return str(predictions)
```

## Helper methods

```python

def flatten(inputs):
    return [[flatten(i) for i in inputs] if isinstance(inputs, (list, tuple)) else inputs]


def update_flatten_list(inputs, res_list):
    for i in inputs:
        res_list.append(i) if not isinstance(i, (list, tuple)) else update_flatten_list(i, res_list)
    return res_list


def to_numpy(x):
    if type(x) is not np.ndarray:
        x = x.detach().cpu().numpy() if x.requires_grad else x.cpu().numpy()
    return x

```
