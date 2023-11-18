# Reproduction for unable to find shared libraries when included in .pex

The following command should print some cuda information on systems with a GPU, graphics driver, and native component:

``` shellsession
$ pants run cmd/cuda.py
14:16:22.56 [INFO] Completed: Building cmd.pex with 1 requirement: torch>=2
/home/ts/.cache/pants/named_caches/pex_root/venvs/s/6d67ba16/venv/lib/python3.9/site-packages/torch/nn/modules/transformer.py:20: UserWarning: Failed to initialize NumPy: No module named 'numpy' (Triggered internally at ../torch/csrc/utils/tensor_numpy.cpp:84.)
  device: torch.device = torch.device(torch._C._get_default_device()),  # torch.device('cpu'),
2.1.1+cu121
Sat Nov 18 14:16:23 2023
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.86.01              Driver Version: 536.67       CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  NVIDIA GeForce RTX 3080        On  | 00000000:06:00.0  On |                  N/A |
| 30%   46C    P0              97W / 320W |   1971MiB / 10240MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+

+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|    0   N/A  N/A     17636      G   /Xwayland                                 N/A      |
+---------------------------------------------------------------------------------------+

ERROR:root:nvcc not found
libcuda.so: cannot open shared object file: No such file or directory
Device: "NVIDIA GeForce RTX 3080"
  Compute capability: (8, 6)
  Multiprocessors:    68
  Warp size:          1536
  Clock rate:         1710000
  Memory clock rate:  1710000
  Total memory:       4294967295
  Cuda cores: 4352
```

The same file ran as a `pex_binary` fails:

``` shellsession
$ # can also :packed, same result
$ pants run cmd:loose
Traceback (most recent call last):
  File "/home/ts/.pex/installed_wheels/0387b97fad0e6603e4d75e20bba37b1b8b37a5246b6d316feb78cf2b38a67408/torch-2.1.1-cp39-cp39-manylinux1_x86_64.whl/torch/__init__.py", line 174, in _load_global_deps
    ctypes.CDLL(lib_path, mode=ctypes.RTLD_GLOBAL)
  File "/usr/lib/python3.9/ctypes/__init__.py", line 374, in __init__
    self._handle = _dlopen(self._name, mode)
OSError: libcufft.so.11: cannot open shared object file: No such file or directory

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/lib/python3.9/runpy.py", line 197, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "/usr/lib/python3.9/runpy.py", line 87, in _run_code
    exec(code, run_globals)
  File "/home/ts/.pex/unzipped_pexes/f76b4b03b46425686e8da607a0a0a9cf1f9f7ed9/__main__.py", line 106, in <module>
    bootstrap_pex(__entry_point__, execute=__execute__, venv_dir=__venv_dir__)
  File "/home/ts/.pex/unzipped_pexes/f76b4b03b46425686e8da607a0a0a9cf1f9f7ed9/.bootstrap/pex/pex_bootstrapper.py", line 618, in bootstrap_pex
    pex.PEX(entry_point).execute()
  File "/home/ts/.pex/unzipped_pexes/f76b4b03b46425686e8da607a0a0a9cf1f9f7ed9/.bootstrap/pex/pex.py", line 560, in execute
    sys.exit(self._wrap_coverage(self._wrap_profiling, self._execute))
  File "/home/ts/.pex/unzipped_pexes/f76b4b03b46425686e8da607a0a0a9cf1f9f7ed9/.bootstrap/pex/pex.py", line 467, in _wrap_coverage
    return runner(*args)
  File "/home/ts/.pex/unzipped_pexes/f76b4b03b46425686e8da607a0a0a9cf1f9f7ed9/.bootstrap/pex/pex.py", line 498, in _wrap_profiling
    return runner(*args)
  File "/home/ts/.pex/unzipped_pexes/f76b4b03b46425686e8da607a0a0a9cf1f9f7ed9/.bootstrap/pex/pex.py", line 603, in _execute
    return self.execute_entry(
  File "/home/ts/.pex/unzipped_pexes/f76b4b03b46425686e8da607a0a0a9cf1f9f7ed9/.bootstrap/pex/pex.py", line 800, in execute_entry
    return self.execute_module(entry_point.module)
  File "/home/ts/.pex/unzipped_pexes/f76b4b03b46425686e8da607a0a0a9cf1f9f7ed9/.bootstrap/pex/pex.py", line 808, in execute_module
    runpy.run_module(module_name, run_name="__main__", alter_sys=True)
  File "/usr/lib/python3.9/runpy.py", line 225, in run_module
    return _run_module_code(code, init_globals, run_name, mod_spec)
  File "/usr/lib/python3.9/runpy.py", line 97, in _run_module_code
    _run_code(code, mod_globals, init_globals,
  File "/usr/lib/python3.9/runpy.py", line 87, in _run_code
    exec(code, run_globals)
  File "/home/ts/.pex/unzipped_pexes/f76b4b03b46425686e8da607a0a0a9cf1f9f7ed9/cuda.py", line 8, in <module>
    import torch
  File "/home/ts/.pex/installed_wheels/0387b97fad0e6603e4d75e20bba37b1b8b37a5246b6d316feb78cf2b38a67408/torch-2.1.1-cp39-cp39-manylinux1_x86_64.whl/torch/__init__.py", line 234, in <module>
    _load_global_deps()
  File "/home/ts/.pex/installed_wheels/0387b97fad0e6603e4d75e20bba37b1b8b37a5246b6d316feb78cf2b38a67408/torch-2.1.1-cp39-cp39-manylinux1_x86_64.whl/torch/__init__.py", line 195, in _load_global_deps
    _preload_cuda_deps(lib_folder, lib_name)
  File "/home/ts/.pex/installed_wheels/0387b97fad0e6603e4d75e20bba37b1b8b37a5246b6d316feb78cf2b38a67408/torch-2.1.1-cp39-cp39-manylinux1_x86_64.whl/torch/__init__.py", line 161, in _preload_cuda_deps
    ctypes.CDLL(lib_path)
  File "/usr/lib/python3.9/ctypes/__init__.py", line 374, in __init__
    self._handle = _dlopen(self._name, mode)
OSError: libnvJitLink.so.12: cannot open shared object file: No such file or directory
```

Uncomment the `import nvidia` line in the `cuda.py` should fix both `loose` and `packed` formats
