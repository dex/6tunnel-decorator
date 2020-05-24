from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json

class Controller(BaseHTTPRequestHandler):
  def sync(self, object, attachments):
    # Generate the desired attachment object(s).
    try:
        port = int(object["metadata"]["annotations"]["ipv6-node-port"])
    except ValueError:
        port = 0
    if port <= 0 or port >= 65536:
        return {}

    desired_attachments = [
      {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
          "name": "ipv6-node-port-%d" % port
        },
        "spec": {
          "replicas": 1,
          "selector": {
              "matchLabels": {
                  "app": "ipv6-node-port-%d" % port
              }
          },
          "template": {
              "metadata": {
                  "labels": {
                      "app": "ipv6-node-port-%d" % port
                  }
              },
              "spec": {
                  "containers": [
                      {
                          "name": "6tunnel",
                          "image": "bastianlemke/docker-6tunnel:latest",
                          "command": ["6tunnel", "-d", "-6", str(port), "localhost", str(port)],
                          "hostNetwork": "true"
                      }
                  ]
              }
          }
        }
      }
    ]

    return {"attachments": desired_attachments}

  def do_POST(self):
    # Serve the sync() function as a JSON webhook.
    observed = json.loads(self.rfile.read(int(self.headers.getheader("content-length"))))
    desired = self.sync(observed["object"], observed["attachments"])

    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()
    self.wfile.write(json.dumps(desired))

HTTPServer(("", 80), Controller).serve_forever()