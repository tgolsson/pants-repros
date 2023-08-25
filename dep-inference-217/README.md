# Missing dependency inference in 2.17.0rc4

This is a reproduction of an issue discovered with Pants 2.17.0rc4 where dependency inference that worked in 2.16 is failing to collect all necessary deps.

To reproduce, compare the output of this command:

``` shell
$ # this can run (though fails due to no test functions)
$ PANTS_VERSION=2.16.0 pants --no-verify-config test cmd::
```

```
? ? PANTS_VERSION=2.16.0 pants --no-verify-config test cmd::
19:46:25.16 [INFO] Initialization options changed: reinitializing scheduler...
19:46:32.54 [INFO] Scheduler initialized.
19:46:49.32 [INFO] Completed: Building 2 requirements for requirements.pex from the locks/base.lock resolve: tensorboard>=2.8, torch!=1.12.0+cpu,!=1.12.0+cu116,==1.12.0
19:46:50.42 [INFO] Completed: Building local_dists.pex
19:47:03.88 [INFO] Completed: Building pytest_runner.pex
19:47:07.88 [ERROR] Completed: Run Pytest - cmd/test_decimate.py:tests - failed (exit code 5).
============================= test session starts ==============================
platform linux -- Python 3.9.16, pytest-7.0.1, pluggy-1.0.0
rootdir: /tmp/pants-sandbox-NY81iz
plugins: forked-1.6.0, cov-3.0.0, xdist-2.5.0
collected 0 items

=============================== warnings summary ===============================
../../home/ts/.cache/pants/named_caches/pex_root/venvs/s/ce0d5fe1/venv/lib/python3.9/site-packages/torch/utils/tensorboard/__init__.py:4
  /home/ts/.cache/pants/named_caches/pex_root/venvs/s/ce0d5fe1/venv/lib/python3.9/site-packages/torch/utils/tensorboard/__init__.py:4: DeprecationWarning: distutils Version classes are deprecated. Use packaging.version instead.
    if not hasattr(tensorboard, "__version__") or LooseVersion(

../../home/ts/.cache/pants/named_caches/pex_root/venvs/s/ce0d5fe1/venv/lib/python3.9/site-packages/torch/utils/tensorboard/__init__.py:6
  /home/ts/.cache/pants/named_caches/pex_root/venvs/s/ce0d5fe1/venv/lib/python3.9/site-packages/torch/utils/tensorboard/__init__.py:6: DeprecationWarning: distutils Version classes are deprecated. Use packaging.version instead.
    ) < LooseVersion("1.15"):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
- generated xml file: /tmp/pants-sandbox-NY81iz/cmd.test_decimate.py.tests.xml -
============================= 2 warnings in 2.17s ==============================

```

With this command:

```shell
$ # this fails to import torch
$ pants test cmd::
```

```
? ? pants test cmd::
19:47:32.33 [WARN] DEPRECATED: using a `pants` launcher binary older than 0.9.2 is scheduled to be removed in version 2.18.0.dev6.

Run `PANTS_BOOTSTRAP_VERSION=report pants` to see the current version of the `pants` launcher binary, and see https://www.pantsbuild.org/v2.17/docs/installation for how to upgrade.
19:47:37.83 [INFO] waiting for pantsd to start...
19:47:39.83 [INFO] pantsd started
19:47:39.95 [INFO] Initializing scheduler...
19:47:45.80 [INFO] Scheduler initialized.
19:47:45.89 [WARN] /home/ts/.cache/nce/c55ee58a557d20bd4b109870e5a01b264c0d501ce817cce29502b2552903834d/bindings/venvs/2.17.0rc4/lib/python3.9/site-packages/pkg_resources/_vendor/packaging/specifiers.py:255: DeprecationWarning: Creating a LegacyVersion has been deprecated and will be removed in the next major release
  warnings.warn(

19:47:48.31 [WARN] Pants cannot infer owners for the following imports in the target cmd/test_decimate.py:tests:

  * tensorboard.backend.event_processing.event_accumulator (line: 1)

If you do not expect an import to be inferrable, add `# pants: no-infer-dep` to the import line. Otherwise, see https://www.pantsbuild.org/v2.17/docs/troubleshooting#import-errors-and-missing-dependencies for common problems.
19:47:48.31 [WARN] Pants cannot infer owners for the following imports in the target cmd/decimate.py:

  * tensorboard.backend.event_processing.event_accumulator (line: 4)
  * tensorboard.compat.proto.summary_pb2.HistogramProto (line: 6)
  * tensorboard.compat.proto.summary_pb2.Summary (line: 6)
  * tensorboard.compat.proto.types_pb2 (line: 5)

If you do not expect an import to be inferrable, add `# pants: no-infer-dep` to the import line. Otherwise, see https://www.pantsbuild.org/v2.17/docs/troubleshooting#import-errors-and-missing-dependencies for common problems.
19:47:48.35 [WARN] /home/ts/.cache/nce/c55ee58a557d20bd4b109870e5a01b264c0d501ce817cce29502b2552903834d/bindings/venvs/2.17.0rc4/lib/python3.9/site-packages/pkg_resources/_vendor/packaging/version.py:111: DeprecationWarning: Creating a LegacyVersion has been deprecated and will be removed in the next major release
  warnings.warn(

19:47:48.87 [ERROR] Completed: Run Pytest - cmd/test_decimate.py:tests - failed (exit code 2).
============================= test session starts ==============================
platform linux -- Python 3.9.16, pytest-7.0.1, pluggy-1.0.0
rootdir: /tmp/pants-sandbox-xvOIuU
plugins: forked-1.6.0, cov-3.0.0, xdist-2.5.0
collected 0 items / 1 error

==================================== ERRORS ====================================
____________________ ERROR collecting cmd/test_decimate.py _____________________
ImportError while importing test module '/tmp/pants-sandbox-xvOIuU/cmd/test_decimate.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.9/importlib/__init__.py:127: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
cmd/test_decimate.py:2: in <module>
    from torch.utils.tensorboard import SummaryWriter
E   ModuleNotFoundError: No module named 'torch'
- generated xml file: /tmp/pants-sandbox-xvOIuU/cmd.test_decimate.py.tests.xml -
=========================== short test summary info ============================
ERROR cmd/test_decimate.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
=============================== 1 error in 0.20s ===============================
```
