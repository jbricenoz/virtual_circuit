# This sample can be run in a Python3 environment
# It requires the sanic library which can be installed by running
# pip install sanic
#
# You can then run this application. 
# The endpoint will be on http://localhost:8000/virtual-circuit/

from sanic import Sanic
from sanic.response import json
from sanic.exceptions import InvalidUsage

app = Sanic(__file__)


@app.route("/virtual-circuit/<src_port:int>/<dest_port:int>", methods=["POST"])
async def test(request, src_port, dest_port):
    """
    Create a virtual circuit between src_port and dest_port

    :param src_port: Integer
    :param dest_port: Integer
    :param speed: String, only accept specific values
    :param term: Integer; If not provided, defaults to 1
    :param description: String
    """

    accepted_speeds = [
        "50Mbps",
        "100Mbps",
        "500Mbps",
        "1Gbps",
        "50Gbps",
    ]
    speed = request.json.pop("speed", None)
    term = request.json.pop("term", 1)
    description = request.json.pop("description", None)

    if speed and speed not in accepted_speeds:
        raise InvalidUsage(f"Invalid Speed provided: {speed}")

    if term:
        term = int(term)
    if term < 1:
        raise InvalidUsage("term must be greater than 0")

    if src_port <= 0:
        raise InvalidUsage("src_port must be a positive integer")
    if dest_port <= 0:
        raise InvalidUsage("dest_port must be a positive integer")

    return_dict = {
        "src_port": src_port,
        "dest_port": dest_port,
        "speed": speed,
        "term": term,
        "description": description,
    }

    return json(return_dict)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)