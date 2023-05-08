This subdirectory contains a reproduction of a potential lockfile generation bug reported in [this thread](https://pantsbuild.slack.com/archives/C046T6T9U/p1683187396031649).

The (potential) bug is the following:

* Pex-via-Pants lockfiles are meant to generate a lockfile that works on both Mac and Linux by default
* PEP440 says that whenever local tags are available we should prefer those
* But the same tag isn't available on each platform.

Running `pants generate-lockfiles' will generate an invalid set of dependencies unless explicitly disallowing local versions. This is the expected set:

``` shellsession
$ cat locks/valid.lock | grep -v "^\s*//" | jq '.locked_resolves[0].locked_requirements[0] | select(.project_name == "torch") | .artifacts'
[
  {
    "algorithm": "sha256",
    "hash": "831cf588f01dda9409e75576741d2823453990dee2983d670f2584b37a01adf7",
    "url": "https://download.pytorch.org/whl/torch-1.11.0-cp39-cp39-manylinux2014_aarch64.whl"
  },
  {
    "algorithm": "sha256",
    "hash": "50fd9bf85c578c871c28f1cb0ace9dfc6024401c7f399b174fb0f370899f4454",
    "url": "https://download.pytorch.org/whl/cpu/torch-1.11.0-cp39-none-macosx_10_9_x86_64.whl"
  },
  {
    "algorithm": "sha256",
    "hash": "0e48af66ad755f0f9c5f2664028a414f57c49d6adc37e77e06fe0004da4edb61",
    "url": "https://download.pytorch.org/whl/cpu/torch-1.11.0-cp39-none-macosx_11_0_arm64.whl"
  },
  {
    "algorithm": "sha256",
    "hash": "831cf588f01dda9409e75576741d2823453990dee2983d670f2584b37a01adf7",
    "url": "https://files.pythonhosted.org/packages/cf/9a/8d80deb5d2e9e17933f5dfe717a42a7608dc0e6799f7a7a0de3f7d7093d7/torch-1.11.0-cp39-cp39-manylinux2014_aarch64.whl"
  },
  {
    "algorithm": "sha256",
    "hash": "0e48af66ad755f0f9c5f2664028a414f57c49d6adc37e77e06fe0004da4edb61",
    "url": "https://files.pythonhosted.org/packages/ec/bc/5e2b92f471496da1629e156553c8d92e0df667743f3128dd5e4db287ddb9/torch-1.11.0-cp39-none-macosx_11_0_arm64.whl"
  },
  {
    "algorithm": "sha256",
    "hash": "58c7814502b1c129a650d7092033bbb0bbd64faf1a7941631aaa1aeaddc37570",
    "url": "https://files.pythonhosted.org/packages/f8/04/ebf936e02d37c185341558de73324c6511d7fb7578cb1c3439411475fd7e/torch-1.11.0-cp39-cp39-manylinux1_x86_64.whl"
  },
  {
    "algorithm": "sha256",
    "hash": "50fd9bf85c578c871c28f1cb0ace9dfc6024401c7f399b174fb0f370899f4454",
    "url": "https://files.pythonhosted.org/packages/fe/6f/9d42e62cbd28e69fef578f8c4a1d33a4716d378dbc7ae720d211b28dc81a/torch-1.11.0-cp39-none-macosx_10_9_x86_64.whl"
  }
]
```

This is the actual set. Note that when not requesting a local tag we've been given cu115, but as that doesn't exist on Mac the lock is invalid.

``` shellsession
$ cat locks/broken.lock | grep -v "^\s*//" | jq '.locked_resolves[0].locked_requirements[0] | select(.project_name == "torch") | .artifacts'
[
  {
    "algorithm": "sha256",
    "hash": "eb81d067bbcfe844c95c5d27e26c97a96a893427cc468b2259eaf0ed93da1c7d",
    "url": "https://download.pytorch.org/whl/cu115/torch-1.11.0%2Bcu115-cp39-cp39-linux_x86_64.whl"
  }
]
```

At the same time, we want to be able to select GPU and CPU variants, which are working as expected (and we're fine with them not working on Mac).

``` shellsession
$ cat locks/gpu.lock | grep -v "^\s*//" | jq '.locked_resolves[0].locked_requirements[0] | select(.project_name == "torch") | .artifacts'
[
  {
    "algorithm": "sha256",
    "hash": "eb81d067bbcfe844c95c5d27e26c97a96a893427cc468b2259eaf0ed93da1c7d",
    "url": "https://download.pytorch.org/whl/cu115/torch-1.11.0%2Bcu115-cp39-cp39-linux_x86_64.whl"
  }
]
```

``` shellsession
$ cat locks/cpu.lock | grep -v "^\s*//" | jq '.locked_resolves[0].locked_requirements[0] | select(.project_name == "torch") | .artifacts'
[
  {
    "algorithm": "sha256",
    "hash": "544c13ef120531ec2f28a3c858c06e600d514a6dfe09b4dd6fd0262088dd2fa3",
    "url": "https://download.pytorch.org/whl/cpu/torch-1.11.0%2Bcpu-cp39-cp39-linux_x86_64.whl"
  }
]
```
