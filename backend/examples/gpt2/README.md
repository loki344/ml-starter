# Example with the GPT-2

The ONNX model included in this example is the pretrained version available on https://github.com/onnx/models/tree/master/text/machine_comprehension/gpt-2.

## Instructions
To run this example locally
```commandline
git clone https://github.com/loki344/ml-starter.git
find ./backend/app/custom_model -type f ! -name '__init__.py' -delete
cp -a ./backend/examples/gpt2/. ./backend/app/custom_model
docker run #WIP
```

To deploy it on www.heroku.com
```commandline
#TBD
```
