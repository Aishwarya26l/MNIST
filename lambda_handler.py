try:
    import requests
except ImportError:
    from botocore.vendored import requests
import json
import base64
import os
import ast


def getIndexPage():
    indexPage = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>MNIST</title>
            <link 
                rel="stylesheet" 
                href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" 
                integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" 
                crossorigin="anonymous">
            </link>
            <style type="text/css">
                .app {
                    margin: 10px;
                }
                table {
                    font-size: smaller;
                }
                #hidden {
                    visibility: hidden;
                }
                #title-text {
                    margin: auto;
                    font-size: 1.5rem;
                }
            </style>
        </head>
        <body>
            <div>
                <nav class="navbar navbar-dark bg-primary">
                    <a id="title-text" class="navbar-brand" href="#">MNIST : Draw a Digit</a>
                </nav>
                <div class="row app">
                    <div class="col-md-6">
                        <div class="row">
                            <h5>&nbsp;&nbsp;Enter your colab notebook url or use default :</h5>
                            <div class="col-md-8">
                                <input
                                    id="colab-url"
                                    class="form-control"
                                    type="text"
                                    placeholder="https://colab.research.google.com/drive/1j65v9d9sMaChxRaouvHDd88W9vsWNekk"
                                    value="https://colab.research.google.com/drive/1j65v9d9sMaChxRaouvHDd88W9vsWNekk"
                                />
                                <p id="test"></p>
                            </div>
                                <button id="clear" type="button" class="btn btn-secondary">
                                    clear
                                </button>
                        </div>
                        <br/>
                        <canvas id="main"></canvas>
                    </div>
                    <div class="col-md-6">
                    <h5>Input :</h5>
                    <canvas
                        id="input"
                        style="border:1px solid"
                        width="140"
                        height="140"
                    ></canvas>
                    <hr />
                    <h5>Output :</h5>
                    <table id="output" class="table table-sm">
                        <thead class="thead-light">
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">Simple</th>
                            <th scope="col">Convolutional</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr>
                            <th scope="row">0</th>
                            <td></td>
                            <td></td>
                        </tr>
                        <tr>
                            <th scope="row">1</th>
                            <td></td>
                            <td></td>
                        </tr>
                        <tr>
                            <th scope="row">2</th>
                            <td></td>
                            <td></td>
                        </tr>
                        <tr>
                            <th scope="row">3</th>
                            <td></td>
                            <td></td>
                        </tr>
                        <tr>
                            <th scope="row">4</th>
                            <td></td>
                            <td></td>
                        </tr>
                        <tr>
                            <th scope="row">5</th>
                            <td></td>
                            <td></td>
                        </tr>
                        <tr>
                            <th scope="row">6</th>
                            <td></td>
                            <td></td>
                        </tr>
                        <tr>
                            <th scope="row">7</th>
                            <td></td>
                            <td></td>
                        </tr>
                        <tr>
                            <th scope="row">8</th>
                            <td></td>
                            <td></td>
                        </tr>
                        <tr>
                            <th scope="row">9</th>
                            <td></td>
                            <td></td>
                        </tr>
                        </tbody>
                    </table>
                    </div>
                </div>
                <p id="hidden">Not Initialised</p>
            </div>
        </body>
        <script 
            src="https://code.jquery.com/jquery-3.4.1.min.js" 
            integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" 
            crossorigin="anonymous">
        </script>
        <script>
            /*global $*/
        class Main {
            constructor() {
                this.canvas = document.getElementById('main');
                this.input = document.getElementById('input');
                this.canvas.width  = 449; // 16 * 28 + 1
                this.canvas.height = 449; // 16 * 28 + 1
                this.ctx = this.canvas.getContext('2d');
                this.canvas.addEventListener(
                    'mousedown', this.onMouseDown.bind(this));
                this.canvas.addEventListener(
                    'mouseup',   this.onMouseUp.bind(this));
                this.canvas.addEventListener(
                    'mousemove', this.onMouseMove.bind(this));
                this.initialize();
            }
            initialize() {
                this.ctx.fillStyle = '#FFFFFF';
                this.ctx.fillRect(0, 0, 449, 449);
                this.ctx.lineWidth = 1;
                this.ctx.strokeRect(0, 0, 449, 449);
                this.ctx.lineWidth = 0.05;
                $('#hidden').text('Initialised');
                $('#output td').text('').removeClass('table-success');
            }
            onMouseDown(e) {
                this.canvas.style.cursor = 'default';
                this.drawing = true;
                this.prev = this.getPosition(e.clientX, e.clientY);
            }
            onMouseUp() {
                this.drawing = false;
                this.drawInput();
            }
            onMouseMove(e) {
                if (this.drawing) {
                    var curr = this.getPosition(e.clientX, e.clientY);
                    this.ctx.lineWidth = 16;
                    this.ctx.lineCap = 'round';
                    this.ctx.beginPath();
                    this.ctx.moveTo(this.prev.x, this.prev.y);
                    this.ctx.lineTo(curr.x, curr.y);
                    this.ctx.stroke();
                    this.ctx.closePath();
                    this.prev = curr;
                }
            }
            getPosition(clientX, clientY) {
                var rect = this.canvas.getBoundingClientRect();
                return {
                    x: clientX - rect.left,
                    y: clientY - rect.top
                };
            }
            drawInput() {
                var ctx = this.input.getContext('2d');
                var img = new Image();
                img.onload = () => {
                    if($('#hidden').text() == 'Initialised'){
                        $('#hidden').text("Done");
                        return;
                    }
                    var inputs = [];
                    var small = document.createElement('canvas').getContext('2d');
                    small.drawImage(img, 0, 0, img.width,
                                    img.height, 0, 0, 28, 28);
                    var data = small.getImageData(0, 0, 28, 28).data;
                    for (var i = 0; i < 28; i++) {
                        for (var j = 0; j < 28; j++) {
                            var n = 4 * (i * 28 + j);
                            inputs[i * 28 + j] = (data[n + 0] + \
                                                  data[n + 1] + data[n + 2]) / 3;
                            ctx.fillStyle = 'rgb(' + [data[n + 0],
                                                 data[n + 1], data[n + 2]].join(',') + ')';
                            ctx.fillRect(j * 5, i * 5, 5, 5);
                        }
                    }
                    if (Math.min(...inputs) === 255) {
                        return;
                    }
                    var dataReq = {"inputs": inputs,"colabUrl" : $('#colab-url').val()}
                    $('#test').text('Loading results please wait....');
                    $.ajax({
                        url: '',
                        method: 'POST',
                        contentType: 'application/json',
                        data: JSON.stringify(dataReq),
                        success: (data) => {
                            $('#test').text('');
                            for (var i = 0; i < 2; i++) {
                                var max = 0;
                                var max_index = 0;
                                for (var j = 0; j < 10; j++) {
                                    var value = Math.round(data.results.mnist[i][j] * 1000);
                                    if (value > max) {
                                        max = value;
                                        max_index = j;
                                    }
                                    var digits = String(value).length;
                                    for (var k = 0; k < 3 - digits; k++) {
                                        value = '0' + value;
                                    }
                                    var text = '0.' + value;
                                    if (value > 999) {
                                        text = '1.000';
                                    }
                                    $('#output tr').eq(j + 1).find('td').eq(i).text(text);
                                }
                                for (var j = 0; j < 10; j++) {
                                    if (j === max_index) {
                                        $('#output tr').eq(j + 1).find('td').eq(i).addClass('table-success');
                                    } else {
                                        $('#output tr').eq(j + 1).find('td').eq(i).removeClass('table-success');
                                    }
                                }
                            }
                        },
                        error: (data) => {
                            $('#test').text(JSON.stringify(data.responseJSON));
                        }
                    });
                };
                img.src = this.canvas.toDataURL();
            }
        }

        $(() => {
            var main = new Main();
            $('#clear').click(() => {
                main.initialize();
            });
        });

        </script>
        </html>
        """
    return indexPage


def get_notebook_from_colab_url(url):
    docId = url.split("drive/")[1]
    url = "https://drive.google.com/uc?export=download&id=" + docId
    content = requests.get(url).json()
    return content


def lambda_handler(event, context):
    method = event.get('httpMethod', {})
    if method == 'GET':
        response = {
            "statusCode": 200,
            "body": getIndexPage(),
            "headers": {
                'Content-Type': 'text/html',
            }
        }
        return response
    if method == 'POST':
        reqBody = json.loads(event.get('body', {}))
        inputs = {"inputs": reqBody['inputs']}
        colabUrl = reqBody['colabUrl']
        print("Request body : " + str(reqBody))
        notebook = get_notebook_from_colab_url(colabUrl)
        fileInfo = {
            "inputs.json": str(base64.b64encode(bytes(json.dumps(inputs), "utf-8")))[2: -1]
        }
        payload = json.loads(json.dumps({
            "notebook": notebook,
            "files": fileInfo
        }))
        print(json.dumps(payload))
        jupyterNbExecuter = os.environ['jupyterNbExecuter']
        modelResponse = requests.post(jupyterNbExecuter, json=payload)
        print(modelResponse.json())
        if(modelResponse.status_code == 200):
            if(str(modelResponse.json()[
                    "ipynb"]["cells"]).find("ename") != -1):
                response = {
                    "statusCode": 500,
                    "headers": {
                        "Content-Type": "application/json",
                    },
                    "body": json.dumps({
                        "results": "Error while executing notebook"
                    })
                }
            elif(modelResponse.json()["result"]):
                print(modelResponse.json()["result"])
                print(type(modelResponse.json()["result"]))
                # json.loads(json.dumps(ast.literal_eval(json_data)))["results"]
                # print(json.loads(modelResponse.json()["result"]))
                results = json.loads(json.dumps(ast.literal_eval(
                    modelResponse.json()["result"])))["results"]
                response = {
                    "statusCode": 200,
                    "headers": {
                        "Content-Type": "application/json",
                    },
                    "body":  json.dumps({
                        "results": results
                    })
                }
            else:
                response = {
                    "statusCode": 500,
                    "headers": {
                        "Content-Type": "application/json",
                    },
                    "body":  json.dumps({
                        "results": "results.json file is empty"
                    })
                }
        else:
            response = {
                "statusCode": 500,
                "headers": {
                    "Content-Type": "application/json",
                },
                "body":  json.dumps({
                    "results": "Error"
                })
            }

        print("Response : " + json.dumps(response))
        return response
