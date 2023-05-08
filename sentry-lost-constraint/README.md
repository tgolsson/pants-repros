This subdirectory contains a reproduction of a potential lockfile generation bug where some constraints are ignored in the lockfile.

Sentry has the following constraints for urllib3:
```json
        [
            "urllib3<2.0.0",
            "urllib3>=1.25.7; python_version <= \"3.4\"",
            "urllib3>=1.26.11; python_version >= \"3.6\"",
            "urllib3>=1.26.9; python_version == \"3.5\""
        ]
```

But the lockfile will (randomly) resolve with the following:

``` json
          "artifacts": [
            {
              "algorithm": "sha256",
              "hash": "d055c2f9d38dc53c808f6fdc8eab7360b6fdbbde02340ed25cfbcd817c62469e",
              "url": "https://files.pythonhosted.org/packages/4b/1d/f8383ef593114755429c307449e7717b87044b3bcd5f7860b89b1f759e34/urllib3-2.0.2-py3-none-any.whl"
            },
            {
              "algorithm": "sha256",
              "hash": "61717a1095d7e155cdb737ac7bb2f4324a858a1e2e6466f6d03ff630ca68d3cc",
              "url": "https://files.pythonhosted.org/packages/fb/c0/1abba1a1233b81cf2e36f56e05194f5e8a0cec8c03c244cab56cc9dfb5bd/urllib3-2.0.2.tar.gz"
            }
          ],
```
