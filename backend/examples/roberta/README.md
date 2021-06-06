# Example with the RoBerta model


:exclamation: In order to try this example you have to download the RoBERTa-SequenceClassification from https://github.com/onnx/models/tree/master/text/machine_comprehension/roberta and copy it into the directory <strong>ml-starter/backend/app/custom_model</strong> with the name <strong>custom_model.onnx</strong> :exclamation:


### Local deployment

To run this example locally
```commandline
git clone https://github.com/loki344/ml-starter.git
cd ./ml-starter
find ./backend/app/custom_model -type f ! -name '__init__.py' -delete
cp -a ./backend/examples/roberta/. ./backend/app/custom_model
docker build -t ml-starter-roberta-example .
docker run -d -p 80:3000 -p 8800:8800 ml-starter-roberta-example
```
Access your browser on localhost (frontend) or localhost:8800/docs (backend)




## Result

<img style="width: 100%" src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/roberta/roberta-1.png"/>
<img style="width: 100%" src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/roberta/roberta-2.png"/>


## Model input

Input is a sequence of words as a string including sentiment. Example: "This film is so good". input_ids: Indices of input tokens in the vocabulary. It's a int64 tensor of dynamic shape (batch_size, sequence_length). Text tokenized by RobertaTokenizer.

### Configuration

The applicationName and the description are interchangeable, whereas the configuration of the input and the requestObject should match the above definition of the input data.

```json
{
  "applicationName": "My sentiment application with RoBERTa",
  "description": "This model determines if the sentiment of a text is good or bad. Try it!",
  "input": [
    {
    "id": "textInput",
    "label": "Enter some text",
    "type": "str"
    }
  ],
  "requestObject": {"inputData": "textInput"}

}
```


### Preprocessing

The preprocessing method is exactly the same as is used in the ONNX example from https://github.com/onnx/models/tree/master/text/machine_comprehension/roberta. 

```python
def pre_process(self, input_data, input_metadata):

    tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
    input_ids = torch.tensor(tokenizer.encode(input_data, add_special_tokens=True)).unsqueeze(0)
    ort_inputs = {input_metadata[0].name: self.to_numpy(input_ids)}

    return ort_inputs
```



## Model output

For RoBERTa-SequenceClassification model: Output of this model is a float32 tensor [batch_size, 2]

### Postprocessing

The postprocessing method is exactly the same as is used in the ONNX example from https://github.com/onnx/models/tree/master/text/machine_comprehension/roberta. 

```python
def post_process(self, model_output):

    pred = np.argmax(model_output)
    if (pred == 0):
        prediction = "The sentiment of this text is negative"
    elif (pred == 1):
        prediction = "The sentiment of this text is positive"

    return prediction
```

### Helper functions
```python
@staticmethod
def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()
```
